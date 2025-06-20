import pytest

from src.compiler import Compiler
from src.excpetions import LexicalExcpetion


class TestCompiler:

    def test_compile_a_correct_program(self):
        program = """int 21 434.22; ,  \"213123 fsdfa sd_ fasd\" ++** def return"""
        compiler = Compiler()
        compiler.compile(program)
        tokens = compiler.get_tokens()
        assert tokens == [('KEYWORD', 'int', 1, 1), ('INT_CONSTANT', '21', 1, 5), ('FLOAT_CONSTANT', '434.22', 1, 8), ('SEP', ';', 1, 14), ('SEP', ',', 1, 16), ('STRING_CONSTANT', '"213123 fsdfa sd_ fasd"', 1, 19), ('OP', '+', 1, 43), ('OP', '+', 1, 44), ('OP', '*', 1, 45), ('OP', '*', 1, 46), ('KEYWORD', 'def', 1, 48), ('KEYWORD', 'return', 1, 52)]


    def test_compile_an_incorrect_program(self):
        program = """float b = 0.0;\nint a = b;\na = 2a + b;"""
        with pytest.raises(LexicalExcpetion) as exc_info:
            Compiler().compile(program)
        
        assert str(exc_info.value) == "Unexpected character '2' at line 3, column 5"