from compiler.state_machine import StateMachine
from compiler.lex import Lexer


class Compiler:

    def __init__(self):
        afd_operators = StateMachine(
            name="OP",
            states=["q0", "q1", "q2", "q3", "q4", "q5", "q6"],
            initial_state="q0",
            accepting_states={"q1", "q2", "q3", "q4", "q5", "q6"},
            transitions=[
                ("q0", r"\*", "q1"),
                ("q0", r"-", "q2"),
                ("q0", r"\+", "q3"),
                ("q0", r"=", "q4"),
                ("q0", r"/", "q5"),
                ("q0", r"%", "q6"),
            ],
        )

        afd_cond_operators = StateMachine(
            name="COND_OP",
            states=["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"],
            initial_state="q0",
            accepting_states={"q5", "q6", "q7", "q8"},
            transitions=[
                ("q0", r"<", "q1"),
                ("q0", r">", "q2"),
                ("q0", r"!", "q3"),
                ("q0", r"=", "q4"),
                ("q1", r"=", "q5"),
                ("q2", r"=", "q6"),
                ("q3", r"=", "q7"),
                ("q4", r"=", "q8"),
            ],
        )


        afd_separators = StateMachine(
            name="SEP",
            states=["q0", "q1"],
            initial_state="q0",
            accepting_states={"q1"},
            transitions=[
                ("q0", r",", "q1"),
                ("q0", r";", "q1"),
                ("q0", r"\[", "q1"),
                ("q0", r"\]", "q1"),
                ("q0", r"\{", "q1"),
                ("q0", r"\}", "q1"),
                ("q0", r"\(", "q1"),
                ("q0", r"\)", "q1"),
            ],
        )


        afd_blank = StateMachine(
            name="WS",
            states=["q0", "q1"],
            initial_state="q0",
            accepting_states={"q1"},
            transitions=[
                ("q0", r"[ \n\t]", "q1"),
                ("q1", r"[ \n\t]", "q1"),
            ],
        )


        afd_ident = StateMachine(
            name="ID",
            states=["q0", "q1"],
            initial_state="q0",
            accepting_states={"q1"},
            transitions=[
                ("q0", r"[a-zA-Z_]", "q1"),
                ("q1", r"[a-zA-Z0-9_]", "q1"),
            ],
        )


        afd_string = StateMachine(
            name="STRING_CONSTANT",
            states=["q0", "q1", "q2"],
            initial_state="q0",
            accepting_states={"q2"},
            transitions=[
                ("q0", r'"', "q1"),
                ("q1", r'[^"]', "q1"),
                ("q1", r'"', "q2"),
            ],
        )


        afd_int_constant = StateMachine(
            name="INT_CONSTANT",
            states=["q0", "q1", "q2", "q3*", "q4*"],
            initial_state="q0",
            accepting_states={"q3*", "q4*"},
            transitions=[
                ("q0", r"[1-9]", "q1"),
                ("q0", r"0", "q2"),
                ("q1", r"[0-9]", "q1"),
                ("q1", r"[^a-zA-Z0-9]", 'q3*'),
                ("q2", r"[^a-zA-Z0-9]", 'q4*'),
            ],
        )


        afd_float_constant = StateMachine(
            name="FLOAT_CONSTANT",
            states=["q0", "q1", "q2", "q3", "q4", 'q5*'],
            initial_state="q0",
            accepting_states={"q5*"},
            transitions=[
                ("q0", r"[1-9]", "q1"),
                ("q0", r"0", "q2"),
                ("q1", r"[0-9]", "q1"),
                ("q1", r"\.", "q3"),
                ("q2", r"\.", "q3"),
                ("q3", r"[0-9]", "q4"),
                ("q4", r"[0-9]", "q4"),
                ("q4", r"[^a-zA-Z0-9]", 'q5*'),
            ],
        )

        keywords = ["for", "float", "else", "print", "break", "def", "return", "read", "call", "string", "null", "new", "if", "int"]

        # IMPORTANTE: A ordem importa!!
        machines = [
            afd_ident,
            afd_blank,
            afd_int_constant,
            afd_float_constant,
            afd_string,
            afd_cond_operators,
            afd_operators,
            afd_separators
        ]

        self.lexer = Lexer(machines, keywords)

        self.tokens = []
    
    def get_tokens(self):
        return self.tokens
    
    def compile(self, program):

        self.lexer.start(program)

        while True:
            token = self.lexer.next_token()

            if token is None:
                break

            token_type, lexeme, line, column = token
            self.tokens.append((token_type, lexeme, line, column))
            print(f"{token_type}: '{lexeme}' at line {line}, column {column}")
