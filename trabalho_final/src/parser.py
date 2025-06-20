

from src.excpetions import SyntaxError  # ou defina uma se não tiver

class Parser:
    def __init__(self, lexer, table):
        self.lexer = lexer
        self.table = table
        self.current_token = None

    def advance(self):
        token = self.lexer.next_token()
        if token:
            self.current_token = token
        else:
            self.current_token = ("$", "$", -1, -1)

    def parse(self):
        self.advance()
        stack = ["$", "start"]  # símbolo inicial

        while stack:
            top = stack.pop()
            token_type, token_value, line, column = self.current_token
            print(f"{top} {stack} {token_type}")

            if top == "ε":
                continue

            elif top == "$":
                if token_type == "$":
                    return  # sucesso
                else:
                    self.error("EOF", token_value, line, column)

            elif top in self.table:
                entrada = token_value if token_value in self.table[top] else token_type.lower()
                if entrada not in self.table[top]:
                    self.error(f"um token válido para {top}", token_value, line, column)

                producao = self.table[top][entrada]
                for simbolo in reversed(producao):
                    stack.append(simbolo)

            elif top == token_value or top.lower() == token_type.lower():
                self.advance()

            else:
                self.error(top, token_value, line, column)

        if self.current_token[0] != "$":
            self.error("EOF", self.current_token[1], self.current_token[2], self.current_token[3])

    def error(self, expected, read, line, column):
        raise SyntaxError(f"SyntaxError at line {line}, column {column}: expected {expected}, got '{read}'")
