//function SimpleFunction.test 2
(SimpleFunction.test)
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
//push local 0
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
//push local 1
@1
D=A
@LCL
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
//not
@SP
A=M-1
M=!M
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
//add
@SP
A=M-1
D=M
@SP
M=M-1
A=M-1
M=M+D
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
//sub
@SP
A=M-1
D=-M
@SP
M=M-1
A=M-1
M=M+D
//return
@LCL
D=M
@R14
M=D
@5
D=D-A
A=D
D=M
@R15
M=D
@SP
M=M-1
A=M
D=M
@R13
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@SP
A=M-1
M=D
@R14
M=M-1
A=M
D=M
@THAT
M=D
@R14
M=M-1
A=M
D=M
@THIS
M=D
@R14
M=M-1
A=M
D=M
@ARG
M=D
@R14
M=M-1
A=M
D=M
@LCL
M=D
@R15
D=M
A=D
0;JMP
(END)
@END
0;JMP

