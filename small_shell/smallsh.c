#define _POSIX_C_SOURCE 2008090L
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdbool.h>
#include <signal.h>
#include <sys/types.h>



char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub);
int static execute(void);
int my_exit();
int cd();
int redirect();
int checking();
void signal_handler(int signal){};
char *line = NULL;
size_t n = 0;
char *words[512];
char *command;
char *arguments[512];
char *in_file = NULL;
char *out_file = NULL;
char *p;
int words_index = 0;
int i = 0;
int exit_num = 0;
char question_expand[10] = "0";
char exclamation_expand[10] = "";
int bg = 0;
pid_t childPid = -5;
int childStatus;


int main(void){
  signal(SIGINT, SIG_IGN);
  signal(SIGTSTP, SIG_IGN);
  int ssh_pid = getpid();
  char *pid = malloc(8);
  sprintf(pid, "%d", ssh_pid);
  
  char *IFS = getenv("IFS");
  if (IFS == NULL){
    IFS = " \t\n";
  }
  for (;;){
    checking();
    in_file = NULL;
    out_file = NULL;
    bg = 0;
    if (getenv("PS1") == NULL){
      fprintf(stderr, "%s",  "");
    }
    else {
      fprintf(stderr, "%s", getenv("PS1"));
    }
    for (i = 0; i < 512; i++){
      words[i] = NULL;
    }
    words_index = 0;
    i = 0;
    if (getline(&line, &n, stdin)){
      signal(SIGINT, signal_handler);
      if (strcmp(&line[0], "\n") == 0){
          continue;
      }
    }
    p = strtok(line, IFS);
    if (p != NULL){
      words[i] = strdup(p);
      i++;
    }
    while (p != NULL){
     p = strtok(NULL, IFS);
     if (p == NULL){
       continue;
     }else if ((strncmp(p, "~/", 2) == 0)){
       words[i] = strdup(p);
       str_gsub(&words[i], "~", getenv("HOME"));
     }else{
       if (strcmp(p, "#") == 0){
         break;
       }
       words[i] = strdup(p);
       str_gsub(&words[i], "$$", pid);
       str_gsub(&words[i], "$!", exclamation_expand);
       str_gsub(&words[i], "$?", question_expand);
     }
     i++;
     words_index++;
    }
    if (strcmp(words[0], "exit") == 0){
      my_exit();
    }
    if (strcmp(words[0], "cd") == 0){
      cd();
      continue;
    }
    if (strcmp(words[words_index], "&") == 0){
      bg = 1;
      words[words_index] = NULL;
    }
    if (words_index > 1){
      redirect();
    }
    execute();
  }
return 0;
}

// copied from Ryan Gambord at https://youtube.com/watch?v=-3ty5W_6-IQ
char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub){
  char *str = *haystack;
  size_t haystack_len = strlen(str);
  size_t const needle_len = strlen(needle),
               sub_len = strlen(sub);

  for (; (str = strstr(str, needle));) {
    ptrdiff_t off = str - *haystack;
    if (sub_len > needle_len) { 
      str = realloc(*haystack, sizeof **haystack * (haystack_len + sub_len - needle_len + 1));
      if (!str) goto exit; 
      *haystack = str;
      str = *haystack + off;
    }

    memmove(str + sub_len, str + needle_len, haystack_len + 1 - off - needle_len);
    memcpy(str, sub, sub_len);
    haystack_len = haystack_len + sub_len - needle_len;
    str += sub_len;
  }
  str = *haystack;
  if (sub_len < needle_len) {
    str = realloc(*haystack, sizeof **haystack * (haystack_len + 1));
    if (!str) goto exit;
    *haystack = str;
  }
exit:
  return str;
}

int execute(void){
  childPid = fork();
  int in;
  int out;
  switch(childPid){
    case -1:
      perror("fork() failed!");
      exit(1);
      break;
    case 0:
      if (in_file != NULL){
        in = open(in_file, O_RDONLY | O_CREAT);
        dup2(in, STDIN_FILENO);
      }
      if (out_file != NULL){
        out = open(out_file, O_RDWR | O_CREAT | O_TRUNC, 0777);
        dup2(out, STDOUT_FILENO);
      }
      execvp(words[0], words);
    default:
      if (bg == 0){
        waitpid(childPid, &childStatus, 0);
        if (WIFEXITED(childStatus)){
          sprintf(question_expand, "%d", WEXITSTATUS(childStatus));
        }
      }else if (bg == 1){
        sprintf(exclamation_expand, "%d", childPid);
        break;
      }
  }
  free(*words);
  return 0;
}


int my_exit(){
  int exit_num = 0;
  if (strcmp(words[0], "exit") == 0){
    if (words[1] == NULL){
      words[1] = question_expand;
    }
    exit_num = atoi(words[1]);
    printf("\nexit\n");
    exit(exit_num);
  }
  exit_num = atoi(question_expand);
  printf("\nexit\n");
  exit(exit_num);
  }

int cd(){
  if (words[2] != NULL){
    perror("too many arguments");
    return -1;
  }
  if (words[1] == NULL){
    if (chdir(getenv("HOME")) == -1){
      perror("no such file or directory");
      return -1;
    }
  } else if ((chdir(words[1]) == -1)){
      perror("no such file or directory");
      return -1;
    }
  return 0;
}

int redirect(){
  if (words_index >= 4){
    if (strcmp(words[words_index-1], "<") == 0){
      in_file = words[words_index];
      words[words_index-1] = NULL;
      if (strcmp(words[words_index-3], ">") == 0){
        out_file = words[words_index-2];
        words[words_index-3] = NULL;
      }
    }
    if (strcmp(words[words_index-1], ">") == 0){
      out_file = words[words_index];
      words[words_index-1] = NULL;
    }
      if (strcmp(words[words_index-3], "<") == 0){
        in_file = words[words_index-2];
        words[words_index-3] = NULL;
      }
  }else if (strcmp(words[words_index-1], "<") == 0){
    in_file = words[words_index];
    words[words_index-1] = NULL;
  }else if (strcmp(words[words_index-1], ">") == 0){
    out_file = words[words_index];
    words[words_index-1] = NULL;
  }
  return 0;
}

int checking(){
  while ((childPid = waitpid(0, &childStatus, WUNTRACED | WNOHANG)) > 0){
    sprintf(exclamation_expand, "%d", childPid);
    if (WIFEXITED(childStatus)){
      sprintf(question_expand, "%d", WEXITSTATUS(childStatus));
      fprintf(stderr, "Child process %d done. Exit status %d. \n", childPid, childStatus);
    }else if(WIFSTOPPED(childStatus)){
      fprintf(stderr, "Child process %d stopped.  Continuing.\n", childPid);
      kill(childPid, SIGCONT);
    }else if (WIFSIGNALED(childStatus)){
      fprintf(stderr, "Child process %d stopped. Signaled %d.\n", childPid, WTERMSIG(childStatus));
      printf("\nexit\n");
      exit(0);
    }
  }
  return 0;
}


