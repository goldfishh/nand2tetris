// ---------find_label----------
// linux window \  / 替换  不兼容 
#include <dirent.h>
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <string>
#include <fstream>
#include <stack>
#include <vector>
#include <map>
//#include "sys/io.h"
#define SP 0
#define LCL 1
#define ARG 2
#define THIS 3
#define THAT 4
using namespace std;
vector <string>::iterator it;
bool Isignore(string snow){
	unsigned int ptr = 0;
	while(snow[ptr] == ' ' || snow[ptr] == '\t') ptr++;
	if(ptr == snow.length())
		return true;
	else if(snow[ptr] == '/' && snow[ptr+1] == '/')
		return true;
	else return false;
}

void listFiles(const char * _dir,vector <string> &vm)  
{  
    DIR* dir = opendir(_dir);//打开指定目录  
    dirent* p = NULL;//定义遍历指针  
    while((p = readdir(dir)) != NULL)//开始逐个遍历  
    {  
        //这里需要注意，linux平台下一个目录中有"."和".."隐藏文件，需要过滤掉  
        int length = strlen(p->d_name);
        if(p->d_name[length-3] == '.' && p->d_name[length-2] == 'v' && p->d_name[length-1] == 'm')//d_name是一个char数组，存放当前遍历到的文件名  
        {                            // find_label
//            string name = "/home/hanchao/picture/" + string(p->d_name); 
				vm.push_back(string(p->d_name)); 
//            cout<<string(p->d_name)<<endl;  
        }  
    }  
    closedir(dir);//关闭指定目录  
}  
// ------------linux error   no such file io.h -----------------------
//void listFiles(const char * dir,vector <string> &vm)  //目录末尾必须是'\' 
//{
//    intptr_t handle;
//    _finddata_t findData;  //_finddata_t 结构体变量 
//
//    handle = _findfirst(dir, &findData);    // 查找目录中的第一个文件
//    if (handle == -1){
//        cout << "Failed to find first file!\n";
//        return;
//    }
//    do{
//        vm.push_back(findData.name);
//    } while (_findnext(handle, &findData) == 0);    // 查找目录中的下一个文件
////    vector <string>::iterator it;
////	for(it = vm.begin();it != vm.end(); it++){
////    	cout << *it << endl;
////    }
//    _findclose(handle);    // 关闭搜索句柄
//}

class CodeWriter{
	string file_name;
	ofstream fout;
	map <int,int> mp;
	int nstatic;
	int func_num;
	int line_num;
public:
	CodeWriter(){
		nstatic = 16;
		func_num = 0;
		line_num = 0;
	}
	void setFileName(string fname,bool flag){
		file_name = fname;	
		fout.open(file_name.c_str());
		if(flag == true) //flag is or is not a dir
			writeInit();
	}
	void writeInit(){
		fout << "@256\nD=A\n@SP\nM=D" << endl;
//		cout << file_name << endl;
//		fout << "@5\nD=A\n@R14\nM=D" << endl;
		line_num += 4;
		writeCall("Sys.init",0);
	}	
	void writeArithmetic(string command){
//		cout << "test" << endl;
		if(strcmp(command.c_str(),"add") == 0){
			fout << "//add" << endl;
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M+D" << endl;
			line_num += 7;
		}
		else if(strcmp(command.c_str(),"sub") == 0){
			fout << "//sub" << endl;
			fout << "@SP\nA=M-1\nD=-M\n@SP\nM=M-1\nA=M-1\nM=M+D" << endl;
			line_num += 7;
		}
		else if(strcmp(command.c_str(),"neg") == 0){
			fout << "//neg" << endl;
			fout << "@SP\nA=M-1\nM=-M" << endl;
			line_num += 3;
		}
		else if(strcmp(command.c_str(),"eq") == 0){
			fout << "//eq" << endl;
			fout << "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D" << endl;
			fout << "@EQ_-1\nD,JEQ" << endl; 
			fout << "(EQ_0)\n@SP\nM=M+1\nA=M-1\nM=0\n@EQBJ\n0;JMP" << endl;
			fout << "(EQ_-1)\n@SP\nM=M+1\nA=M-1\nM=-1" << endl;
			fout << "(EQBJ)" << endl;
			line_num += 20;
		}
		else if(strcmp(command.c_str(),"gt") == 0){
			fout << "//gt" << endl;
			fout << "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D" << endl;
			fout << "@GT_-1\nD,JGT" << endl; 
			fout << "(GT_0)\n@SP\nM=M+1\nA=M-1\nM=0\n@GTBJ\n0;JMP" << endl;
			fout << "(GT_-1)\n@SP\nM=M+1\nA=M-1\nM=-1" << endl;
			fout << "(GTBJ)" << endl;			
			line_num += 20;			
		}
		else if(strcmp(command.c_str(),"lt") == 0){
			fout << "//lt" << endl;
			fout << "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D" << endl;
			fout << "@LT_-1\nD,JLT" << endl; 
			fout << "(LT_0)\n@SP\nM=M+1\nA=M-1\nM=0\n@LTBJ\n0;JMP" << endl;
			fout << "(LT_-1)\n@SP\nM=M+1\nA=M-1\nM=-1" << endl;
			fout << "(LTBJ)" << endl;				
			line_num += 20;			
		}
		else if(strcmp(command.c_str(),"and") == 0){
			fout << "//and" << endl;
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M&D" << endl;
			line_num += 7;
		}
		else if(strcmp(command.c_str(),"or") == 0){
			fout << "//or" << endl;
			fout << "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M|D" << endl;
			line_num += 7;
		}
		else if(strcmp(command.c_str(),"not") == 0){
			fout << "//not" << endl;
			fout << "@SP\nA=M-1\nM=!M" << endl;
			line_num += 3;
		}
		else{
			printf("ERROR in writeArithmetic\n");
		}
	}
	void writePushPop(string command, string segment, int index){
//		cout << "11" << endl;
		if(strcmp(command.c_str(),"C_PUSH") == 0){
			if(segment == "argument"){
				fout << "//push argument " << index << endl;
				fout << "@" << index << "\nD=A\n@ARG\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 10;
			}
			else if(segment == "local"){
				fout << "//push local " << index << endl;
				fout << "@" << index << "\nD=A\n@LCL\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 10;
			}
			else if(segment == "static"){
				fout << "//push static " << index << endl;
				fout << "@" << *it << "." << index << "\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 6;
			}
			else if(segment == "constant"){
				fout << "//push constant " << index << endl;
				fout << "@" << index << "\nD=A" << "\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 6;
			}
			else if(segment == "this"){
				fout << "//push this " << index << endl;
				fout << "@" << index << "\nD=A\n@THIS\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 10;
			}
			else if(segment == "that"){
				fout << "//push that " << index << endl;
				fout << "@" << index << "\nD=A\n@THAT\nD=D+M\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 10;
			}
			else if(segment == "pointer"){
				fout << "//push pointer " << index << endl;
				if(index == 0){			
					fout << "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
					line_num += 6;
				}
				else if(index == 1){
					fout << "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
					line_num += 6;
				}
				else printf("ERROR writeArithmetic pointer");
			}
			else if(segment == "temp"){
				fout << "//push temp " << index << endl;
				fout << "@5\nD=A\n@" << index << "\nD=D+A\nA=D\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
				line_num += 10;
			}
		}
		else if(strcmp(command.c_str(),"C_POP") == 0){
			if(segment == "argument"){
				fout << "//pop argument " << index << endl;
				fout << "@" << index << "\nD=A\n@ARG\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
				line_num += 13;
			}
			else if(segment == "local"){
				fout << "//pop local " << index << endl;
				fout << "@" << index << "\nD=A\n@LCL\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
				line_num += 13;
			}
			else if(segment == "static"){
				fout << "//pop static " << index << endl;
				fout << "@SP\nM=M-1\nA=M\nD=M\n" <<"@" << *it << "." << index << "\nM=D" << endl;
				line_num += 6;
				if(mp.find(index) == mp.end())
					mp[index] = nstatic++;
			}
//			else if(segment == "constant"){
//			
//			}
			else if(segment == "this"){
				fout << "//pop this " << index << endl;
				fout << "@" << index << "\nD=A\n@THIS\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
				line_num += 13;
			}
			else if(segment == "that"){
				fout << "//pop that " << index << endl;
				fout << "@" << index << "\nD=A\n@THAT\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
				line_num += 13;
			}
			else if(segment == "pointer"){
				fout << "//pop pointer " << index << endl;
				if(index == 0){
					fout << "@SP\nM=M-1\nA=M\nD=M\n@3\nM=D" << endl;
					line_num += 6;
				}
				else if(index == 1){
					fout << "@SP\nM=M-1\nA=M\nD=M\n@4\nM=D" << endl;
					line_num += 6;
				}
				else{
					printf("ERROR in writePop pointer");
				}
			}
			else if(segment == "temp"){
				fout << "//pop temp " << index << endl;
				fout << "@" << index << "\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D" << endl;
				line_num += 13;
			}			
		}
	}
	void writeLabel(string label){
		fout << "//label " << label << endl;
		fout << "(" << label << ")" << endl;
	}	
	void writeGoto(string label){
		fout << "//goto " << label << endl;
		fout << "@" << label << "\n0;JMP" << endl;
		line_num += 2;
	}
	void writeIf(string label){
		fout << "//if-goto " << label << endl;
		fout << "@SP\nM=M-1\nA=M\nD=M\n@" << label << "\nD;JNE" << endl;
		line_num += 6;
	}	
	void writeCall(string functionName,int numArgs){
		fout << "//call " << functionName << " " << numArgs << endl; 
		char func_num_str[100];
		sprintf(func_num_str,"%d",func_num);
		char tmp_s[100] = "return-address-";
		strcat(tmp_s,func_num_str);
		strcpy(func_num_str,tmp_s);
		func_num++;
		int return_address = line_num + 44;
		fout << "@" << return_address << "\n" << "D=A\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
//		writePushPop("C_PUSH","constant",RAM[LCL]);
		fout << "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
//		writePushPop("C_PUSH","constant",RAM[ARG]);
		fout << "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
//		writePushPop("C_PUSH","constant",RAM[THIS]);
		fout << "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
//		writePushPop("C_PUSH","constant",RAM[THAT]);
		fout << "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D" << endl;
		fout << "@SP\nD=M\n@" << numArgs << "\nD=D-A\n@5\nD=D-A\n@ARG\nM=D" << endl;
		fout << "@SP\nD=M\n@LCL\nM=D" << endl;	
		writeGoto(functionName);
		writeLabel(func_num_str);
		line_num += 42;
	}	
	void writeReturn(){
		fout << "//return" << endl; 
		fout << "@LCL\nD=M\n@R14\nM=D\n";  //R14 = FNAME
		fout << "@5\nD=D-A\nA=D\nD=M\n@R15\nM=D" << endl;  //R15 = *(FNAME - 5)
		fout << "@SP\nM=M-1\nA=M\nD=M\n@R13\nM=D" << endl; //R13 = pop()
		line_num += 16;
		fout << "@ARG\nD=M+1\n@SP\nM=D" << endl;
		fout << "@R13\nD=M\n@SP\nA=M-1\nM=D" << endl;
		fout << "@R14\nM=M-1\nA=M\nD=M\n@THAT\nM=D" << endl;
		line_num += 15;
		fout << "@R14\nM=M-1\nA=M\nD=M\n@THIS\nM=D" << endl;
		fout << "@R14\nM=M-1\nA=M\nD=M\n@ARG\nM=D" << endl;
		line_num += 12;
		fout << "@R14\nM=M-1\nA=M\nD=M\n@LCL\nM=D" << endl;
		fout << "@R15\nD=M\nA=D\n0;JMP" << endl;
		line_num += 10;
	}
	void writeFunction(string functionName,int numLocals){
		fout << "//function " << functionName << " " << numLocals << endl;
		fout << "(" << functionName << ")" << endl;
		for(int i = 0; i < numLocals; i++){
			 writePushPop("C_PUSH", "constant", 0);
		}
	}
	void writeEnd(){
		fout << "(END)\n@END\n0;JMP\n" << endl;
		line_num += 2;
	}
	void Close(){
		writeEnd();
		fout.close();
		mp.clear();
	}
};
class Parser{
	string file_name;
	string dir_name;
	vector<string> vm; 
	friend class CodeWriter;
	string snow,sfuture;
	bool multi_flag;
	CodeWriter cw;
//	int line_num;
	ifstream fin;	
public:
	Parser(string fname){
		multi_flag = true;
//		line_num = 0;
		for(unsigned int i = 0; i < fname.length(); i++)
			if(fname[i] == '.' && fname[i+1] == 'v' && fname[i+2] == 'm')
				multi_flag = false;
		if(!multi_flag){
			file_name = fname;
			fin.open(file_name.c_str());
			char out_file[500];
			sscanf(file_name.c_str(),"%[^.]",out_file);  // cut the .vm
			strcat(out_file,".asm");
	//		cout << out_file << endl;		
			cw.setFileName(out_file,false);			
		}
		else{
			dir_name = fname; 
			string re = dir_name;
//			cout << re << endl;
			listFiles(re.c_str(),vm);   //vector vm;
		}
	}
	~Parser(){
		vm.clear();
		fin.close();
		cw.Close();	
	}
	bool hasMoreCommands(){
		if(!getline(fin,sfuture))
			return false;
		else
	 		return true;		
	}
	void judge_advance(){
		if(!multi_flag){
			advance();
		}
		else{
			int ptr = dir_name.length() - 1;
			for(; ptr > 0; ptr--){
				if(dir_name[ptr] == '\\')             // find_label
					break;
			}
			string sub_dir_name = dir_name.substr(ptr,dir_name.length());
			if(ptr != 0)
				cw.setFileName(dir_name+sub_dir_name+".asm",true);
			else
				cw.setFileName(dir_name+"\\"+sub_dir_name+".asm",true);  // find_label
			for(it = vm.begin(); it != vm.end(); it++){
				string now_file = dir_name + "\\" + *it;          // find_label
				cout << now_file << endl;
				fin.open(now_file.c_str());
				advance();
				fin.close();
			}
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
			else if(strcmp(commandType().c_str(),"C_LABEL") == 0){
				char stmp[100];
				sscanf(snow.c_str(),"%*s%*[^a-zA-Z0-9_]%s",stmp);
				cw.writeLabel(stmp);
			}
			else if(strcmp(commandType().c_str(),"C_GOTO") == 0){
				char stmp[100];
				sscanf(snow.c_str(),"%*s%*[^a-zA-Z0-9_]%s",stmp);
				cw.writeGoto(stmp);				
			}
			else if(strcmp(commandType().c_str(),"C_IF") == 0){
				char stmp[100];
				sscanf(snow.c_str(),"%*s%*[^a-zA-Z0-9_]%s",stmp);
				cw.writeIf(stmp);				
			}
			else if(strcmp(commandType().c_str(),"C_FUNCTION") == 0){
				char stmp[100],tint[100];
				int nval;
				sscanf(snow.c_str(),"%*s%*[ ]%s",stmp);
				sscanf(snow.c_str(),"%*s%*[ ]%*s%*[ ]%s",tint);
				nval = atoi(tint);
				cw.writeFunction(stmp,nval);
			}
			else if(strcmp(commandType().c_str(),"C_RETURN") == 0){
				cw.writeReturn();
			}
			else if(strcmp(commandType().c_str(),"C_CALL") == 0){
				char stmp[100],tint[100];
				int nval;
				sscanf(snow.c_str(),"%*s%*[ ]%s",stmp);
				sscanf(snow.c_str(),"%*s%*[ ]%*s%*[ ]%s",tint);
				nval = atoi(tint);
				cw.writeCall(stmp,nval);				
			}												
			else printf("ERROR in advance\n");
		}			
	}
	string commandType(){ // generally is a command
		char stmp[100];
		int ptr = 0,end = snow.length();
		while(!isalpha(snow[ptr])) ptr++;
		snow = snow.substr(ptr, end);  //cut former blank characters
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
		else if(strcmp(stmp,"label") == 0)
			return "C_LABEL";
		else if(strcmp(stmp,"goto") == 0)
			return "C_GOTO";
		else if(strcmp(stmp,"if-goto") == 0)
			return "C_IF";
		else if(strcmp(stmp,"function") == 0)
			return "C_FUNCTION";		
		else if(strcmp(stmp,"return") == 0)
			return "C_RETURN";
		else if(strcmp(stmp,"call") == 0)
			return "C_CALL";
		else{
			printf("ERROR in commandType\n");
			return "ERROR";
		}
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
		else{
			printf("ERROR Arg2");
			return -1;
		}
	}
};

int main(int argc,char *argv[]){
//int main(){
	for(int i = 0; i < argc - 1; i++){
//		cout << *(argv+i+1) << endl;
		Parser tpr(*(argv+i+1));
//		Parser tpr("C:\\Users\\goldfish\\Desktop\\nand2tetris\\projects\\08\\FunctionCalls\\StaticsTest");
		tpr.judge_advance();
	}
	return 0;
}

