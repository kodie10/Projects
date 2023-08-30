Custom Shell

A simple shell implementation in C that supports background processes, command executions, redirections, and custom signal handling.
Features

    Background Processes: Execute commands in the background by appending & at the end.
    Command Executions: Directly execute most of the UNIX commands.
    Redirections: Supports input (<) and output (>) redirections.
    
    Signal Handling:
        Ignores interruption signal (CTRL+C).
        Ignores stop signal (CTRL+Z).
        
    Custom Variables Expansion:
        Replace $$ with the shell's PID.
        Replace $! with the PID of the last process executed in the background.
        Replace $? with the exit status of the last foreground process.
        
    Path Expansion: Replace ~/ with the value of $HOME.
