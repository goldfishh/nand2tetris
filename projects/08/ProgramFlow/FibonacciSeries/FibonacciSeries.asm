//push argument 1
@1
D=A
@ARG
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@4
M=D
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//pop that 0
@0
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
//pop that 1
@1
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//push constant 2
@2
D=A
@SP
M=M+1
A=M-1
M=D
//sub
@SP
A=M-1
D=-M
@SP
M=M-1
A=M-1
M=M+D
//pop argument 0
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//label MAIN_LOOP_START
(MAIN_LOOP_START)
//push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
//goto END_PROGRAM
@END_PROGRAM
0;JMP
//label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
//push that 0
@0
D=A
@THAT
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//push that 1
@1
D=A
@THAT
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//add
@SP
A=M-1
D=M
@SP
M=M-1
A=M-1
M=M+D
//pop that 2
@2
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//push pointer 1
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
//push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
//add
@SP
A=M-1
D=M
@SP
M=M-1
A=M-1
M=M+D
//pop pointer 1
@SP
M=M-1
A=M
D=M
@4
M=D
//push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
//sub
@SP
A=M-1
D=-M
@SP
M=M-1
A=M-1
M=M+D
//pop argument 0
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
//goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
//label END_PROGRAM
(END_PROGRAM)
(END)
@END
0;JMP

