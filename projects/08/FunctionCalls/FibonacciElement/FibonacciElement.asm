@256
D=A
@SP
M=D
//call Sys.init 0
@48
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
//goto Sys.init
@Sys.init
0;JMP
//label return-address-0
(return-address-0)
//function Main.fibonacci 0
(Main.fibonacci)
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
//lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LT_-1
D,JLT
(LT_0)
@SP
M=M+1
A=M-1
M=0
@LTBJ
0;JMP
(LT_-1)
@SP
M=M+1
A=M-1
M=-1
(LTBJ)
//if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
//goto IF_FALSE
@IF_FALSE
0;JMP
//label IF_TRUE
(IF_TRUE)
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
//label IF_FALSE
(IF_FALSE)
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
//call Main.fibonacci 1
@222
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
//goto Main.fibonacci
@Main.fibonacci
0;JMP
//label return-address-1
(return-address-1)
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
//call Main.fibonacci 1
@289
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
//goto Main.fibonacci
@Main.fibonacci
0;JMP
//label return-address-2
(return-address-2)
//add
@SP
A=M-1
D=M
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
//function Sys.init 0
(Sys.init)
//push constant 4
@4
D=A
@SP
M=M+1
A=M-1
M=D
//call Main.fibonacci 1
@399
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
//goto Main.fibonacci
@Main.fibonacci
0;JMP
//label return-address-3
(return-address-3)
//label WHILE
(WHILE)
//goto WHILE
@WHILE
0;JMP
(END)
@END
0;JMP
