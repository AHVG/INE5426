import pytest
from src.state_machine import StateMachine

class TestStateMachine:
    @pytest.fixture(autouse=True)
    def setup_machine(self):
        self.machine = StateMachine(
            name="simple_id",
            states={"q0", "q1"},
            initial_state="q0",
            accepting_states={"q1"},
            transitions=[
                ("q0", r"[a-zA-Z_]", "q1"),
                ("q1", r"[a-zA-Z0-9_]", "q1"),
            ]
        )

    def test_initial_state(self):
        assert self.machine.get_state() == "q0"
        assert not self.machine.is_accepting()

    def test_valid_identifier(self):
        for char in "abc123":
            assert self.machine.step(char) is True
        assert self.machine.get_state() == "q1"
        assert self.machine.is_accepting()
        assert self.machine.get_lexeme() == "abc123"

    def test_invalid_first_char(self):
        self.machine.reset()
        assert self.machine.step("1") is False
        assert self.machine.get_state() == "q0"
        assert not self.machine.is_accepting()

    def test_reset(self):
        self.machine.step("a")
        self.machine.step("b")
        self.machine.reset()
        assert self.machine.get_state() == "q0"
        assert self.machine.get_lexeme() == ""

    def test_partial_match(self):
        assert self.machine.step("a") is True
        assert self.machine.step("!") is False
        assert self.machine.get_state() == "q1"
        assert self.machine.get_lexeme() == "a"
