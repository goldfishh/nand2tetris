#include <iostream>
#include <fstream>
#include <string>
using namespace std;
class JackTokenizer{
private:	
	ifstream fin;
	string now_word,now_token;
	int now_ptr;
public:	
	// file = *.jack
	JackTokenizer(string file){
		fin.open(file.c_str());
		now_word = "";
		now_token = "";
	}
	bool hasMoreTokens(string &tmp){
		fin >> tmp;
		return tmp != "";
	}
	void advance(){
		while(hasMoreTokens(now_word)){
			
		}
	}
	string tokenType(){
		//KEYWORD
		
		//SYMBOL
		
		//IDENTIFIER
		
		//INT_CONST
		
		//STRING_CONST
		
	}
	string keyword(){
		//CLASS
		
		//METHOD
		
		//INT
		
		//FUNCTION
		
		//BOOLEAN
		
		//CONSTRUCTOR
		
		//CHAR
		
		//VOID
		
		//VAR
		
		//STATIC
		
		//FIELD
		
		//LET
		
		//DO
		
		//IF
		
		//ELSE
		
		//WHILE
		
		//RETURN
		
		//TRUE
		
		//FALSE
		
		//NULL
		
		//THIS
	}
	char symbol(){
		
	} 
	string identifier(){
		
	}
	int intVal(){
		
	}
	string stringVal(){
		
	}
	
};

class JackAnalyzer{
	
	
};

class CompilationEngine{
	
};

int main(int argc,char *argv[]){
//	freopen("datain","r",stdin);
	
	return 0;
}
