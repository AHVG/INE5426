import re

class StateMachine:
    def __init__(self, name, states, initial_state, accepting_states, transitions):
        self.name = name
        self.states = {s: [] for s in states}
        self.initial_state = initial_state
        self.accepting_states = set(accepting_states)
        self.current_state = initial_state
        self.history = []

        for from_state, regex, to_state in transitions:
            self.states[from_state].append((regex, to_state))

    def reset(self):
        self.current_state = self.initial_state
        self.history = []

    def step(self, char):
        for regex, target_state in self.states[self.current_state]:
            if re.fullmatch(regex, char):
                self.current_state = target_state
                self.history.append(char)
                return True
        return False

    def is_accepting(self):
        return self.current_state in self.accepting_states

    def get_state(self):
        return self.current_state

    def get_lexeme(self):
        return ''.join(self.history)
