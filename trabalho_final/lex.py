class LexicalAnalyzer:
    def __init__(self, input_string, afd_list):
        self.input_string = input_string
        self.pos = 0
        self.length = len(input_string)

        # Detectar se cada item é só AFD (peso implícito pela ordem)
        self.afds = []
        for i, item in enumerate(afd_list):
            if isinstance(item, tuple):
                afd, peso = item
            else:
                afd, peso = item, len(afd_list) - i  # maior peso para o primeiro
            self.afds.append((afd, peso))

    def get_next_token(self):
        while self.pos < self.length:
            char = self.input_string[self.pos]
            if char.isspace():
                self.pos += 1
                continue

            max_token = None
            max_length = 0
            max_weight = -1
            selected_afd = None

            for afd, peso in self.afds:
                afd.reset()
                i = self.pos
                last_accept = None

                while i < self.length and afd.step(self.input_string[i]):
                    i += 1
                    if afd.is_accepting():
                        last_accept = i

                length = (last_accept - self.pos) if last_accept else 0

                if length > max_length or (length == max_length and peso > max_weight):
                    max_token = self.input_string[self.pos:last_accept]
                    max_length = length
                    max_weight = peso
                    selected_afd = afd

            if max_token is None:
                raise ValueError(f"Erro léxico na posição {self.pos}: '{self.input_string[self.pos]}'")

            self.pos += max_length
            return (selected_afd.name, max_token)

        return ('EOF', None)  # fim do programa
