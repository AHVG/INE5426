def lex(input_string, afd_list):
    pos = 0
    tokens = []

    while pos < len(input_string):
        # Descomente para ele identificar espaços e etc
        if input_string[pos].isspace():
            pos += 1
            continue

        max_token = None
        max_length = 0
        max_weight = -1
        selected_afd = None

        for i, (afd, peso) in enumerate(afd_list):
            afd.reset()
            i_pos = pos
            last_accept = None

            while i_pos < len(input_string) and afd.step(input_string[i_pos]):
                i_pos += 1
                if afd.is_accepting():
                    last_accept = i_pos

            length = (last_accept - pos) if last_accept else 0
            if length > max_length or (length == max_length and peso > max_weight):

                max_token = input_string[pos:last_accept]
                max_length = length
                max_weight = peso
                selected_afd = afd

        if max_token is None:
            raise ValueError(f"Erro léxico na posição {pos}: '{input_string[pos]}'")

        tokens.append((selected_afd.name, max_token))
        pos += max_length

    return tokens