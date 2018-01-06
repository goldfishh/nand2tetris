import re
import sys
import os
class JackTokenizer:
	def __init__(self,file):
		fin = open(file,"r")
		self.contents = fin.read()
		#preprocessing
		self.fout_name = re.sub(r'\.jack',"",file)
		# self.fout = open(self.fout_name,"w")
		# self.fout.write("<tokens>\n")
		self.contents = re.sub(r'\/\/[^\n]*',"",self.contents)
		self.contents = re.sub(r'\/\*\*[\d\D]*?\*\/',"",self.contents)
		# print (contents)
		self.symbol_Table = ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]
		self.keywords_Table = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
		for s in self.symbol_Table:
			self.contents = self.contents.replace(s," "+s+" ")
		# print (contents)
		# self.word_list = contents.split()  string have bug!
		self.word_list = re.findall(r'(\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~|\".*\"|\d+|[\w_]+)',self.contents)
		self.token_iter = 0
		self.now_token = ""
	def __del__(self):
		# self.fout.write("</tokens>")
		# self.fout.close()
	def hasMoreTokens(self):
		if(self.token_iter < len(self.word_list)):
			return True
		else:
			return False
	def advance(self,symbolTable=None,id_type=None):
		if(self.hasMoreTokens()):
			self.now_token = self.word_list[self.token_iter]
			self.token_iter += 1;
			if(self.tokenType() == "KEYWORD"):
				tmp = self.keyword()
				# Cfout.write(" <keyword> "+tmp+" </keyword>\n")
			elif(self.tokenType() == "SYMBOL"):
				tmp = self.symbol()
				# Cfout.write(" <symbol> ")
				if(tmp == "<"):
					# Cfout.write("&lt;")
				elif(tmp == ">"):
					# Cfout.write("&gt;")
				elif(tmp == "\""):
					# Cfout.write("&quot;")
				elif(tmp == "&"):
					# Cfout.write("&amp;")
				else:
					# Cfout.write(tmp)
				# Cfout.write(" </symbol>\n")
			elif(self.tokenType() == "INT_CONST"):
				tmp = str(self.intVal())
				# Cfout.write(" <integerConstant> "+tmp+" </integerConstant>\n")
			elif(self.tokenType() == "STRING_CONST"):
				tmp = self.stringVal()
				# Cfout.write(" <stringConstant> "+tmp+" </stringConstant>\n")
			elif(self.tokenType() == "IDENTIFIER"):
				tmp = self.identifier()
				# Cfout.write(" <identifier>\n")
				# Cfout.write("  <"+id_type+">\n")
				# 变量是否定义
				if(symbolTable.KindOf(tmp) == "NONE"):
					# Cfout.write("   <Undefined></Undefined>\n")
				else:
					# Cfout.write("   <Defined></Defined>\n")
				# 变量是否已使用
				if(symbolTable.HaveBeenUsed(tmp) == True):
					# Cfout.write("   <Used></Used>\n")
				elif(symbolTable.HaveBeenUsed(tmp) == False):
					# Cfout.write("   <Unused></Unused>\n")
				# 变量是否有索引
				if(id_type == "VAR" or id_type == "ARG" or id_type == "STATIC" or id_type == "FIELD"):
					# Cfout.write("   <Index>"+symbolTable.IndexOf(tmp)+"</Index>\n")

				# Cfout.write("   "+tmp+"\n</"+id_type+">\n")
				# Cfout.write(" </identifier>\n")

	def tokenType(self):
		for kw in self.keywords_Table:
			if(self.now_token == kw):
				return "KEYWORD"
		for sb in self.symbol_Table:
			if(self.now_token == sb):
				return "SYMBOL"
		if(self.now_token.isdigit()):
			return "INT_CONST"
		if(self.now_token[0] == '\"'):
			return "STRING_CONST"
		if(re.match(r'[_A-Za-z][\w_]*',self.now_token) != None):
			return "IDENTIFIER"
	def LL1tokenType(self):
		LL1token = self.word_list[self.token_iter]
		for kw in self.keywords_Table:
			if(LL1token == kw):
				return "KEYWORD"
		for sb in self.symbol_Table:
			if(LL1token == sb):
				return "SYMBOL"
		if(LL1token.isdigit()):
			return "INT_CONST"
		if(LL1token[0] == '\"'):
			return "STRING_CONST"
		if(re.match(r'[_A-Za-z][\w_]*',LL1token) != None):
			return "IDENTIFIER"				
	def keyword(self):
		for kw in self.keywords_Table:
			if(self.now_token == kw):
				return kw
	def symbol(self):
		for sb in self.symbol_Table:
			if(self.now_token == sb):
				return sb
	def identifier(self):
		return self.now_token
	def intVal(self):
		return self.now_token
	def stringVal(self):
		return self.now_token[1:len(self.now_token)-1]


class CompilationEngine:
	def __init__(self,obj):
		# self.fout_name = obj.fout_name
		# self.fout_name = re.sub(r'T\.xml','.xml',obj.fout_name)
		# self.fout = open(self.fout_name,"w")
		self.file_name = obj.fout_name
		self.fout_name = self.file_name + ".vm"
		self.vmwriter = VMWriter(self.fout_name)
		self.tokenizer = obj
		self.symbolTable = SymbolTable()
	def __del__(self):
		# self.fout.close()
	def CompileClass(self):
		#self.num += 1
		# self.fout.write("<class>\n")
		self.tokenizer.advance()  # 'class'
		self.tokenizer.advance()  # className
		self.tokenizer.advance()  # '{'
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == 'static' or self.tokenizer.word_list[self.tokenizer.token_iter] == 'field' ):
			self.CompileClassVarDec()
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == 'constructor' or self.tokenizer.word_list[self.tokenizer.token_iter] == 'function' or self.tokenizer.word_list[self.tokenizer.token_iter] == 'method' ):
			self.CompileSubroutine()	
		self.tokenizer.advance()  # '}'
		# self.fout.write("</class>")	
	def CompileClassVarDec(self):
		# self.fout.write("<classVarDec>\n")
		_kind = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  # ('static'|'field')
		_type = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  # type
		if(_kind == 'static'):
			_kind = "STATIC"
		elif(_kind == 'field'):
			_kind = "FIELD"
		_name = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  # varName
		self.symbolTable.Define(_name,_type,_kind)
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == ','):
			self.tokenizer.advance()  # ','
			_name = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  # varName
			self.symbolTable.Define(_name,_type,_kind)
		self.tokenizer.advance()  # ';'
		# self.fout.write("</classVarDec>\n")	
	def CompileSubroutine(self):
		# self.fout.write("<subroutineDec>\n")	
		self.symbolTable.startSubroutine()
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == 'method'):
			self.symbolTable.Define("this",self.file_name,"ARG")
		self.tokenizer.advance()  # ('constructor'|'function'|'method')
		self.tokenizer.advance()  # ('void'|type)
		_subroutineName = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  # subroutineName
		self.tokenizer.advance()  # '('
		_num = self.CompileParameterList()
		self.tokenizer.advance()  # ')'
		self.CompileSubroutineBody()
		_name = self.file_name + "." + _subroutineName
		self.vmwriter.writeFunction(_name,_num)
		# self.fout.write("</subroutineDec>\n")	
	def CompileSubroutineBody(self):
		# self.fout.write("<subroutineBody>\n")
		self.tokenizer.advance()  # {
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == "var"):
			self.CompileVarDec()
		self.CompileStatements()
		self.tokenizer.advance() # }
		# self.fout.write("</subroutineBody>\n")	

	def CompileParameterList(self):
		# self.fout.write("<parameterList>\n")
		_num = 0
		if(self.tokenizer.word_list[self.tokenizer.token_iter] != ")"):
			_type = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  #type
			_name = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  #varName
			self.symbolTable.Define(_name,_type,"ARG")
			_num += 1
			while(self.tokenizer.word_list[self.tokenizer.token_iter] == ","):
				 self.tokenizer.advance()  #,
				 _type = self.tokenizer.word_list[self.tokenizer.token_iter]
				 self.tokenizer.advance()  #type
				 _name = self.tokenizer.word_list[self.tokenizer.token_iter]
				 self.tokenizer.advance()  #varName
				 self.symbolTable.Define(_name,_type,"ARG")
				 _num += 1
		return _num
		# self.fout.write("</parameterList>\n")
	def CompileVarDec(self):
		# self.fout.write("<varDec>\n")
		self.tokenizer.advance()  #var
		_type = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  #type
		_name = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  #varName
		self.symbolTable.Define(_name,_type,"VAR")
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == ","):
			self.tokenizer.advance()  #,
			_name = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  #varName
			self.symbolTable.Define(_name,_type,"VAR")
		self.tokenizer.advance()  #;
		# self.fout.write("</varDec>\n")
	def CompileStatements(self):
		# self.fout.write("<statements>\n")
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == "let" or self.tokenizer.word_list[self.tokenizer.token_iter] == "if" or self.tokenizer.word_list[self.tokenizer.token_iter] == "while" or self.tokenizer.word_list[self.tokenizer.token_iter] == "do" or self.tokenizer.word_list[self.tokenizer.token_iter] == "return"):
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == "let"):
				self.CompileLet()
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == "if"):
				self.CompileIf()
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == "return"):
				self.CompileReturn()
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == "while"):
				self.CompileWhile()				
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == "do"):
				self.CompileDo()
		# self.fout.write("</statements>\n")		
	def CompileDo(self):
		# self.fout.write("<doStatement>\n")
		self.tokenizer.advance()  #'do'
		#subroutineCall
		_name = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  #subroutineName or className or varName
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == "."):
			if(self.symbolTable.TypeOf(_name) != "NONE"):
				_name = self.symbolTable.TypeOf(_name)
			self.tokenizer.advance()  # '.'
			_name = _name + "." +self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  # subroutineName		
			self.tokenizer.advance()  # '('
			_num = self.CompileExpressionList()
			self.tokenizer.advance()  # ')'
			self.tokenizer.advance()  # ';'
			self.vmwriter.writeCall(_name,_num)
		else:
			_name = self.file_name + "." + _name
			self.tokenizer.advance()  # '('
			_num = self.CompileExpressionList()
			self.tokenizer.advance()  # ')'
			self.tokenizer.advance()  # ';'	
			self.vmwriter.writeCall(_name,_num)	
		# self.fout.write("</doStatement>\n")

	def CompileLet(self):
		# self.fout.write("<letStatement>\n")
		self.tokenizer.advance()  #'let'	
		_name = self.tokenizer.word_list[self.tokenizer.token_iter]
		_kind = self.symbolTable.KindOf(_name)
		self.tokenizer.advance()  # varName
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == "["):
			self.tokenizer.advance()  # '['
			self.CompileExpression()
			self.tokenizer.advance()  # ']'
		self.tokenizer.advance()  # '='
		self.CompileExpression()
		self.tokenizer.advance()  # ';'
		# self.fout.write("</letStatement>\n")	

	def CompileWhile(self):
		# self.fout.write("<whileStatement>\n")
		self.tokenizer.advance()  #'while'	
		self.tokenizer.advance()  # '('
		self.CompileExpression()
		self.tokenizer.advance()  # ')'
		self.tokenizer.advance()  # '{'
		self.CompileStatements()
		self.tokenizer.advance()  # '}'		
		# self.fout.write("</whileStatement>\n")	

	def CompileReturn(self):
		# self.fout.write("<returnStatement>\n")
		self.tokenizer.advance()  #'return'	
		if(self.tokenizer.word_list[self.tokenizer.token_iter] != ";"):
			self.CompileExpression()
		self.tokenizer.advance()  # ';'
		self.vmwriter.writeReturn()
		# self.fout.write("</returnStatement>\n")	

	def CompileIf(self):
		# self.fout.write("<ifStatement>\n")
		self.tokenizer.advance()  #'if'	
		self.tokenizer.advance()  # '('
		self.CompileExpression()
		self.tokenizer.advance()  # ')'
		self.tokenizer.advance()  # '{'
		self.CompileStatements()
		self.tokenizer.advance()  # '}'	
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == "else"):
			self.tokenizer.advance()  # "else"
			self.tokenizer.advance()  # '{'
			self.CompileStatements()
			self.tokenizer.advance()  # '}'						
		# self.fout.write("</ifStatement>\n")	

	def CompileExpression(self):
		# self.fout.write("<expression>\n")
		self.CompileTerm()
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == "+" or self.tokenizer.word_list[self.tokenizer.token_iter] == "-" or self.tokenizer.word_list[self.tokenizer.token_iter] == "*" or self.tokenizer.word_list[self.tokenizer.token_iter] == "/" or self.tokenizer.word_list[self.tokenizer.token_iter] == "&" or self.tokenizer.word_list[self.tokenizer.token_iter] == "|" or self.tokenizer.word_list[self.tokenizer.token_iter] == "<" or self.tokenizer.word_list[self.tokenizer.token_iter] == ">" or self.tokenizer.word_list[self.tokenizer.token_iter] == "="):
			_op = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  # op
			self.CompileTerm()
			self.writeArithmetic(_op)
		# self.fout.write("</expression>\n")	

	def CompileTerm(self):
		# self.fout.write("<term>\n")
		# self.tokenizer.now_token = self.tokenizer.word_list[self.tokenizer.token_iter]
		if(self.tokenizer.LL1tokenType() == "INT_CONST"):
			self.tokenizer.advance() # INT
			self.writePush("CONST",self.tokenizer.intVal())
		elif(self.tokenizer.LL1tokenType() == "STRING_CONST"):
			self.tokenizer.advance() # STRING
		elif(self.tokenizer.LL1tokenType() == "KEYWORD"):
			self.tokenizer.advance()  # 'true' or 'false' or 'null' or 'this'
		elif(self.tokenizer.LL1tokenType() == "IDENTIFIER"):
			if(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "+" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "-" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "*" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "/" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "&" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "|" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "<" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == ">" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "=" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "]" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == ")" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "," or self.tokenizer.word_list[self.tokenizer.token_iter+1] == ";"):
				_name = self.tokenizer.word_list[self.tokenizer.token_iter]
				_kind = self.symbolTable.KindOf(_name)				
				self.tokenizer.advance()  # varName
				if(self.symbolTable.KindOf(_name) == "VAR"):
					_segment = "LOCAL"
				elif(self.symbolTable.KindOf(_name) == "ARG"):
					_segment = "ARG"
				else:
					_segment = "ERROR"
				_index = self.symbolTable.IndexOf(_name)
				self.vmwriter.writePush(_segment,_index)
			elif(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "["):
				_name = self.tokenizer.word_list[self.tokenizer.token_iter]
				_kind = self.symbolTable.KindOf(_name)					
				self.tokenizer.advance()  # varName
				self.tokenizer.advance()  # '['
				self.CompileExpression()
				self.tokenizer.advance()  # ']'
				self.vmwriter.writePop("TEMP",0)
				self.vmwriter.writePush()
			elif(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "." or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "("):
				if(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "."):
					self.tokenizer.advance()  # ClassName or varName
					self.tokenizer.advance()  # '.'
				self.tokenizer.advance()  # subroutineName
				self.tokenizer.advance()  # '('
				self.CompileExpressionList()
				self.tokenizer.advance()  # ')'
		elif(self.tokenizer.word_list[self.tokenizer.token_iter] == "("):
			self.tokenizer.advance()  # '('
			self.CompileExpression()
			self.tokenizer.advance()  # ')'			
		elif(self.tokenizer.word_list[self.tokenizer.token_iter] == "-" or self.tokenizer.word_list[self.tokenizer.token_iter] == "~"):
			_flag = self.tokenizer.word_list[self.tokenizer.token_iter] == "-"
			self.tokenizer.advance()  # unaryOp
			self.CompileTerm()
			if(_flag):
				self.vmwriter.writeArithmetic("--")
			else:
				self.vmwriter.writeArithmetic("~")	
		# self.fout.write("</term>\n")	

	def CompileExpressionList(self):
		# self.fout.write("<expressionList>\n")
		_num = 0
		if(self.tokenizer.word_list[self.tokenizer.token_iter] != ")"):
			self.CompileExpression()
			_num += 1
			while(self.tokenizer.word_list[self.tokenizer.token_iter] == ","):
				self.tokenizer.advance()  #","
				self.CompileExpression()
				_num += 1
		# self.fout.write("</expressionList>\n")
		return _num	

class SymbolTable:
	def __init__(self):
		#self.varCount = 0
		self.Global_symbolTable = { }
		self.Local_symbolTable = { }
		self.static_num = 0
		self.field_num = 0
		self.argument_num = 0
		self.var_num = 0
	def __del__(self):
		self.Global_symbolTable.clear()
		self.Local_symbolTable.clear()

	def startSubroutine(self):
		self.Local_symbolTable.clear()

	def Define(self,_name,_type,kind):
		if(kind == "STATIC" or kind == "FIELD"):
			tmp = []
			tmp.append(_type)
			tmp.append(kind)
			if(kind == "STATIC"):
				tmp.append(self.static_num)
				self.static_num += 1
			elif(kind == "FIELD"):
				tmp.append(self.field_num)
				self.field_num += 1
			tmp.append(False)
			self.Global_symbolTable[_name] = tmp
		elif(kind == "ARG" or kind == "VAR"):
			tmp = []
			tmp.append(_type)
			tmp.append(kind)
			if(kind == "ARG"):
				tmp.append(self.argument_num)
				self.argument_num += 1
			elif(kind == "VAR"):
				tmp.append(self.var_num)
				self.var_num += 1
			tmp.append(False)
			self.Global_symbolTable[_name] = tmp	

	def VarCount(self,kind):
		if(kind == "STATIC"):
			return self.static_num
		elif(kind == "FIELD"):
			return self.field_num
		elif(kind == "ARG"):
			return self.argument_num
		elif(kind == "VAR"):
			return self.var_num

	def KindOf(self,_name):
		if(self.Local_symbolTable.get(_name)):
			return self.Local_symbolTable[_name][1]
		elif(self.Global_symbolTable.get(_name)):
			return self.Global_symbolTable[_name][1]
		else:
			return "NONE"

	def TypeOf(self,_name):
		if(self.Local_symbolTable.get(_name)):
			return self.Local_symbolTable[_name][0]
		elif(self.Global_symbolTable.get(_name)):
			return self.Global_symbolTable[_name][0]
		else:
			return "NONE"

	def IndexOf(self,_name):
		if(self.Local_symbolTable.get(_name)):
			return self.Local_symbolTable[_name][2]
		elif(self.Global_symbolTable.get(_name)):
			return self.Global_symbolTable[_name][2]
		else:
			return "NONE"

	def HaveBeenUsed(self,_name):
		if(self.Local_symbolTable.get(_name)):
			return self.Local_symbolTable[_name][3]
		elif(self.Global_symbolTable.get(_name)):
			return self.Global_symbolTable[_name][3]
		else:
			return "NONE"	

class VMWriter:
	def __init__(self,file):
		f = open(file,"w")

	def __del__(self):
		f.close()
	def writePush(self,segment,index):
		#segment = "CONST" or "ARG" or "LOCAL" or "STATIC" 
		#                  or "THIS" or "THAT" or "POINTER" or "TEMP"
		f.write("  push "+segment+" "+str(index)+"\n")
	def writePop(self,segment,index):
		f.write("  push "+segment+" "+str(index)+"\n")
	def writeArithmetic(self,command):
		#command = "ADD" or "SUB" or "NEG" or "EQ" or "GT" or 
		#          "LT" or "AND" or "OR" or "NOT"
		if(command == "+"):
			command = "add"
		elif(command == "-"):
			command = "sub"
		elif(command == "&"):
			command = "and"
		elif(command == "|"):
			command = "or"
		elif(command == "~"):
			command = "not"
		elif(command == "--"):
			command = "neg"
		elif(command == "eq"):
			command = "eq"
		elif(command == ">"):
			command = "gt"
		elif(command == "<"):
			command = "lt" 
		f.write("  "+command+"\n")
	def writeLabel(self,label):
		f.write("label "+label+"\n")
	def writeGoto(self,label):
		f.write("  goto "+label+"\n")
	def writeIf(self,label):
		f.write("  if-goto "+label+"\n")
	def writeCall(self,name,nArgs):
		f.write("  call "+name+" "+str(nArgs)+"\n")
	def writeFunction(self,name,nLocals):
		f.write("function "+name+" "+str(nLocals)+"\n")
	def writeReturn(self):
		f.write("  return\n")

# class JackAnalyzer:
# 	def __init__():



#C:\Users\goldfish\Desktop\nand2tetris\tools\TextComparer.bat
if (__name__ == '__main__'):
	print(len(sys.argv))
	for i in range(len(sys.argv)):
		if(i == 0):
			continue
		tmp = sys.argv[i]
		print(tmp)
		_path = ""
		if(tmp.find(".") == -1):
			if(tmp[0] != '/'):
				_path = os.getcwd() + "/"
				_path = os.path.join(_path,tmp)
				os.chdir(_path)
			else:
				_path = tmp
				os.chdir(_path)
			for fpath,dirs,fs in os.walk(_path):
				for file in fs:
					if(file.find(".jack") != -1):
						# obj1 = JackTokenizer(file)
						# obj1.Advance()
						obj2 = JackTokenizer(file)					
						compiler = CompilationEngine(obj2)
						compiler.CompileClass()
		else:
			# obj1 = JackTokenizer(tmp)
			# obj1.Advance()
			obj2 = JackTokenizer(tmp)		
			compiler = CompilationEngine(obj2)
			compiler.CompileClass()
			# obj = JackTokenizer("C:\\Users\\goldfish\\Desktop\\nand2tetris\\projects\\10\\ArrayTest\\Main.jack")


	