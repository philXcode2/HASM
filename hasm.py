from rply import LexerGenerator, ParserGenerator
import io, sys

####################################### open and prepare files ##############################################
in_file = sys.argv[1]
dot_index = in_file.rindex('.')
if in_file[dot_index:] != ".hasm":
    print(".hasm expected at end of input path")
    exit()
file = io.open(sys.argv[1], mode="r", encoding="utf-8")     # input file
asm_file = io.open(in_file[0:dot_index] + ".asm", mode='w')
####################################### open and prepare files ##############################################

###################################### utility functions ##################################################
token_list = []
###################################### utility functions ##################################################

####################################### generate lexer ###################################################
# generate parser
lg = LexerGenerator()
# add all the keywords and tokens
lg.add("GLOBAL", r'लौकिक')
lg.add("SECTION", r'ढेर')
lg.add("mov", r'भेजो')
lg.add("int", r'रोक') #interrupt
# mathematical operation_statements
lg.add("add", r'जोड')
lg.add("sub", r'घटा')
lg.add("mul", r'गुण')
lg.add("div", r'विभाज')
lg.add("cmp", r'तुलना')
# control flow instructions
lg.add("jmp", r'छलांग')
lg.add("jl", r'छलांग-कम')
lg.add("jg", r'छलांग-अधिक')
# stack operation_statements
lg.add("push", r'डाल')
lg.add("pop", r'निकाल')
lg.add("esp", r'तल')
lg.add("ebp", r'तट')
# registers
lg.add("eax", r'संचालक')
lg.add("ecx", r'अंक')
lg.add("ebx", r'सुचि')
lg.add("edx", r'सूचना')

# general purpose tokens
lg.add("number", r'[1-9]d*')
lg.add("hexadecimal", r'[0][xX][0-9a-fA-F]+')
lg.add("NAME", r'[a-zA-Z_][a-zA-Z0-9_]+')
lg.add("H_NAME", r"[बहगदजडपरकतचटमनवलसयज्ञत्रक्षश्रऋऔऐआईऊभङघधझढञऑओएअइउफखथछठषशण][बहगदजडपरकतचटमनवलसयज्ञत्रक्षश्रऋऔऐआईऊभङघधझढञऑओएअइउफखथछठषशणैौाीूोे्िुंृ़ॉॅःँ]*")
lg.add("COLON", r':')
lg.add("COMMA", r',')
lg.add("SEMICOLON", r';')   # plan to use later for comments or  ending statements
lg.ignore(r' ')
lg.ignore(r'\n')

lexer = lg.build()
####################################### generate lexer ###################################################

###################################### generate parser ###################################################
# generate parser
# add all tokens that parser will use
pg = ParserGenerator([
    "GLOBAL", "SECTION", "mov", "int", 
    "add", "sub", "mul", "div", "cmp",
    "jmp", "jl", "jg",
    "push", "pop", "esp", "ebp", "eax", "ecx", "ebx", "edx",
    "number", "hexadecimal", "COLON", "NAME", "COMMA", "H_NAME"
])

# collect multiple statements
@pg.production('statement_list : statement')
def start(p):
    print("rule 1: ", p)
@pg.production('statement_list : statement_list statement')
def start(p):
    print("rule 3: ", p)

# initializers
@pg.production('statement : declaration')
def start(p):
    print("rule 4: ", p)
@pg.production('statement : label')
def start(p):
    print("rule 5: ", p)

@pg.production('declaration : GLOBAL H_NAME')
def start(p):
    print("rule 6: ", p)
    #print(p[1].__dict__) use this to list all members of token object
    if p[1].value == "शुरु": 
        p[1].value = "_start"
    asm_file.write("global " + p[1].value + "\n")

@pg.production('declaration : SECTION H_NAME')
def start(p):
    print("rule 7: ", p)
    if p[1].value == "शुरु": 
        p[1].value = "_start"
    asm_file.write("section ." + p[1].value + '\n')

@pg.production('label : H_NAME COLON')
def start(p):
    print("rule 8: ", p)
    if p[0].value == "शुरु": 
        p[0].value = "_start"
    asm_file.write(p[0].value + ' :\n')

# operation statements
@pg.production('statement : double_operation_statement')
def start(p):
    print("rule 9: ", p)
@pg.production('statement : single_operation_statement')
def start(p):
    print("rule 10: ", p)
# @pg.production('statement : zero_operation')
# def start(p):
#     print("rule 10: ", p)

@pg.production('double_operation_statement : double_operation operand COMMA operand')
def start(p):
    print("rule 11: ", p)
    asm_file.write(token_list[0] + ' ' + token_list[2] + ',' + token_list[1] + '\n')
    token_list.clear()
@pg.production('single_operation_statement : single_operation operand')
def start(p):
    print("rule 12: ", p)
    asm_file.write(token_list[0] + ' ' + token_list[1] + '\n')
    token_list.clear()

# operation_statements
@pg.production('double_operation : mov')
def start(p):
    print("rule 13: ", p)
    token_list.append('mov')
@pg.production('double_operation : add')
def start(p):
    print("rule 14: ", p)
    token_list.append('add')
@pg.production('double_operation : sub')
def start(p):
    print("rule 15: ", p)
    token_list.append('sub')
@pg.production('double_operation : cmp')
def start(p):
    print("rule 16: ", p)
    token_list.append('cmp')

@pg.production('single_operation : int')
def start(p):
    print("rule 17: ", p)
    token_list.append('int')
@pg.production('single_operation : mul')
def start(p):
    print("rule 18: ", p)
    token_list.append('mul')
@pg.production('single_operation : div')
def start(p):
    print("rule 19: ", p)
    token_list.append('div')
@pg.production('single_operation : jmp')
def start(p):
    print("rule 20: ", p)
    token_list.append('jmp')
@pg.production('single_operation : jg')
def start(p):
    print("rule 21: ", p)
    token_list.append('jg')
@pg.production('single_operation : jl')
def start(p):
    print("rule 22: ", p)
    token_list.append('jl')
@pg.production('single_operation : push')
def start(p):
    print("rule 23: ", p)
    token_list.append('push')
@pg.production('single_operation : pop')
def start(p):
    print("rule 24: ", p)
    token_list.append('pop')

# @pg.production('zero_operation : syscall')
# def start(p):
#     print("rule 14: ", p)
#     asm_file.write("syscall\n")

@pg.production('operand : number')
def start(p):
    print("rule 25: ", p)
    token_list.append(p[0].value)
@pg.production('operand : hexadecimal')
def start(p):
    print("rule 26: ", p)
    token_list.append(p[0].value)
@pg.production('operand : esp')
def start(p):
    print("rule 27: ", p)
    token_list.append('esp')
@pg.production('operand : ebp')
def start(p):
    print("rule 28: ", p)
    token_list.append('ebp')
@pg.production('operand : eax')
def start(p):
    print("rule 29: ", p)
    token_list.append('eax')
@pg.production('operand : ecx')
def start(p):
    print("rule 30: ", p)
    token_list.append('ecx')
@pg.production('operand : ebx')
def start(p):
    print("rule 31: ", p)
    token_list.append('ebx')
@pg.production('operand : edx')
def start(p):
    print("rule 32: ", p)
    token_list.append('edx')

parser = pg.build()
###################################### generate parser ###################################################

###################################### run the assembler ##################################################
token_stream = lexer.lex(file.read())
parser.parse(token_stream)
file.close()
asm_file.close()
###################################### run the assembler ##################################################