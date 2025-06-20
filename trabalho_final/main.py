from src.compiler import Compiler


if __name__ == "__main__":
    program = '''
    int a;
    '''
    program = '''
    def main(int argv , string args) {
        int a;
        int b;
        print b;
    }
    '''

    compiler = Compiler()
    compiler.compile(program)
