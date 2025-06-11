class AFD:
    def __init__(self, name, transitions, start_state, accepting_states):
        self.name = name  # nome do token, como "ID", "NUM", etc.
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.reset()

    def reset(self):
        self.state = self.start_state

    def step(self, char):
        self.state = self.transitions.get((self.state, char), None)
        return self.state is not None

    def is_accepting(self):
        return self.state in self.accepting_states
