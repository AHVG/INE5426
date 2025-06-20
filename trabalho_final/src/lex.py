from src.excpetions import LexicalError


class Lexer:
    def __init__(self, machines, keywords):
        self.machines = machines
        self.keywords = keywords
        self.text = ""
        self.index = 0
        self.line = 1
        self.column = 1
        self.finished = True

    def start(self, text: str):
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 1
        self.finished = False

    def next_token(self):
        if self.finished or self.index >= len(self.text):
            self.finished = True
            return None

        i = self.index
        line = self.line
        column = self.column

        best_match = None
        best_length = 0
        best_machine = None
        rollback = 0

        for machine in self.machines:
            machine.reset()
            j = i
            while j < len(self.text) and machine.step(self.text[j]):
                if machine.is_accepting():
                    lexeme = machine.get_lexeme()
                    current_length = j - i + 1

                    current_rollback = 1 if any('*' in s for s in machine.accepting_states) else 0
                    effective_length = current_length - current_rollback
                    best_effective_length = best_length - rollback

                    if effective_length > best_effective_length:
                        best_match = lexeme
                        best_length = current_length
                        rollback = current_rollback
                        best_machine = machine

                j += 1

        if best_match:
            consumed = best_length - rollback
            token_type = best_machine.name
            token = best_match[:-rollback] if rollback else best_match

            # Atualiza linha/coluna
            for c in token:
                if c == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1

            self.index += consumed

            if token_type == "WS":
                return self.next_token()  # Pula espaço e vai direto pro próximo

            if token_type == "ID" and token in self.keywords:
                token_type = "KEYWORD"

            return (token_type, token, line, column)
        else:
            raise LexicalError(f"Unexpected character '{self.text[i]}' at line {line}, column {column}")
