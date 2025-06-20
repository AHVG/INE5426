from src.constants import MACHINES, KEYWORDS, LL1_TABLE
from src.lex import Lexer
from src.parser import Parser


class Compiler:

    def __init__(self):
        self.lexer = Lexer(MACHINES, KEYWORDS)
        self.parser = Parser(self.lexer, LL1_TABLE)
        self.tokens = []
    
    def get_tokens(self):
        return self.tokens
    
    def compile(self, program):

        self.lexer.start(program)

        self.parser.parse()