//push constant 111
@111
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 333
@333
D=A
@SP
M=M+1
A=M-1
M=D
//push constant 888
@888
D=A
@SP
M=M+1
A=M-1
M=D
//pop static 8
@SP
M=M-1
A=M
D=M
@StaticTest.asm.8
M=D
//pop static 3
@SP
M=M-1
A=M
D=M
@StaticTest.asm.3
M=D
//pop static 1
@SP
M=M-1
A=M
D=M
@StaticTest.asm.1
M=D
//push static 3
@StaticTest.asm.3
D=M
@SP
M=M+1
A=M-1
M=D
//push static 1
@StaticTest.asm.1
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
//push static 8
@StaticTest.asm.8
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
