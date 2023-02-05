TITLE PROGRAMMING ASSIGNMENT 6    (Proj6_artmayek.asm)

; Author: Kodie Artmayer
; Last Modified:  12/5/2021
; OSU email address: artmayek@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number:  6               Due Date: 12/5/2021
; Description: Create a program that uses two macros to for string processing.  Create Two procedures for signed integer processing
;			   using string primitive instructions.  Gets 10 valid integers from a user stores these in an array, displays their sum
;			   and truncated average.
;Despite my countless hours of debugging I cannot get this spaghetti code to work properly

INCLUDE Irvine32.inc

;description: gets a string of numbers from a user
;preconditions: variables defined
;postconditions: do not use eax as an argument
;receives: prompt, string, count, len
;returns: length of the string entered
mGetString		MACRO	prompt, string, count, len
	push	ecx
	push	edx
	mov		edx, prompt
	call	WriteString
	mov		edx, string
	mov		ecx, count
	call	ReadString
	mov		len, eax
	pop		edx
	pop		ecx
ENDM

;description: displays a string 
;preconditions: address of string passed 
;postconditions: do not use edx as an argument
;receives: display_string
;returns: None
mDisplayString MACRO display_string
	push	edx

	mov		edx, display_string
	call	WriteString

	pop		edx
ENDM
;CONSTANTS

MAX = 10		;Maximum amount of numbers for a user to enter

.data

Intro			BYTE	"PROGRAMMING ASSIGNMENT 6: Designing low-level I/O procedures",10,13
				BYTE	"Written by: Kodie Artmayer",10,13,0
Intro2			BYTE	"Please provide 10 signed decimal integers.",10,13
				BYTE	"Each number needs to be small enough to fit inside a 32 bit register. After you have finished ",10,13
				BYTE	"inputting the raw numbers I will display a list offset the integers, ",10,13
				BYTE	"their sum, and their average value.",10,13,0
prompt			BYTE	"Please enter a signed number: ", 0
error			BYTE	"Either you didn't enter a number or it was too large for a 32 bit register: ", 0
usrNumbers		BYTE	"The numbers you entered are: ", 0
comma			BYTE	", ", 0
sumPrompt		BYTE	"The sum of the numbers you entered is: ", 0
averagePrompt	BYTE	"The average of the numbers you entered is: ", 0
farewell		BYTE	"GoodBye!", 0
usrArray		BYTE	MAX DUP(?)			;array where we need to store numbers
usrInput		SDWORD	10 DUP(?)
inputString		BYTE	11 DUP(0)
outputString	BYTE	11 DUP(0)
len				DWORD	?	
average			SDWORD	0					;average
sum				SDWORD	0					;sum
negative		DWORD	0
.code
main PROC
	
	push	OFFSET Intro				;40
	push	OFFSET Intro2				;36
	call	Introduction
	
	push	OFFSET usrInput				;56
	push	OFFSET negative				;52	
	push	OFFSET error				;48
	push	OFFSET prompt				;44
	push	OFFSET usrArray				;40
	push	OFFSET len					;36
	call	ReadVal
	call	Crlf
	
	push	OFFSET sumPrompt			;44
	push	OFFSET sum					;40
	push	OFFSET usrInput				;36
	call	CalculateSum

	push	OFFSET averagePrompt		;44
	push	OFFSET average				;40
	push	OFFSET sum					;36
	call	CalculateAvg

	push	OFFSET Farewell				;4
	call	Goodbye

	Invoke ExitProcess,0	; exit to operating system
main ENDP

;description: introduce the program
;preconditions: variables defined and pushed to the stack
;postconditions: changes edx
;receives: parameters Intro, Intro2
;returns: None
Introduction PROC
	pushad							;preserve registers
	mov		ebp,esp
	mDisplayString [ebp + 40]
	call	CrLf
	mDisplayString [ebp + 36]
	call	Crlf
	popad							;restore registers
	ret		8
Introduction ENDP

;description: Reads a value entered by a user converts ASC II code into a number and stores it into an array
;preconditions: array and variables defined and pushed to the stack
;postconditions: ebp, esp, edi, ecx, eax, ebx, and edx changed
;receives: parameters usrInput, negative, error, prompt, usrArray, len
;returns: usrInput, usrArray
ReadVal PROC
	pushad							;preserve registers
	mov		ebp, esp				;setup stack
	
	mov		edi, [ebp + 56]			;access array to add into
	mov		ecx, MAX				;set up counter for loop
_start1:
	push	ecx

_start2:
	mGetString [ebp + 44], [ebp + 40], MAX, [ebp + 36]			;read input
	push	eax
	mov		eax, [ebp + 36]
	mov		ecx, eax											;length of string
	pop		eax
	mov		esi, [ebp + 40]				
	mov		ebx, 0
	mov		[ebp + 52], ebx										;variable to add negative later
	cmp		ecx, 10												;largest amount of numbers a user can enter without being too large
	jg		_invalid
	lodsb
_top:
	cmp		al, 45
	je		_isNegative
	cmp		al, 43
	je		_plus
	jmp		_validation

_plus:
	dec		ecx													;user entered a plus sign
	jmp		_next

_isNegative:
	push	ebx													;user entered a negative sign
	mov		ebx, 1
	mov		[ebp + 52], ebx
	pop		ebx
	dec		ecx
	jmp		_next

_next:
	cld
	lodsb														;clear direction flag load next number
	jmp		_top

_validation:
	cmp		al, 48												;check to make sure its a number
	jb		_invalid
	cmp		al, 57
	jg		_invalid
	jmp		_add

_invalid:
	mDisplayString [ebp + 48]
	call	CrLf
	mov		ebx, 0
	mov		[edi], ebx
	jmp		_start2

_add:
	mov		ebx, [edi]							;convert ASC II characters to numbers
	push	eax
	push	ebx
	mov		eax, ebx
	mov		ebx, 10
	mul		ebx
	mov		[edi], eax
	pop		ebx
	pop		eax
	sub		al, 48
	add		[edi], al
	dec		ecx
	cmp		ecx, 0 
	ja		_next

	push	eax
	mov		eax, [ebp + 52]
	cmp		eax, 1 
	je		_makeNegative
	jmp		_end

_makeNegative:
	mov		eax,[edi]							;add back the negative sign for the array
	neg		eax
	mov		[edi], eax

_end:
	pop		eax									;increment to next location in the array
	add		edi, 4
	pop		ecx
	dec		ecx									;loop wouldn't work?
	cmp		ecx, 0
	ja		_start1

	popad										;restore registers
	ret		28
ReadVal ENDP

;description: could not get a writeVal procedure to work
;preconditions:
;postconditions:
;receives:
;returns:
WriteVal PROC

WriteVal ENDP

;description: calculates and displays the sum of the array, couldn't get writeVal to work so it doesn't display the sum
;preconditions: filled out array, parameters defined and pushed to stack
;postconditions: ebp, esp, ecx, esi, edx, eax changed
;receives: sumPrompt, sum, usrInput
;returns: sum
CalculateSum PROC
	pushad							;preserve registers
	mov		ebp, esp
	mDisplayString [ebp + 44]
	call	Crlf
	mov		ecx, MAX
	mov		esi, [ebp + 36]			;address of array of inputed numbers
_sumLoop:
	mov		eax, [esi]				;move address of first element into eax
	add		[ebp + 40], eax			;add eax to sum variable
	add		esi, 4					;get next element
	loop	_sumLoop
	
	popad							;restore registers
	ret		12
CalculateSum ENDP

;description: calculates and displays the average of the array, couldn't get writeVal to work so it doesn't display the average
;preconditions: sum to be calculated, variables pushed on the stack
;postconditions: ebp, ecx, eax, edx, ebx changed
;receives: parameters averagePrompt, average, sum
;returns: average
CalculateAvg PROC
	pushad							;preserve registers
	mov		ebp, esp
	mDisplayString	[ebp + 44]
	call	crlf
	mov		ecx, MAX
	mov		eax, [ebp + 36]			;move address of sum in eax

	mov		ebx, MAX				;set up for division
	mov		edx, 0
	cdq
	idiv	ebx

	mov		ebx, [ebp + 40]			;move address of average in ebx
	mov		[ebx], eax				;store average at the address in ebx
	popad							;restore registers
	ret		12
CalculateAvg ENDP

;description: display a farwell message with a macro
;preconditions: variables defined and pushed on the stack
;postconditions: ebp, edx changed
;receives:farewell
;returns: None
Goodbye	PROC
	pushad							;preserve registers
	mov		ebp, esp
	mDisplayString [ebp + 36]
	popad							;restore registers
	ret		4
Goodbye ENDP
END main
