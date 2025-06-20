import pytest
import src.machines

from src.lex import Lexer


class TestLexer:

    @pytest.mark.parametrize("machine, program, expected_tokens", [
        (src.machines.afd_blank, """  \n\t""", []),
        ([src.machines.afd_cond_operators, src.machines.afd_blank], """< > <= >= ==""", [('COND_OP', '<', 1, 1), ('COND_OP', '>', 1, 3), ('COND_OP', '<=', 1, 5), ('COND_OP', '>=', 1, 8), ('COND_OP', '==', 1, 11)]),
        ([src.machines.afd_float_constant, src.machines.afd_blank], """12.12 344.2 0.12 0.02 """, [('FLOAT_CONSTANT', '12.12', 1, 1), ('FLOAT_CONSTANT', '344.2', 1, 7), ('FLOAT_CONSTANT', '0.12', 1, 13), ('FLOAT_CONSTANT', '0.02', 1, 18)]),
        ([src.machines.afd_int_constant, src.machines.afd_blank], """899 0 1234 2341 """, [('INT_CONSTANT', '899', 1, 1), ('INT_CONSTANT', '0', 1, 5), ('INT_CONSTANT', '1234', 1, 7), ('INT_CONSTANT', '2341', 1, 12)]),
        ([src.machines.afd_string, src.machines.afd_blank], """\"(4321) fasd 5$!#@$¨%725 \" \"adsfa f asdf - 423_ oiwoert\"""", [('STRING_CONSTANT', '"(4321) fasd 5$!#@$¨%725 "', 1, 1), ('STRING_CONSTANT', '"adsfa f asdf - 423_ oiwoert"', 1, 28)]),
        ([src.machines.afd_ident, src.machines.afd_blank], """hsd ghsd321  k234 bvcb afsd_1234_ __234 _2a""", [('ID', 'hsd', 1, 1), ('ID', 'ghsd321', 1, 5), ('ID', 'k234', 1, 14), ('ID', 'bvcb', 1, 19), ('ID', 'afsd_1234_', 1, 24), ('ID', '__234', 1, 35), ('ID', '_2a', 1, 41)]),
        ([src.machines.afd_operators, src.machines.afd_blank], """* / % + - """, [('OP', '*', 1, 1), ('OP', '/', 1, 3), ('OP', '%', 1, 5), ('OP', '+', 1, 7), ('OP', '-', 1, 9)]),
        ([src.machines.afd_separators, src.machines.afd_blank], """{ } [] , ;""", [('SEP', '{', 1, 1), ('SEP', '}', 1, 3), ('SEP', '[', 1, 5), ('SEP', ']', 1, 6), ('SEP', ',', 1, 8), ('SEP', ';', 1, 10)]),
    ])
    def test_machines(self, machine, program, expected_tokens):
        lexer = Lexer([machine] if not isinstance(machine, list) else machine, [])
        lexer.start(program)
        tokens = []

        while True:
            token = lexer.next_token()

            if token is None:
                break

            token_type, lexeme, line, column = token
            tokens.append((token_type, lexeme, line, column))
        
        assert tokens == expected_tokens