#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <string>
#include <fstream>
#include <stack>
#include <map>
#define SP 0
#define LCL 1
#define ARG 2
#define THIS 3
#define THAT 4
using namespace std;
int RAM[10000] = {256,300,400,3000,3010};
bool Isignore(string snow){
	int ptr = 0;
	while(snow[ptr] == ' ' || snow[ptr] == '\t') ptr++;
	if(ptr == snow.length())
		return true;
	else if(snow[ptr] == '/' && snow[ptr+1] == '/')
		return true;
	else return false;
}
class CodeWriter{
	string file_name;
	ofstream fout;
//	friend class Parser;
	stack <int> sk;
	map <int,int> mp;
	int nstatic;
public:
	CodeWriter(){
		nstatic = 16;
	}
//	CodeWriter &operator = (const CodeWriter &tmp){
//		file_name = tmp.file_name;
//		fout.open(file_name);
//		nstatic = tmp.nstatic;
//	}
	void setFileName(string fname){
		file_name = fname;	
		fout.open(file_name.c_str());
	}
	void writeArithmetic(string command){
//		cout << "11" << endl;
		if(strcmp(command.c_str(),"add") == 0){
			fout << "//add" << endl;
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M+D" << endl;
		}
		else if(strcmp(command.c_str(),"sub") == 0){
			fout << "//sub" << endl;
			fout << "@SP\nA=M-1\nD=-M\n@SP\nM=M-1\nA=M-1\nM=M+D" << endl;
		}
		else if(strcmp(command.c_str(),"neg") == 0){
			fout << "//neg" << endl;
			fout << "@SP\nA=M-1\nM=-M" << endl;
		}
		else if(strcmp(command.c_str(),"eq") == 0){
			int a = sk.top();
			sk.pop();
			int b = sk.top();
			sk.pop();
			fout << "//eq" << endl;
			if(a == b){
				fout << "@SP\nM=M-1\nA=M-1\nM=-1" << endl;
				sk.push(-1);
			}
			else{
				fout << "@SP\nM=M-1\nA=M-1\nM=0" << endl;
				sk.push(0);
			}
		}
		else if(strcmp(command.c_str(),"gt") == 0){
			int a = sk.top();
			sk.pop();
			int b = sk.top();
			sk.pop();
			fout << "//gt" << endl;
			if(a < b){
				fout << "@SP\nM=M-1\nA=M-1\nM=-1" << endl;
				sk.push(-1);
			}
			else{
				fout << "@SP\nM=M-1\nA=M-1\nM=0" << endl;
				sk.push(0);
			}			
		}
		else if(strcmp(command.c_str(),"lt") == 0){
			int a = sk.top();
			sk.pop();
			int b = sk.top();
			sk.pop();
			fout << "//lt" << endl;
			if(a > b){
				fout << "@SP\nM=M-1\nA=M-1\nM=-1" << endl;
				sk.push(-1);
			}
			else{
				fout << "@SP\nM=M-1\nA=M-1\nM=0" << endl;
				sk.push(0);
			}			
		}
		else if(strcmp(command.c_str(),"and") == 0){
			fout << "//and" << endl;
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M&D" << endl;
		}
		else if(strcmp(command.c_str(),"or") == 0){
			fout << "//or" << endl;
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M|D" << endl;
		}
		else if(strcmp(command.c_str(),"not") == 0){
			fout << "//not" << endl;
			fout << "@SP\nA=M-1\nM=!M" << endl;
		}
		else{
			printf("ERROR in writeArithmetic\n");
		}
	}
	void writePushPop(string command, string segment, int index){
//		cout << "11" << endl;
		if(strcmp(command.c_str(),"C_PUSH") == 0){
			if(segment == "argument"){
				sk.push(RAM[ARG+index]);
				fout << "//push argument " << index << endl;
				fout << "@" << index << "\nD=A\n@ARG\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "local"){
				sk.push(RAM[LCL+index]);
				fout << "//push local " << index << endl;
				fout << "@" << index << "\nD=A\n@LCL\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "static"){
				fout << "//push static " << index << endl;
				string ttmp;
				int pt;
				for(pt = file_name.length()-1; pt > 0; pt--) 
					if(file_name[pt] == '/')
						break;
				if(pt != 0)		
					ttmp = file_name.substr(pt+1, file_name.length());
				fout << "@" << ttmp << "." << index << "\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				sk.push(RAM[mp[index]]);
			}
			else if(segment == "constant"){
				sk.push(index);
				fout << "//push constant " << index << endl;
				fout << "@" << index << "\nD=A" << "\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "this"){
				sk.push(RAM[THIS+index]);
				fout << "//push this " << index << endl;
				fout << "@" << index << "\nD=A\n@THIS\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "that"){
				sk.push(RAM[THAT+index]);
				fout << "//push that " << index << endl;
				fout << "@" << index << "\nD=A\n@THAT\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
			else if(segment == "pointer"){
				fout << "//push pointer " << index << endl;
				if(index == 0){
					sk.push(RAM[THIS]);				
					fout << "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				}
				else if(index == 1){
					sk.push(RAM[THAT]);
					fout << "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				}
				else printf("ERROR writeArithmetic pointer");
			}
			else if(segment == "temp"){
				sk.push(RAM[5+index]);
				fout << "//push temp " << index << endl;
				fout << "@5\nD=A\n@" << index << "\nD=D+A\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
			}
		}
		else if(strcmp(command.c_str(),"C_POP") == 0){
			if(segment == "argument"){
				RAM[ARG+index] = sk.top();
				sk.pop();
				fout << "//pop argument " << index << endl;
				fout << "@" << index << "\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "local"){
				RAM[LCL+index] = sk.top();
				sk.pop();
				fout << "//pop local " << index << endl;
				fout << "@" << index << "\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "static"){
				string ttmp;
				int pt;
				for(pt = file_name.length()-1; pt > 0; pt--)
					if(file_name[pt] == '/')
						break;
				if(pt != 0)
					ttmp = file_name.substr(pt+1,file_name.length());
				fout << "//pop static " << index << endl;
				fout << "@SP\nM=M-1\nA=M\nD=M\n" <<"@" << ttmp << "." << index << "\nM=D" << endl;
				if(mp.find(index) == mp.end())
					mp[index] = nstatic++;
				RAM[mp[index]] = sk.top();
				sk.pop();
			}
//			else if(segment == "constant"){
//			
//			}
			else if(segment == "this"){
				RAM[THIS+index] = sk.top();
				sk.pop();
				fout << "//pop this " << index << endl;
				fout << "@" << index << "\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "that"){
				RAM[THAT+index] = sk.top();
				sk.pop();
				fout << "//pop that " << index << endl;
				fout << "@" << index << "\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}
			else if(segment == "pointer"){
				fout << "//pop pointer " << index << endl;
				if(index == 0){
					RAM[THIS] = sk.top();
					sk.pop();
					fout << "@SP\nM=M-1\nA=M\nD=M\n@3\nM=D" << endl;
				}
				else if(index == 1){
					RAM[THAT] = sk.top();
					sk.pop();
					fout << "@SP\nM=M-1\nA=M\nD=M\n@4\nM=D" << endl;
				}
				else{
					printf("ERROR in writePop pointer");
				}
			}
			else if(segment == "temp"){
				RAM[5+index] = sk.top();
				sk.pop();
				fout << "//pop temp " << index << endl;
				fout << "@" << index << "\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
			}			
		}
	}
	void writeEnd(){
		fout << "0;JMP\n" << endl;
	}
	void Close(){
//		writeEnd();
		fout.close();
		while(!sk.empty()) sk.pop();
	}
};
class Parser{
	string file_name;
	string snow,sfuture;
//	friend class CodeWriter;
	CodeWriter cw;
	ifstream fin;	
public:
	Parser(string fname){
		file_name = fname;
		fin.open(file_name.c_str());
		char out_file[100];
		sscanf(file_name.c_str(),"%[^.]",out_file);
		strcat(out_file,".asm");
//		cout << out_file << endl;		
		cw.setFileName(out_file);
	}
	~Parser(){
		fin.close();
		cw.Close();	
	}
	bool hasMoreCommands(){
		if(!getline(fin,sfuture))
			return false;
		else{
//			cout << "11" << endl;
	 		return true;		
		}
	}
	void advance(){
		string command,segment;
		int index;
		while(hasMoreCommands()){
			snow = sfuture;
			if(Isignore(snow)){
				continue;
			}
			else if(strcmp(commandType().c_str(),"C_PUSH") == 0){
//				cout << "11" << endl;
				command = "C_PUSH";
				segment = arg1();
				index = Arg2();
				cw.writePushPop(command, segment, index);
			}
			else if(strcmp(commandType().c_str(),"C_POP") == 0){
//				cout << "22" << endl;
				command = "C_POP";
				segment = arg1();
				index = Arg2();	
				cw.writePushPop(command, segment, index);			
			}
			else if(strcmp(commandType().c_str(),"C_ARITHMATIC") == 0){
//				cout << "33" << endl;
				char stmp[100];
				sscanf(snow.c_str(),"%s",stmp);
				command = stmp;
				cw.writeArithmetic(command);				
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
		if(strcmp(stmp,"push") == 0)
			return "C_PUSH";
		else if(strcmp(stmp,"pop") == 0)
			return "C_POP";		
		else if(strcmp(stmp,"add") == 0 ||
				strcmp(stmp,"sub") == 0 ||
				strcmp(stmp,"neg") == 0 ||
				strcmp(stmp,"eq") == 0 ||
				strcmp(stmp,"gt") == 0 ||
				strcmp(stmp,"lt") == 0 ||
				strcmp(stmp,"and") == 0 ||
				strcmp(stmp,"or") == 0 ||
				strcmp(stmp,"not") == 0)
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
//int main(){
//	freopen("BasicTest.vm","r",stdin);
//	CodeWriter cw;
	for(int i = 0; i < argc - 1; i++){
//		cout << *(argv+i+1) << endl;
		Parser tpr(*(argv+i+1));
//		Parser tpr("PointerTest.vm");
		tpr.advance();
	}
	return 0;
}
