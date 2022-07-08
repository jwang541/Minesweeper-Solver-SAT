import time
import json
from solver_implementation import *

n_rows = 16
n_cols = 30
n_mines = 99
initial = (int(n_rows / 2), int(n_cols / 2))

board = Board(0, 0, 0)
player_solution = Solution(0, 0, 0)
solver_solution = Solution(0, 0, 0)

updated_solver = False
used_solver = False

updated_statistics = False
n_wins = 0
n_losses = 0

modes = [(8, 8, 10), (16, 16, 40), (16, 30, 99)]
statistics = [[0, 0], [0, 0], [0, 0]]
records = [3599, 3599, 3599]

state = 0  # -1: loss, 0: ongoing, 1: win

start_time = 0


def new_state(force_solvable=False):
    global board
    global player_solution
    global solver_solution
    global used_solver
    global updated_solver
    global start_time
    global state
    global updated_statistics

    board = generate_fair_board(n_rows, n_cols, n_mines, initial, max_depth=1, remainder_cutoff=16, max_attempts=1000) \
        if force_solvable else generate_fun_board(n_rows, n_cols, n_mines, initial, max_attempts=1000)
    player_solution = Solution(board.n_rows, board.n_cols, board.n_mines)
    solver_solution = Solution(board.n_rows, board.n_cols, board.n_mines)

    initial_revealed = board.reveal_node(initial)
    update_solution(player_solution, initial_revealed)
    update_solution(solver_solution, initial_revealed)

    state = 0
    used_solver = False
    updated_solver = False
    updated_statistics = False
    start_time = time.time()


def load_statistics():
    global records
    global statistics

    try:
        with open('save_data/records.json', 'r') as f:
            records = json.load(f)
    except FileNotFoundError:
        records = [3599, 3599, 3599]
    try:
        with open('save_data/statistics.json', 'r') as f:
            statistics = json.load(f)
    except FileNotFoundError:
        statistics = [[0, 0], [0, 0], [0, 0]]


def save_statistics():
    with open('save_data/records.json', 'w') as f:
        json.dump(records, f)
    with open('save_data/statistics.json', 'w') as f:
        json.dump(statistics, f)


def mode():
    return modes.index((player_solution.n_rows, player_solution.n_cols, player_solution.n_mines))

