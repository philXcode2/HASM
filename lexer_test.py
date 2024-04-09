from rply import LexerGenerator, ParserGenerator
import io

lg = LexerGenerator()
lg.add("ok", r"[बहगदजडपरकतचटमनवलसयज्ञत्रक्षश्रऋऔऐआईऊभङघधझढञऑओएअइउफखथछठषशण][बहगदजडपरकतचटमनवलसयज्ञत्रक्षश्रऋऔऐआईऊभङघधझढञऑओएअइउफखथछठषशणैौाीूोे्िुंृ़ॉॅःँ]*")
lg.ignore(r" ")
lg.ignore(r"\n")

lexer = lg.build()

pg = ParserGenerator(["ok"])
@pg.production("oks : ok")
def ok(p):
    print(p)
@pg.production("oks : oks ok")
def ok(p):
    print(p)

file = io.open("Test/lexer_test.txt", mode="r", encoding="utf-8")

parser = pg.build()
print(parser.parse(lexer.lex(file.read())))