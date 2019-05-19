from game.state import State
from game.questionitem import SubmitStatus


def run_cli_mode():
    state = State()

    state.reset()
    while not state.gameover:
        state.load_new_item()
        while True:
            print(f'Score: {state.score}')
            state.item.log_state()

            if state.is_end_game:
                break

            c = input('Enter char:').strip()
            response = state.submit_char(c)

            if response == SubmitStatus.SUCCESS:
                state.increment_score()
            print('=================')


if __name__ == '__main__':
    run_cli_mode()
