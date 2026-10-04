import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from logic_utils import check_guess

APP_PATH = str(ROOT / "app.py")
NORMAL_LIMIT = 8  # attempt_limit_map["Normal"] in app.py


def _new_app():
    return AppTest.from_file(APP_PATH, default_timeout=10).run()


def _submit_wrong_guess(at):
    # secret + 1 can never equal the secret, so the guess is always wrong
    wrong = at.session_state.secret + 1
    at.text_input[0].set_value(str(wrong))
    at.button[0].click()  # "Submit Guess"
    return at.run()

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Attempt limit regression tests ---
# Bug: attempts started at 1 on first load (but 0 after "New Game"), so the
# first game allowed one fewer guess than the sidebar claimed.

def test_attempts_start_at_zero():
    at = _new_app()
    assert at.session_state.attempts == 0


def test_attempts_left_shows_full_limit_before_first_guess():
    at = _new_app()
    assert f"Attempts left: {NORMAL_LIMIT}" in at.info[0].value


def test_first_game_allows_full_attempt_limit():
    at = _new_app()

    # All but the last allowed guess: the game must still be in progress
    for _ in range(NORMAL_LIMIT - 1):
        at = _submit_wrong_guess(at)
        assert at.session_state.status == "playing"

    # The final allowed guess is the one that ends the game
    at = _submit_wrong_guess(at)
    assert at.session_state.attempts == NORMAL_LIMIT
    assert at.session_state.status == "lost"


def test_attempts_left_counts_down_by_one_per_guess():
    at = _new_app()
    at = _submit_wrong_guess(at)
    assert f"Attempts left: {NORMAL_LIMIT - 1}" in at.info[0].value


# --- Difficulty change / secret range regression tests ---
# Bug: the secret was only drawn once, so switching difficulty kept a secret
# from the old range (e.g. 46 on Easy, range 1-20), and "New Game" always drew
# from 1-100 regardless of difficulty.

import pytest

RANGES = {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 50)}
OUT_OF_RANGE_SECRET = 46  # valid on Normal, impossible on Easy (1-20)


def _select_difficulty(at, difficulty):
    at.selectbox[0].select(difficulty)
    return at.run()


@pytest.mark.parametrize("difficulty", ["Easy", "Hard"])
def test_switching_difficulty_redraws_secret_in_new_range(difficulty):
    at = _new_app()
    at.session_state.secret = OUT_OF_RANGE_SECRET if difficulty == "Easy" else 99

    at = _select_difficulty(at, difficulty)

    low, high = RANGES[difficulty]
    assert low <= at.session_state.secret <= high


def test_switching_difficulty_starts_a_fresh_game():
    at = _new_app()
    at = _submit_wrong_guess(at)
    assert at.session_state.attempts == 1

    at = _select_difficulty(at, "Easy")

    assert at.session_state.attempts == 0
    assert at.session_state.score == 0
    assert at.session_state.status == "playing"
    assert at.session_state.history == []


def test_switching_back_and_forth_always_keeps_secret_in_range():
    at = _new_app()
    for difficulty in ["Easy", "Hard", "Normal", "Easy", "Hard"]:
        at = _select_difficulty(at, difficulty)
        low, high = RANGES[difficulty]
        assert low <= at.session_state.secret <= high


def test_new_game_uses_selected_difficulty_range():
    at = _new_app()
    at = _select_difficulty(at, "Easy")

    # The old code drew from 1-100, so one press could pass by luck (~20%).
    # Pressing it repeatedly makes a regression all but certain to show up.
    for _ in range(30):
        at.button[1].click()  # "New Game"
        at = at.run()
        assert 1 <= at.session_state.secret <= 20


def test_info_banner_shows_range_of_selected_difficulty():
    at = _new_app()
    at = _select_difficulty(at, "Easy")
    assert "between 1 and 20" in at.info[0].value
