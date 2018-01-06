// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP_OUT)
	@SCREEN
	D = A
// sum = address of screen	
	@sum
	M = D
	
	@KBD
	D = M
	@WHITE
	D;JEQ

// BLACK	
	@8192
	D = -A
(LOOP_IN1)
//all done!
	@LOOP_OUT
	D;JEQ
	
	@temp
	M = D
	
	@sum
	A = M
	M = -1
	@sum
	M = M + 1
	
	@temp
	D = M + 1	
	
	@LOOP_IN1
	0;JMP
	
(WHITE)
	@8192
	D = -A
(LOOP_IN2)
//all done!
	@LOOP_OUT
	D;JEQ
	
	@temp
	M = D
	
	@sum
	A = M	
	M = 0
	@sum
	M = M + 1
	
	@temp
	D = M + 1	
	
	@LOOP_IN2
	0;JMP	