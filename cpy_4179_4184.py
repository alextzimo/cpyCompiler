# Alexandros-Dimitrios Tzimogiannis,  A.M.: 4179, Username: cse74179
# Georgios Triantos,                  A.M.: 4184, Username: cse74184


import sys
from enum import Enum



numbers = ["0","1","2","3","4","5","6","7","8","9"]
symbols = ["+","-","*","//","%",",",":","(",")","#{","#}","##"]
relationalOperators = ["<",">","=","<=",">=","==","!="]
reservedWords = ["main","def","#def","#int","global","if","elif","else","while","print","return","input", "int","and","or","not"]


level = 0
symbolTable = []


class TokenType(Enum):
    IDENTIFIER      = 0
    NUMBER          = 1
    # Brackets
    LEFTPAREN       = 2
    RIGHTPAREN      = 3
    DIESISLEFTBRACE = 4
    DIESISRIGHTBRACE= 5
    # Separators
    COMMA           = 6
    COLON           = 7
    # Relational Operators
    LESS            = 8
    GREATER         = 9
    LESSOREQUAL     = 10
    GREATEROREQUAL  = 11
    DOUBLEEQUAL     = 12
    NOTEQUAL        = 13
    # Assignment
    ASSIGNMENT      = 14
    # Arithmetic Operators
    PLUS            = 15
    MINUS           = 16
    TIMES           = 17
    SLASH           = 18
    MOD             = 19
    # Keywords
    MAIN            = 20
    DEF             = 21
    DIESISDEF       = 22
    DIESISINT       = 23
    GLOBAL          = 24
    IF              = 25
    ELIF            = 26
    ELSE            = 27
    WHILE           = 28
    PRINT           = 29
    RETURN          = 30
    INPUT           = 31
    INT             = 32
    AND             = 33
    OR              = 34
    NOT             = 35
    DIESIS          = 36
    # EOF
    EOF             = 37
    # Comments
    DOUBLEDIESIS    = 38


class Token():
    def __init__(self, tokenType, tokenValue, tokenLineNumber, tokenCharNumber):
        self.tokenType, self.tokenValue, self.tokenLineNumber, self.tokenCharNumber = tokenType, tokenValue, tokenLineNumber, tokenCharNumber
    
    def __str__(self):
        return  '(' + str(self.tokenType)+ ', ' + str(self.tokenValue) + ', ' + str(self.tokenLineNumber) + ', ' + str(self.tokenCharNumber) + ')'




class Quad():
	def __init__(self, op, x, y, z):
		self.op, self.x, self.y, self.z = op, x, y, z

	def __str__(self):
		return str(self.op)+ ', ' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z)



#################### Symbol Table #################



class Scope():
	def __init__(self, entitiesList, nestingLevel):
		self.entitiesList, self.nestingLevel = list(), nestingLevel



class Entity():
	def __init__(self, name):
		self.name = name


class Variable(Entity):
	def __init__(self, name, datatype, offset):
		super().__init__(name)
		self.datatype, self.offset = datatype, offset


class Function(Entity):
	def __init__(self, name, datatype, startQuad, argument, framelength):
		super().__init__(name)
		self.datatype, self.startQuad, self.argument, self.framelength = datatype, startQuad, argument, framelength


class Constant(Entity):
	def __init__(self, name, value):
		super().__init__(name)
		self.value = value


class Parameter(Entity):
	def __init__(self, name, parMode, offset):
		super().__init__(name)
		self.datatype, self.parMode, self.offset = datatype, parMode, offset


class TempVariable(Entity):
	def __init__(self, name, offset):
		super().__init__(name)
		self.offset = offset



class Argument():
	def __init__(self, parMode, datatype):
		self.parMode, self.datatype = parMode, datatype



############## Symbol Table related functions ##############




def add_new_entinty(entity):
	global symbolTable
	for i in symbolTable[-1].entitiesList:
		if i.name == entity.name:
			print("Error. This entity name is already declared.")
			exit(1)
	symbolTable[-1].entitiesList.append(entity)



def add_new_scope():
	global symbolTable
	symbolTable.append(Scope(entitiesList, level))
	level += 1


def delete_scope():
	global symbolTable, level
	symbolTable.pop()
	level -= 1


def update_entity(entity, startingQuad, framelength):
	entity.startingQuad = startingQuad
	entity.framelength = framelength


def add_formal_par(name, datatype, mode):
	scope = symbolTable[-1]
	scope.append(FormalParameter(name, datatype, mode))


def search_entity(name):
	global symbolTable
	for i in symbolTable:
		for e in i.entitiesList:
			if e.name == name:
				return e
	print("Entity name not found in symbol table")
	exit(1)




lineNumber = 1
charNumber = 0
token    = Token(None, None, None, None)
programName = ""
nextLabel = 0
quadList = []
entitiesList = list()
buffer = ''
variablesToDeclare = []
scopes = list() 
globalVariables = []
localGlobalVariables = []
localVariables = []
global eraseLocalVariables
eraseLocalVariables = True
isGlobal = False
nextLabel = 0
nextTempVar = 1

global inputFile, testFile, intCodeFile, symTableFile, outFile, tok



tokens         = {
    '(':          TokenType.LEFTPAREN,
    ')':          TokenType.RIGHTPAREN,
    '#{':         TokenType.DIESISLEFTBRACE,
	'#}':         TokenType.DIESISRIGHTBRACE,
    ',':          TokenType.COMMA,
    ':':          TokenType.COLON,
    '<':          TokenType.LESS,
    '>':          TokenType.GREATER,
    '<=':         TokenType.LESSOREQUAL,
    '>=':         TokenType.GREATEROREQUAL,
    '==':         TokenType.DOUBLEEQUAL,
    '!=':         TokenType.NOTEQUAL,
    '=':          TokenType.ASSIGNMENT,
    '+':          TokenType.PLUS,
    '-':          TokenType.MINUS,
    '*':          TokenType.TIMES,
    '//':         TokenType.SLASH,
    '%':          TokenType.MOD,
    'main':       TokenType.MAIN,
    'def':        TokenType.DEF,
    '#def':       TokenType.DIESISDEF,
    '#int':       TokenType.DIESISINT,
    'global':     TokenType.GLOBAL,
    'if':         TokenType.IF,
    'elif':       TokenType.ELIF,
    'else':       TokenType.ELSE,
    'while':      TokenType.WHILE,
    'print':      TokenType.PRINT,
    'return':     TokenType.RETURN,
    'input':      TokenType.INPUT,
    'int':        TokenType.INT,
    'and':        TokenType.AND,
    'or':         TokenType.OR,
    'not':        TokenType.NOT,
    '#':          TokenType.DIESIS,
    'EOF':		  TokenType.EOF}


def errorMessage(message, lineNumber, charNumber):
	print(message + ' Line, Character: ', lineNumber, charNumber)
	sys.exit(0)	






#######  LEXICAL ANALYSIS  #######




def lex():
	
	global lineNumber, charNumber, inputFile, testFile, lexeme
	lexeme = ''
	bufferList = []
	state = 0
	OK = -2
	filePointerMove = False  # True if file pointer should be moved

	while state != OK:
		nextChar = testFile.read(1)
		bufferList.append(nextChar)
		charNumber += 1
		if nextChar == '': # Special case. End of file (EOF).
				return Token(TokenType.EOF, 'EOF', lineNumber, charNumber)
		if state == 0:
			if nextChar.isspace():
				del bufferList[-1]
				state = 0
				filePointerMove = False
				if nextChar == '\n':
					lineNumber += 1
					charNumber = 0
			elif nextChar.isalpha():
				state = 1
			elif nextChar.isdigit():
				state = 2
			elif nextChar == '<':
				state = 3
			elif nextChar == '>':
				state = 4
			elif nextChar == '!':
				state = 5
			elif nextChar == '#':
				state = 6
			elif nextChar == '=':
				state = 7
			elif nextChar == '/':
				state = 8
			elif nextChar in (':', '+', '-', '*', '%', ',', '(', ')'):
				state = OK
			else:
				errorMessage("Invalid character.", lineNumber, charNumber)
		elif state == 1:
			if nextChar == '_':
				state = 1
			elif not nextChar.isalnum():
				filePointerMove = True
				state = OK
		elif state == 2:
			if not nextChar.isdigit():
				filePointerMove = True
				state = OK
		elif state == 3:
			if nextChar != '=':
				filePointerMove = True
				state = OK
			else:
				state = OK
		elif state == 4:
			if nextChar != '=':
				filePointerMove = True
				state = OK
			else:
				state = OK
		elif state == 5:
			if nextChar == '=':
				state = OK
			else:
				errorMessage("Invalid character. Expected '!='.", lineNumber, charNumber)
		elif state == 6:
			if nextChar == '{' or nextChar == '}':
				state = OK
			elif nextChar == 'd':
				state = 9
			elif nextChar == 'i':
				state = 11
			else:
				errorMessage("Invalid character.", lineNumber, charNumber)	
		elif state == 7:
			if nextChar == '=':
				state = OK
			else:
				filePointerMove = True
				state = OK
		elif state == 8:
			if nextChar == '/':
				state = OK
			else:
				errorMessage("Invalid character. Expected '//'.", lineNumber, charNumber)
		elif state == 9:
			if nextChar == 'e':
				state = 10
			else:
				errorMessage("Invalid character.", lineNumber, charNumber)
		elif state == 10:
			if nextChar == 'f':
				state = OK
			else:
				errorMessage("Invalid character.", lineNumber, charNumber)
		elif state == 11:
			if nextChar == 'n':
				state = 12
			else:
				errorMessage("Invalid character.", lineNumber, charNumber)
		elif state == 12:
			if nextChar == 't':
				state = OK
			else:
				errorMessage("Invalid character.", lineNumber, charNumber)
		
		if state == OK:
			tln = lineNumber
			tcn = charNumber

	if filePointerMove == True:
		del bufferList[-1]
		if nextChar != '':
			testFile.seek(testFile.tell() - 1)
		charNumber -= 1
	
	lexeme = ''.join(bufferList)
	if lexeme not in tokens.keys():
		if lexeme.isdigit():
			if int(lexeme) >= -32767 and int(lexeme) <= 32767:
				returnValue = Token(TokenType.NUMBER, lexeme, tln, tcn)
			else:
				errorMessage("Invalid character '%(nextChar)d'. Integer must not be less than -32767 and not greater than 32767.", lineNumber, charNumber)
		else:
			returnValue = Token(TokenType.IDENTIFIER, lexeme[:30], tln, tcn)
	else:
		returnValue = Token(tokens[lexeme], lexeme, tln, tcn)
	del bufferList[:]
	return returnValue






#######  SYNTAX ANALYSIS  #######


def startRule():
	global token
	generate_int_code_file()
	token = lex()
	global_check()
	while token.tokenType == TokenType.DEF:
		def_function()
	def_main_function()
	if token.tokenType != TokenType.EOF:
		errorMessage("Expected EOF.", lineNumber, charNumber)


def global_check():
	global token
	if token.tokenType == TokenType.DIESISINT:
		token = lex()
		if token.tokenType == TokenType.IDENTIFIER:
			#####add_new_entinty(token.tokenValue)
			globalVariables.append(token.tokenValue)
			token = lex()
			isGlobal = True
		else:
			errorMessage("Error. Expected identifier.", lineNumber, charNumber)



def function_globals_check():
	global token
	###############
	if token.tokenType == TokenType.GLOBAL:
		token = lex()
		if token.tokenType == TokenType.IDENTIFIER:
			if token.tokenValue in globalVariables:
				########add_new_entinty(token.tokenValue)
				localGlobalVariables.append(token.tokenValue)
				token = lex()
			else:
				errorMessage("Error. The global variable has not been initialized.", lineNumber, charNumber)
		else:
			errorMessage("Error. Expected identifier.", lineNumber, charNumber)



def main_global_check():
	global token
	if isGlobal:
		if token.tokenType == TokenType.IDENTIFIER:
			if not token.tokenValue in globalVariables:
				errorMessage("Error. The variable has not been initialized.", lineNumber, charNumber)




def def_main_function():
	global token
	if token.tokenType != TokenType.DIESISDEF:
		errorMessage("Error. Expected keyword '#def'.", lineNumber, charNumber)
	token = lex()
	name = token.tokenValue
	if token.tokenType == TokenType.MAIN:
		token = lex()
		declarations()
		main_global_check()
		gen_quad("begin_block",name,"_","_")
		statements()
		gen_quad("halt","_","_","_")
		gen_quad("end_block",name,"_","_")
	else:
		errorMessage("Error. Expected keyword 'main'.", lineNumber, charNumber)



def def_function():
	global token, eraseLocalVariables
	#########token = lex()
	if token.tokenType != TokenType.DEF:
		errorMessage("Error. Expected keyword 'def'.", lineNumber, charNumber)
	token = lex()
	if token.tokenType == TokenType.IDENTIFIER:
		name = token.tokenValue
		token = lex()
		if token.tokenType == TokenType.LEFTPAREN:
			token = lex()
			id_list()
			if token.tokenType == TokenType.RIGHTPAREN:
				token = lex()
				if token.tokenType == TokenType.COLON:
					token = lex()
					if token.tokenType == TokenType.DIESISLEFTBRACE:
						token = lex()
						declarations()
						function_globals_check()
						while token.tokenType == TokenType.DEF:
							eraseLocalVariables = False
							def_function()
						#function_globals_check()
						gen_quad("begin_block",name,"_","_")
						statements()
						gen_quad("halt","_","_","_")
						gen_quad("end_block",name,"_","_")
						if token.tokenType != TokenType.DIESISRIGHTBRACE:
							errorMessage("Error. Expected keyword '#}'.", lineNumber, charNumber)
						token = lex()
						if eraseLocalVariables:
							localGlobalVariables.clear()
							localVariables.clear()
					else:
						errorMessage("Error. Expected keyword '#{'.", lineNumber, charNumber)
				else:
					errorMessage("Error. Expected keyword ':'.", lineNumber, charNumber)
			else:
				errorMessage("Error. Expected keyword ')'.", lineNumber, charNumber)
		else:
			errorMessage("Error. Expected keyword '('.", lineNumber, charNumber)
	else:
		errorMessage("Error. Expected identifier.", lineNumber, charNumber)



def declarations():
	global token
	while token.tokenType == TokenType.DIESISINT:
		declaration_line()
		#token = lex()


def declaration_line():
	global token
	token = lex()
	id_list()



def statements():
	global token
	statement()
	#token  = lex()
	while token.tokenType == TokenType.IDENTIFIER or token.tokenType == TokenType.PRINT or token.tokenType == TokenType.RETURN or token.tokenType == TokenType.IF or token.tokenType == TokenType.WHILE:
		statement()
		#token = lex()


def statement():
	global token
	#token = lex()
	if token.tokenType == TokenType.IF or token.tokenType == TokenType.WHILE:
		structured_statement()
	else:
		simple_statement()

def simple_statement():
	global token, tok
	tok = token.tokenValue
	e_place = tok
	if token.tokenType == TokenType.IDENTIFIER:
		####add_new_entinty(token.tokenValue)
		if token.tokenValue not in localGlobalVariables and token.tokenValue not in localVariables:
			errorMessage("Error. The variable has not been initialized.", lineNumber, charNumber)
		input_stat()
	elif token.tokenType == TokenType.PRINT:
		e_place = print_stat()
		gen_quad("out",e_place,"_","_")
	else:
		e_place = return_stat()
		gen_quad("retv",e_place,"_","_")


def structured_statement():
	global token
	if token.tokenType == TokenType.IF:
		if_stat()
	else:
		while_stat()


def input_stat():
	global token, tok
	token = lex()
	if token.tokenType == TokenType.ASSIGNMENT:
		token = lex()
		if token.tokenType == TokenType.INT:
			token = lex()
			if token.tokenType == TokenType.LEFTPAREN:
				token = lex()
				if token.tokenType == TokenType.INPUT:
					token = lex()
					if token.tokenType == TokenType.LEFTPAREN:
						token = lex()
						if token.tokenType == TokenType.RIGHTPAREN:
							token = lex()
							if token.tokenType == TokenType.RIGHTPAREN:
								token = lex()
							else:
								errorMessage("Error. Expected keyword ')'.", lineNumber, charNumber)
						else:
							errorMessage("Error. Expected keyword ')'.", lineNumber, charNumber)
					else:
						errorMessage("Error. Expected keyword '('.", lineNumber, charNumber)
				else:
					errorMessage("Error. Expected keyword 'input'.", lineNumber, charNumber)
			else:
				errorMessage("Error. Expected keyword '('.", lineNumber, charNumber)
			gen_quad("inp",tok,"_","_")
		else:
			exp = expression()
			e_place = exp
			gen_quad("=",e_place,"_",tok)
	else:
		errorMessage("Error. Expected keyword '='.", lineNumber, charNumber)



def print_stat():
	global token
	token = lex()
	if token.tokenType == TokenType.LEFTPAREN:
		token = lex()
		exp = expression()
		#token = lex()
		if token.tokenType == TokenType.RIGHTPAREN:
			token = lex()
		else:
			errorMessage("Error. Expected keyword ')'.", lineNumber, charNumber)
	else:
		errorMessage("Error. Expected keyword '('.", lineNumber, charNumber)



def return_stat():
	global token
	token = lex()
	if token.tokenType == TokenType.MINUS:
		token = lex()
		if token.tokenType == TokenType.NUMBER:
			returnVal = (-1)*token.tokenValue
			token = lex()
	else:
		exp = expression()
	########################



def if_stat():
	global token
	token = lex()
	(B_true, B_false) = condition()
	backpatch(B_true,next_quad())
	while token.tokenType == TokenType.AND or token.tokenType == TokenType.OR:
		token = lex()
		(B_true, B_false) = condition()
		backpatch(B_true,nextquad())
	if token.tokenType != TokenType.COLON:
		errorMessage("Error. Expected keyword ':'.", lineNumber, charNumber)
	token = lex()
	statements()
	ifList=makelist(next_quad())
	backpatch(B_false,next_quad())
	gen_quad("jump", "_", "_", "_")
	while token.tokenType == TokenType.ELIF:
		token = lex()
		(condTrue, condFalse) = condition()
		if token.tokenType != TokenType.COLON:
			errorMessage("Error. Expected keyword ':'.", lineNumber, charNumber)
		token = lex()
		statements()
		backpatch(ifList,next_quad())
	if token.tokenType == TokenType.ELSE:
		token = lex()
		if token.tokenType != TokenType.COLON:
			errorMessage("Error. Expected keyword ':'.", lineNumber, charNumber)
		token = lex()
		statements()
		backpatch(ifList,next_quad())


def while_stat():
	global token
	token = lex()
	B_quad = next_quad()
	(B_true, B_false) = condition()
	backpatch(B_true, next_quad())
	if token.tokenType == TokenType.COLON:
		token = lex()
		if token.tokenType == TokenType.DIESISLEFTBRACE:
			token = lex()
			statements()
			if token.tokenType != TokenType.DIESISRIGHTBRACE:
				errorMessage("Error. Expected keyword '#}'.", lineNumber, charNumber)
		else:
			errorMessage("Error. Expected keyword '#{'.", lineNumber, charNumber)
	else:
		errorMessage("Error. Expected keyword ':'.", lineNumber, charNumber)
	token = lex()
	gen_quad("jump", "_", "_", B_quad)
	backpatch(B_false, next_quad())
	


def id_list():
	global token
	if token.tokenType == TokenType.IDENTIFIER:
		###add_new_entinty(token.tokenValue)
		localVariables.append(token.tokenValue)
		token = lex()
		while token.tokenType == TokenType.COMMA:
			token = lex()
			localVariables.append(token.tokenValue)
			if token.tokenType != TokenType.IDENTIFIER:
				errorMessage("Error. Expected identifier.", lineNumber, charNumber)
			token = lex()





def expression():
	global token, tok
	opSign = optional_sign()
	term1 = term()
	t1_place = term1
	e_place = t1_place
	while token.tokenType == TokenType.PLUS or token.tokenType == TokenType.MINUS:
		addOp = ADD_OP()
		#token = lex()############
		term2 = term()
		t2_place = term2
		w = newtemp()
		gen_quad(addOp,t1_place,t2_place,w)
		t1_place = w
		tok = w
		#term1 = tmp
	return term1


def term():
	global token
	factor1 = factor()
	f1_place = factor1
	t_place = f1_place
	while token.tokenType == TokenType.TIMES or token.tokenType == TokenType.SLASH or token.tokenType == TokenType.MOD:
		mulOp = MUL_OP()
		#token = lex()############
		factor2 = factor()
		f2_place = factor2
		w = newtemp()
		gen_quad(mulOp,f1_place,f2_place,w)
		f1_place = w
		#factor1 = tmp
	return factor1


def factor():
	global token
	if token.tokenType == TokenType.NUMBER:
		returnVal = token.tokenValue
		token = lex()##########
		e_place = returnVal
		f_place=e_place
	elif token.tokenType == TokenType.MINUS:
		token = lex()
		if token.tokenType == TokenType.NUMBER:
			returnVal = (-1)*token.tokenValue
			token = lex()
			f_place=e_place
		else:
			errorMessage("Error. Expected number.", lineNumber, charNumber)
	elif token.tokenType == TokenType.LEFTPAREN:
		token = lex()
		returnVal = expression()
		e_place = returnVal
		if token.tokenType != TokenType.RIGHTPAREN:
			errorMessage("Error. Expected keyword ')'.", lineNumber, charNumber)
		token = lex()
		f_place=e_place
	elif token.tokenType == TokenType.IDENTIFIER:
		returnVal = token.tokenValue
		id_place = returnVal
		token = lex() ###########
		idtail()
		f_place=id_place
	else:
		errorMessage("Error. Expected integer or keyword '(' or identifier.", lineNumber, charNumber)
	return returnVal


def idtail():
	global token
	#token = lex()
	if token.tokenType == TokenType.LEFTPAREN:
		token = lex()
		actual_par_list()
		if token.tokenType != TokenType.RIGHTPAREN:
			errorMessage("Error. Expected keyword ')'.", lineNumber, charNumber)
		token = lex()



def actual_par_list():
	global token
	#token = lex()
	exp = expression()
	#token = lex()
	while token.tokenType == TokenType.COMMA:
		token = lex()
		exp = expression()



def optional_sign():
	global token
	retVal = None
	if token.tokenType == TokenType.PLUS or token.tokenType == TokenType.MINUS:
		token = lex() ##############
		return ADD_OP()
	return retVal
	


def condition():
	global token
	###########token = lex()
	(q1True, q1False) = bool_term()
	(B_true, B_false) = (q1True, q1False)
	while token.tokenType == TokenType.OR:
		backpatch(B_false, next_quad())
		token = lex()
		(q2True, q2False) = bool_term()
		B_true = mergelist(B_true, q2True)
		B_false = q2False
		############token = lex()
	return (B_true, B_false)



def bool_term():
	global token
	(qTrue, qFalse) = bool_factor()
	(r1True, r1False) = (qTrue, qFalse)
	while token.tokenType == TokenType.AND:
		backpatch(qTrue, next_quad())
		token = lex()
		(r2True, r2False) = bool_factor()
		qFalse = mergelist(qFalse, r2False)
		qTrue = r2True
	return (qTrue, qFalse)




def bool_factor():
	global token
	if token.tokenType == TokenType.NOT:
		token = lex()
		(condTrue, condFalse) = condition()
		token = lex()
		R_true = B_false
		R_false = B_true
	else:
		exp1 = expression()
		e1_place = exp1
		relOp = REL_OP()
		#token = lex() #########
		exp2 = expression()
		e2_place = exp2
		R_true=makelist(next_quad())
		gen_quad(relOp, e1_place, e2_place, "_")
		R_false=makelist(next_quad())
		gen_quad("jump", "_", "_", "_")
		return (R_true, R_false)




def REL_OP():
	global token
	rel_op = token.tokenValue
	if token.tokenType != TokenType.ASSIGNMENT and token.tokenType != TokenType.LESSOREQUAL and token.tokenType != TokenType.GREATEROREQUAL and token.tokenType != TokenType.GREATER and token.tokenType != TokenType.LESS and token.tokenType != TokenType.DOUBLEEQUAL and token.tokenType != TokenType.NOTEQUAL:
		errorMessage("Error. Expected relational operator.", lineNumber, charNumber)
	token = lex()
	return rel_op


def ADD_OP():
	global token
	add_op = token.tokenValue
	if token.tokenType != TokenType.PLUS and token.tokenType != TokenType.MINUS:
		errorMessage("Error. Expected '+' or '-'.", lineNumber, charNumber)
	token = lex()
	return add_op


def MUL_OP():
	global token
	mul_op = token.tokenValue
	if token.tokenType != TokenType.TIMES and token.tokenType != TokenType.SLASH and token.tokenType != TokenType.MOD:
		errorMessage("Error. Expected '*' or '/' or ''%'.", lineNumber, charNumber)
	token = lex()
	return mul_op


############     INTERMEDIATE CODE RELATED FUNCTIONS     #############

def next_quad():
	global nextLabel
	return nextLabel


def gen_quad(op, x, y, z):
    global nextLabel
    nextLabel += 1
    newquad  = Quad(op, x, y, z)
    quadList.append([nextLabel, newquad])


def newtemp():
	global nextTempVar
	retVal = 'T_'+str(nextTempVar)
	nextTempVar += 1
	return retVal


def emptylist():
	return list()


def makelist(x):
	newlist = list()
	newlist.append(x)
	return newlist


def mergelist(list1,list2):
	return list1 + list2


def backpatch(list1,z):
	global quadList, quadLabel
	for quad in quadList:
		if quad[0] in list1:
			quad[1].z = z


def generate_int_code_file():
	global intCodeFile
	for quad in quadList:
		intCodeFile.write((str(quad[0]))+': '+quad[1].__str__()+'\n')


def generate_symTable_file():
	global symTableFile
	for entity in entitiesList:
		symTableFile.write(str(entity))




def main():
	global inputFile, testFile, intCodeFile, symTableFile, outFile
	inputFile= sys.argv[1]
	testFile = open(inputFile, 'r')
	intCodeFile = open("intcodefile.int", 'w')
	#symTableFile = open("symTableFile.sym", 'w')
	#outFile = open("outfile.txt", 'a') 
	startRule()
	generate_int_code_file()
	#generate_symTable_file()
	testFile.close()
	intCodeFile.close()
	#outFile.close()


if __name__ == '__main__':
	main()