class Lexer:
    def __init__(self, machines, keywords):
        self.machines = machines
        self.keywords = keywords

    def tokenize(self, text):
        tokens = []
        i = 0
        line = 1
        column = 1

        while i < len(text):
            best_match = None
            best_length = 0
            best_machine = None
            rollback = 0  # quanto voltar após match

            for machine in self.machines:
                machine.reset()
                j = i
                while j < len(text) and machine.step(text[j]):
                    if machine.is_accepting():
                        lexeme = machine.get_lexeme()
                        best_match = lexeme
                        best_length = j - i + 1
                        best_machine = machine

                        # Checa se estado final tem '*'
                        if any(s for s in machine.accepting_states if '*' in s):
                            rollback = 1
                        else:
                            rollback = 0
                    j += 1

            if best_match:
                if best_machine.name != "WS":
                    token_type = best_machine.name
                    token = best_match[:-rollback] if rollback else best_match

                    if token_type == "ID" and token in self.keywords:
                        token_type = "KEYWORD"

                    tokens.append((token_type, token))

                consumed = best_length - rollback
                for c in text[i:i+consumed]:
                    if c == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1

                i += consumed
            else:
                raise Exception(f"Unexpected character '{text[i]}' at line {line}, column {column}")
            
        return tokens
