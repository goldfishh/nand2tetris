#include <iostream>
#include <cstdio>
#include <cstring>
#include <string>
#include <fstream>
#include <stack>
#define SP 0
#define LCL 1
#define ARG 2
#define THIS 3
#define THAT 4
using namespace std;
bool Isignore(string snow){
	int ptr = 0;
	while(snow[ptr] == ' ' || snow[ptr] == '\t') ptr++;
	if(snow[ptr] == '\n')
		return true;
	else if(snow[ptr] == '/' && snow[ptr+1] == '/')
		return true;
	else return true;
}
class CodeWriter{
	string file_name;
	ofstream fout;
//	friend class Parser;
	stack <int> sk;
	int nstatic;
public:
	CodeWriter(){
		nstatic = 0;
	}
	void setFileName(string fname){
		file_name = fname;	
		fout.open(file_name);
	}
	void writeArithmetic(string command){
		if(command == "add"){
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M+D" << endl;
		}
		else if(command == "sub"){
			fout << "@SP\nA=M-1\nD=-M\n@SP\nM=M-1\nA=M-1\nM=M+D" << endl;
		}
		else if(command == "neg"){
			fout << "@SP\nA=M-1\nM=-M" << endl;
		}
		else if(command == "eq"){
			int a = sk.top();
			sk.pop();
			int b = sk.top();
			sk.pop();
			if(a == b){
				fout << "@SP\nM=M-1\nA=M-1\nM=-1" << endl;
				sk.push(-1);
			}
			else{
				fout << "@SP\nM=M-1\nA=M-1\nM=0" << endl;
				sk.push(0);
			}
		}
		else if(command == "gt"){
			int a = sk.top();
			sk.pop();
			int b = sk.top();
			sk.pop();
			if(a > b){
				fout << "@SP\nM=M-1\nA=M-1\nM=-1" << endl;
				sk.push(-1);
			}
			else{
				fout << "@SP\nM=M-1\nA=M-1\nM=0" << endl;
				sk.push(0);
			}			
		}
		else if(command == "lt"){
			int a = sk.top();
			sk.pop();
			int b = sk.top();
			sk.pop();
			if(a < b){
				fout << "@SP\nM=M-1\nA=M-1\nM=-1" << endl;
				sk.push(-1);
			}
			else{
				fout << "@SP\nM=M-1\nA=M-1\nM=0" << endl;
				sk.push(0);
			}			
		}
		else if(command == "and"){
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M&D" << endl;
		}
		else if(command == "or"){
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M|D" << endl;
		}
		else if(command == "not"){
			fout << "@SP\nA=M-1\nM=!M" << endl;
		}
		else{
			printf("ERROR in writeArithmetic\n");
		}
	}
	void writePushPop(string command, string segment, int index){
		if(command == "push"){
			if(segment == "argument"){
				fout << "@" << index << "\nD=A\n@ARG\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "local"){
				fout << "@" << index << "\nD=A\n@LCL\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "static"){
				fout << "@" << file_name << "." << nstatic << "\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "constant"){
				sk.push(index);
				fout << "@" << index << "\nD=A" << "@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "this"){
				fout << "@" << index << "\nD=A\n@THIS\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "that"){
				fout << "@" << index << "\nD=A\n@THAT\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "pointer"){
				if(index == 0){
					fout << "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				}
				else if(index == 1){
					fout << "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				}
				else printf("ERROR writeArithmetic pointer");
			}
			else if(segment == "temp"){
				fout << "@5\nD=A\n@" << index << "\nD=D+A\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
		}
		else if(command == "pop"){
			if(segment == "argument"){
				fout << "@" << index << "\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "local"){
				fout << "@" << index << "\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "static"){
				fout << "@SP\nM=M-1\nA=M\nD=M\n" <<"@" << file_name << "." << nstatic << "\nM=D" << endl;
			}
//			else if(segment == "constant"){
//			
//			}
			else if(segment == "this"){
				fout << "@" << index << "\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "that"){
				fout << "@" << index << "\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "pointer"){
				if(index == 0){
					fout << "@SP\nM=M-1\nA=M\nD=M\n@3\nM=D" << endl;
				}
				else if(index == 1){
					fout << "@SP\nM=M-1\nA=M\nD=M\n@4\nM=D" << endl;
				}
				else{
					printf("ERROR in writePop pointer");
				}
			}
			else if(segment == "temp"){
				fout << "@" << index << "\nD=A\n@5\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}			
		}
	}
	void writeEnd(){
		printf("0;JMP");
	}
	void Close(){
		fout.close();
		while(!sk.empty()) sk.pop();
		writeEnd();
	}
};
class Parser{
	string file_name;
	string snow,sfuture;
//	friend class CodeWriter;
	CodeWriter cw_t;
	ifstream fin;	
public:
	Parser(string fname){
		file_name = fname;
		fin.open(file_name,ios::in);
	}
	~Parser(){
		fin.close();
	}
	bool hasMoreCommands(){
		if(!getline(fin,sfuture))
			return false;
		else return true;
	}
	void advance(){
		string command,segment;
		int index;
		while(hasMoreCommands()){
			snow = sfuture;
			if(Isignore(snow)){
				continue;
			}
			else if(commandType() == "C_PUSH"){
				command = "C_PUSH";
				segment = arg1();
				index = Arg2();
				cw_t.writePushPop(command, segment, index);
			}
			else if(commandType() == "C_POP"){
				command = "C_POP";
				segment = arg1();
				index = Arg2();	
				cw_t.writePushPop(command, segment, index);			
			}
			else if(commandType() == "C_ARITHMATIC"){
				command = "C_ARITHMATIC";
				cw_t.writeArithmetic(command);				
			}
			else printf("ERROR advance\n");
		}
	}
	string commandType(){ // generally is a command
		char stmp[100];
		int ptr = 0,end = snow.length();
		while(!isalpha(snow[ptr])) ptr++;
		snow = snow.substr(ptr, end);
		sscanf(snow.c_str(),"%s",stmp);
		if(stmp == "push")
			return "C_PUSH";
		else if(stmp == "pop")
			return "C_POP";		
		else if(stmp == "add" || stmp == "sub" || stmp == "neg" || 
				stmp == "eq" || stmp == "gt" || stmp == "lt" || 
				stmp == "and" || stmp == "or" || stmp == "not")
			return "C_ARITHMATIC";
//		"C_LABEL"
//		"C_GOTO"
//		"C_IF"
//		"C_FUNCTION"		
//		"C_RETURN"
//		"C_CALL"
	}
	string arg1(){
		// C_RETURE should not invoke this function.
		if(commandType() == "C_RETURN") printf("ERROR in arg1");
		char stmp[100];
		sscanf(snow.c_str(),"%*s%*[ ]%s",stmp);
		return stmp;
	}
	int Arg2(){
		if(commandType() == "C_POP" || commandType() == "C_PUSH"||
		   commandType() == "C_FUNCTION"||commandType() == "C_CALL"){
			char sint[100];
			int stoint;
			sscanf(snow.c_str(),"%*s%*[ ]%*s%*[ ]%s",sint);
			stoint = atoi(sint);
			return stoint;	   		
		   }
		else printf("ERROR Arg2");
	}
};

int main(int argc,char *argv[]){
//	freopen("datain","r",stdin);
	CodeWriter cw;
	for(int i = 0; i < argc - 1; i++){
		Parser tpr(*(argv+i));
		cw.setFileName(*(argv+i));
		tpr.advance();
		cw.Close();		
	}
	return 0;
}
