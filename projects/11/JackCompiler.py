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
	# def __del__(self):
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
			elif(self.tokenType() == "SYMBOL"):
				tmp = self.symbol()
				if(tmp == "<"):
					pass
				elif(tmp == ">"):
					pass
				elif(tmp == "\""):
					pass
				elif(tmp == "&"):
					pass
				else:
					pass
			elif(self.tokenType() == "INT_CONST"):
				tmp = str(self.intVal())
			elif(self.tokenType() == "STRING_CONST"):
				tmp = self.stringVal()
			elif(self.tokenType() == "IDENTIFIER"):
				tmp = self.identifier()
				# 变量是否定义
				# if(symbolTable.KindOf(tmp) == "NONE"):
				# 	pass
				# else:
				# 	pass
				# # 变量是否已使用
				# if(symbolTable.HaveBeenUsed(tmp) == True):
				# 	pass
				# elif(symbolTable.HaveBeenUsed(tmp) == False):
				# 	pass
				# # 变量是否有索引
				# if(id_type == "VAR" or id_type == "ARG" or id_type == "STATIC" or id_type == "FIELD"):
				# 	pass

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
		self.while_num = 0
		self.if_num = 0		
	# def __del__(self):
		# self.fout.close()
	def CompileClass(self):
		#self.num += 1
		# self.fout.write("<class>\n")
		self.tokenizer.advance()  # 'class'
		self.tokenizer.advance()  # className
		self.tokenizer.advance()  # '{'
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == 'static' or self.tokenizer.word_list[self.tokenizer.token_iter] == 'field' ):
			self.CompileClassVarDec()
		static_num = self.symbolTable.static_num
		self.field_num = static_num	
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
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == 'method' or self.tokenizer.word_list[self.tokenizer.token_iter] == 'constructor'):
			self.symbolTable.Define("this",self.file_name,"ARG")
		self.tokenizer.advance()  # ('constructor'|'function'|'method')
		self.tokenizer.advance()  # ('void'|type)
		self._subroutineName = self.tokenizer.word_list[self.tokenizer.token_iter]	
		self.tokenizer.advance()  # subroutineName
		self.tokenizer.advance()  # '('
		self.CompileParameterList()		
		self.tokenizer.advance()  # ')'
		self.CompileSubroutineBody()
		# self.fout.write("</subroutineDec>\n")	
	def CompileSubroutineBody(self):
		# self.fout.write("<subroutineBody>\n")
		self.tokenizer.advance()  # {
		_num = 0
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == "var"):
			_num += self.CompileVarDec()
		_name = self.file_name + "." + self._subroutineName
		self.vmwriter.writeFunction(_name,_num)	
		self.CompileStatements()
		self.tokenizer.advance() # }
		# self.fout.write("</subroutineBody>\n")	

	def CompileParameterList(self):
		# self.fout.write("<parameterList>\n")
		if(self.tokenizer.word_list[self.tokenizer.token_iter] != ")"):
			_type = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  #type
			_name = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  #varName
			self.symbolTable.Define(_name,_type,"ARG")
			while(self.tokenizer.word_list[self.tokenizer.token_iter] == ","):
				 self.tokenizer.advance()  #,
				 _type = self.tokenizer.word_list[self.tokenizer.token_iter]
				 self.tokenizer.advance()  #type
				 _name = self.tokenizer.word_list[self.tokenizer.token_iter]
				 self.tokenizer.advance()  #varName
				 self.symbolTable.Define(_name,_type,"ARG")
		# self.fout.write("</parameterList>\n")
	def CompileVarDec(self):
		# self.fout.write("<varDec>\n")
		_num = 1
		self.tokenizer.advance()  #var
		_type = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  #type
		_name = self.tokenizer.word_list[self.tokenizer.token_iter]
		self.tokenizer.advance()  #varName
		self.symbolTable.Define(_name,_type,"VAR")
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == ","):
			_num += 1
			self.tokenizer.advance()  #,
			_name = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  #varName
			self.symbolTable.Define(_name,_type,"VAR")
		self.tokenizer.advance()  #;
		return _num
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
			flag = False
			if(self.symbolTable.TypeOf(_name) != "NONE"):
				_name = self.symbolTable.TypeOf(_name)
				flag = True
			self.tokenizer.advance()  # '.'
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == "new" and _name != "Array" and _name != "String"):
				flag = True			
			_name = _name + "." +self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  # subroutineName		
			self.tokenizer.advance()  # '('
			_num = self.CompileExpressionList()
			self.tokenizer.advance()  # ')'
			self.tokenizer.advance()  # ';'
			if(flag):
				_num += 1
			self.vmwriter.writeCall(_name,_num)
		else:
			_name = self.file_name + "." + _name
			self.tokenizer.advance()  # '('
			_num = self.CompileExpressionList()
			self.tokenizer.advance()  # ')'
			self.tokenizer.advance()  # ';'	
			self.vmwriter.writeCall(_name,_num+1)	
		# self.fout.write("</doStatement>\n")

	def CompileLet(self):
		# self.fout.write("<letStatement>\n")
		self.tokenizer.advance()  #'let'	
		_name = self.tokenizer.word_list[self.tokenizer.token_iter]
		_kind = self.symbolTable.KindOf(_name)
		_index = self.symbolTable.IndexOf(_name)
		self.tokenizer.advance()  # varName
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == "["):
			if(_kind == "VAR"):
				self.vmwriter.writePush("local",_index)
			elif(_kind == "ARG"):
				self.vmwriter.writePush("argument",_index)
			elif(_kind == "FIELD"):
				self.vmwriter.writePush("static",self.field_num+_index)
			elif(_kind == "STATIC"):
				self.vmwriter.writePush("static",_index)
			self.tokenizer.advance()  # '['
			self.CompileExpression()
			self.vmwriter.writeArithmetic("+")
			self.vmwriter.writePop("pointer",0)
			self.tokenizer.advance()  # ']'

			self.tokenizer.advance()  # '='
			self.CompileExpression()
			self.tokenizer.advance()  # ';'	
			self.vmwriter.writePop("this",0)		
		else:
			self.tokenizer.advance()  # '='
			self.CompileExpression()
			self.tokenizer.advance()  # ';'
			
			if(_kind == "VAR"):
				self.vmwriter.writePop("local",_index)
			elif(_kind == "ARG"):
				self.vmwriter.writePop("argument",_index)
			elif(_kind == "FIELD"):
				self.vmwriter.writePop("static",self.field_num+_index)
			elif(_kind == "STATIC"):
				self.vmwriter.writePop("static",_index)
		# self.fout.write("</letStatement>\n")	

	def CompileWhile(self):
		# self.fout.write("<whileStatement>\n")
		_now = str(self.while_num)
		self.while_num += 1
		self.tokenizer.advance()  #'while'	
		self.tokenizer.advance()  # '('
		self.vmwriter.writeLabel("begin_"+_now)
		self.CompileExpression()
		self.vmwriter.writeIf("while_"+_now)
		self.vmwriter.writeGoto("end_while_"+_now)
		self.vmwriter.writeLabel("while_"+_now)
		self.tokenizer.advance()  # ')'
		self.tokenizer.advance()  # '{'
		self.CompileStatements()
		self.vmwriter.writeGoto("begin_"+_now)
		self.vmwriter.writeLabel("end_while_"+_now)
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
		_now = str(self.if_num)
		self.if_num += 1
		self.tokenizer.advance()  #'if'	
		self.tokenizer.advance()  # '('
		self.CompileExpression()
		self.vmwriter.writeIf("if_"+_now)
		self.vmwriter.writeGoto("else_"+_now)
		self.vmwriter.writeLabel("if_"+_now)
		self.tokenizer.advance()  # ')'
		self.tokenizer.advance()  # '{'
		self.CompileStatements()
		self.tokenizer.advance()  # '}'	
		self.vmwriter.writeGoto("end_if_"+_now)
		self.vmwriter.writeLabel("else_"+_now)
		if(self.tokenizer.word_list[self.tokenizer.token_iter] == "else"):
			self.tokenizer.advance()  # "else"
			self.tokenizer.advance()  # '{'
			self.CompileStatements()
			self.tokenizer.advance()  # '}'
		self.vmwriter.writeLabel("end_if_"+_now)							
		# self.fout.write("</ifStatement>\n")	

	def CompileExpression(self):
		# self.fout.write("<expression>\n")
		self.CompileTerm()
		while(self.tokenizer.word_list[self.tokenizer.token_iter] == "+" or self.tokenizer.word_list[self.tokenizer.token_iter] == "-" or self.tokenizer.word_list[self.tokenizer.token_iter] == "*" or self.tokenizer.word_list[self.tokenizer.token_iter] == "/" or self.tokenizer.word_list[self.tokenizer.token_iter] == "&" or self.tokenizer.word_list[self.tokenizer.token_iter] == "|" or self.tokenizer.word_list[self.tokenizer.token_iter] == "<" or self.tokenizer.word_list[self.tokenizer.token_iter] == ">" or self.tokenizer.word_list[self.tokenizer.token_iter] == "="):
			_op = self.tokenizer.word_list[self.tokenizer.token_iter]
			self.tokenizer.advance()  # op
			self.CompileTerm()
			if(_op != "*" and _op != "/"):
				self.vmwriter.writeArithmetic(_op)
			elif(_op == "*"):
				self.vmwriter.writeCall("Math.multiply",2)
			elif(_op == "/"):
				self.vmwriter.writeCall("Math.divide",2)
		# self.fout.write("</expression>\n")	

	def CompileTerm(self):
		# self.fout.write("<term>\n")
		# self.tokenizer.now_token = self.tokenizer.word_list[self.tokenizer.token_iter]
		if(self.tokenizer.LL1tokenType() == "INT_CONST"):
			self.tokenizer.advance() # INT
			self.vmwriter.writePush("constant",self.tokenizer.intVal())
		elif(self.tokenizer.LL1tokenType() == "STRING_CONST"):
			self.tokenizer.advance() # STRING
			_string = self.tokenizer.stringVal()
			_slen = len(_string)			
			self.vmwriter.writePush("constant",_slen)
			self.vmwriter.writeCall("String.new",1)
			for i in range(_slen):
				self.vmwriter.writePush("constant",ord(_string[i]))
				self.vmwriter.writeCall("String.appendChar",2)
		elif(self.tokenizer.LL1tokenType() == "KEYWORD"):
			if(self.tokenizer.word_list[self.tokenizer.token_iter] == 'true'):
				self.vmwriter.writePush("constant",1)
				self.vmwriter.writeArithmetic("--")
			elif(self.tokenizer.word_list[self.tokenizer.token_iter] == 'false'):
				self.vmwriter.writePush("constant",0)	
			elif(self.tokenizer.word_list[self.tokenizer.token_iter] == 'this'):
				self.vmwriter.writePush("argument",0)	
			elif(self.tokenizer.word_list[self.tokenizer.token_iter] == 'null'):
				self.vmwriter.writePush("constant",0)	
			self.tokenizer.advance()  # 'true' or 'false' or 'null' or 'this'

		elif(self.tokenizer.LL1tokenType() == "IDENTIFIER"):
			if(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "+" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "-" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "*" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "/" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "&" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "|" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "<" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == ">" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "=" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "]" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == ")" or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "," or self.tokenizer.word_list[self.tokenizer.token_iter+1] == ";"):
				_name = self.tokenizer.word_list[self.tokenizer.token_iter]
				_kind = self.symbolTable.KindOf(_name)
				_index = self.symbolTable.IndexOf(_name)				
				self.tokenizer.advance()  # varName
				if(self.symbolTable.KindOf(_name) == "VAR"):
					self.vmwriter.writePush("local",_index)
				elif(self.symbolTable.KindOf(_name) == "ARG"):
					self.vmwriter.writePush("argument",_index)
				elif(self.symbolTable.KindOf(_name) == "STATIC"):
					self.vmwriter.writePush("static",_index)
				elif(self.symbolTable.KindOf(_name) == "FIELD"):
					self.vmwriter.writePush("static",self.field_num+_index)
			elif(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "["):
				_name = self.tokenizer.word_list[self.tokenizer.token_iter]
				_kind = self.symbolTable.KindOf(_name)
				_index = self.symbolTable.IndexOf(_name)
				if(_kind == "VAR"):
					self.vmwriter.writePush("local",_index)
				elif(_kind == "ARG"):
					self.vmwriter.writePush("argument",_index)
				elif(_kind == "FIELD"):
					self.vmwriter.writePush("static",self.field_num+_index)
				elif(_kind == "STATIC"):
					self.vmwriter.writePush("static",_index)									
				self.tokenizer.advance()  # varName
				self.tokenizer.advance()  # '['
				self.CompileExpression()
				self.vmwriter.writeArithmetic("+")
				self.vmwriter.writePop("pointer",1)
				self.tokenizer.advance()  # ']'
				self.vmwriter.writePush("that",0)
			elif(self.tokenizer.word_list[self.tokenizer.token_iter+1] == "." or self.tokenizer.word_list[self.tokenizer.token_iter+1] == "("):
				flag = False
				_name = self.tokenizer.word_list[self.tokenizer.token_iter]
				self.tokenizer.advance()  #subroutineName or className or varName
				if(self.tokenizer.word_list[self.tokenizer.token_iter] == "."):
					if(self.symbolTable.TypeOf(_name) != "NONE"):
						_name = self.symbolTable.TypeOf(_name)
						flag = True
					self.tokenizer.advance()  # '.'
					if(self.tokenizer.word_list[self.tokenizer.token_iter] == "new" and _name != "Array" and _name != "String"):
						flag = True
					_name = _name + "." +self.tokenizer.word_list[self.tokenizer.token_iter]						
					self.tokenizer.advance()  # subroutineName		
					self.tokenizer.advance()  # '('
					_num = self.CompileExpressionList()
					self.tokenizer.advance()  # ')'
					if(flag):
						_num += 1
					self.vmwriter.writeCall(_name,_num)
				else:
					_name = self.file_name + "." + _name
					self.tokenizer.advance()  # '('
					_num = self.CompileExpressionList()
					self.tokenizer.advance()  # ')'
					self.vmwriter.writeCall(_name,_num+1)	
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
		self.argument_num = 0
		self.var_num = 0

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
		self.f = open(file,"w")

	def __del__(self):
		self.f.close()

	def writePush(self,segment,index):
		#segment = "constant" or "argument" or "local" or "static" 
		#                  or "this" or "that" or "pointer" or "temp"
		self.f.write("  push "+segment+" "+str(index)+"\n")

	def writePop(self,segment,index):
		self.f.write("  pop "+segment+" "+str(index)+"\n")

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
		elif(command == "="):
			command = "eq"
		elif(command == ">"):
			command = "gt"
		elif(command == "<"):
			command = "lt" 
		self.f.write("  "+command+"\n")

	def writeLabel(self,label):
		self.f.write("label "+label+"\n")

	def writeGoto(self,label):
		self.f.write("  goto "+label+"\n")

	def writeIf(self,label):
		self.f.write("  if-goto "+label+"\n")

	def writeCall(self,name,nArgs):
		self.f.write("  call "+name+" "+str(nArgs)+"\n")

	def writeFunction(self,name,nLocals):
		self.f.write("function "+name+" "+str(nLocals)+"\n")
		
	def writeReturn(self):
		self.f.write("  return\n")

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
			# 多文件操作
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
			# 单文件操作
			if(tmp.find('\\') != -1):
				file = tmp.split('\\')[-1]
				tmp = re.sub("\\\\\w+\.jack","",tmp)
				os.chdir(tmp)
			elif(tmp.find('/') != -1):
				file = tmp.split('/')[-1]
				tmp = re.sub("/\w+\.jack","",tmp)
				os.chdir(tmp)				
			else:
				file = tmp
			obj2 = JackTokenizer(file)		
			compiler = CompilationEngine(obj2)
			compiler.CompileClass()