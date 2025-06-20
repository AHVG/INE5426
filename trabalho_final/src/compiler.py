from src.machines import machines, keywords
from src.lex import Lexer


class Compiler:

    def __init__(self):
        self.lexer = Lexer(machines, keywords)
        self.tokens = []
    
    def get_tokens(self):
        return self.tokens
    
    def compile(self, program):

        self.lexer.start(program)

        while True:
            token = self.lexer.next_token()

            if token is None:
                break

            token_type, lexeme, line, column = token
            self.tokens.append((token_type, lexeme, line, column))
            print(f"{token_type}: '{lexeme}' at line {line}, column {column}")
