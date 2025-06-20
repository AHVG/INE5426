from compiler import Compiler


if __name__ == "__main__":
    program = '''
    int a = 12 + 34;

    def asdf() {
        float var=0.23;
        string other_var = "Um texto qualquer, que tem virgula e ponto e se quiser underline ___. Ja ia esquecendo dos numeros 1234567890";
        
        if (1 == 1) {
            print("Hello world")
        } else if (5 >= 3.2) {
            read;
        }

        return 12.0032;
    }

    float ret = call asdf();

    '''

    compiler = Compiler()
    compiler.compile(program)
    