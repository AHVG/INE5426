def analisador_lexico(codigo):
    tokens = []
    estado = 0  # Estado inicial
    lexema = ""
    i = 0
    n = len(codigo)
    
    while i < n:
        c = codigo[i]
        
        # Estado inicial (S0)
        if estado == 0:
            if c.isalnum():  # Começa um identificador
                estado = 1
                lexema += c
            elif c.isspace():  # Ignora espaços
                pass
            else:  # Outro caractere
                estado = 2
                lexema += c
            i += 1
        
        # Estado IDENT (S1)
        elif estado == 1:
            if c.isalnum():  # Continua identificador
                lexema += c
                i += 1
            else:  # Fim do identificador
                tokens.append("IDENT")
                lexema = ""
                estado = 0
        
        # Estado OUTRO (S2)
        elif estado == 2:
            tokens.append("OUTRO")
            lexema = ""
            estado = 0
    
    # Processa últimos lexemas que podem ter ficado nos buffers
    if estado == 1:
        tokens.append("IDENT")
    elif estado == 2:
        tokens.append("OUTRO")
    
    return tokens

# Código de teste
codigo = """def f (int a) {

x = x + a;

return;

}"""

tokens = analisador_lexico(codigo)
print(" ".join(tokens))