import pytest

from src.excpetions import LexicalError, SyntaxError
from src.compiler import Compiler


class TestCompiler:

    def test_compile_a_correct_program(self):
        program = "\ndef MAIN (float a, string b ){\nfloat c;\nc = a;\nreturn;\n}\n"
        compiler = Compiler()
        compiler.compile(program)

    @pytest.mark.parametrize("program, excpetion, err_msg", [
        (".def main(){})", LexicalError, "Unexpected character '.' at line 1, column 1"),
        ("def main(){a++;}", SyntaxError, "SyntaxError at line 1, column 13: expected =, got '+'"),
    ])
    def test_compile_an_incorrect_program(self, program, excpetion, err_msg):
        compiler = Compiler()
        with pytest.raises(excpetion) as exc_info:
            compiler.compile(program)
        
        assert str(exc_info.value) == err_msg
