#include <iostream>
#include <string>
using namespace std;
int main(){
	string file_name = "C:\\Users\\goldfish\\Desktop\\nand2tetris\\projects\\08\\FunctionCalls\\StaticsTest";
	file_name = file_name + "\\";
	char out_file[500];
	sscanf(file_name.c_str(),"%[^.]",out_file);  // cut the .vm
	cout << out_file << endl;
	return 0;
}
