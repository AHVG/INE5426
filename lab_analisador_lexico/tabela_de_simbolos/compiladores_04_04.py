def analisador_lexico(codigo):
    tokens = {}
    estado = 0  # Estado inicial
    lexema = ""
    i = 0
    line = 1
    
    while i < len(codigo):
        c = codigo[i]
        if c == '\n':
            line += 1
        
        # Estado inicial (S0)
        if estado == 0:
            if c.isalpha():  # Começa um identificador
                estado = 1
                lexema = c
        
        # Estado IDENT (S1)
        elif estado == 1:
            if c.isalnum():  # Continua identificador
                lexema += c
            else:
                token_set = tokens.get(lexema, set())
                token_set.add(line)
                tokens[lexema] = token_set
                estado = 0
                if not c.isspace():
                    continue
            
        i += 1
    
    return tokens

# Código de teste
codigo = """def f (int x) {
  if x < 0
     x = -x;
  return; 
}"""

tokens = analisador_lexico(codigo)
print("\n".join([f"{key}\t{list(value)}" for key, value in tokens.items()]))
# print(" ".join(tokens))