from rply import LexerGenerator, ParserGenerator
import io

lg = LexerGenerator()
lg.add("ok", r"स")
lg.ignore(r" ")

lexer = lg.build()

pg = ParserGenerator(["global", "लौकिक"])
@pg.production("yes : ok ok")
def ok(p):
    print(p)

file = io.open("test", mode="r", encoding="utf-8")

parser = pg.build()
print(parser.parse(lexer.lex(file.read())))