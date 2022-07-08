from minesweeper import *
from solver import *


def solve(board, initial, max_depth=1, remainder_cutoff=0):
    solution = Solution(board.n_rows, board.n_cols, board.n_mines)

    initial_revealed = board.reveal_node(initial)
    for node, value in initial_revealed:
        solution.grid.nodes[node]['solved'] = True
        solution.grid.nodes[node]['value'] = value

    depth = 0
    for i in range(10000):
        solved = sat_inspect(solution, depth=depth)
        revealed = board.reveal_nodes(solved)
        for node, value in revealed:
            solution.grid.nodes[node]['solved'] = True
            solution.grid.nodes[node]['value'] = value
        if len(revealed) == 0:
            if depth < max_depth:
                depth += 1
            else:
                break
        else:
            depth = 0

    for i in range(1000):
        remainder_solved = solve_remainder(solution, cutoff=remainder_cutoff)
        remainder_revealed = board.reveal_nodes(remainder_solved)
        for node, value in remainder_revealed:
            solution.grid.nodes[node]['solved'] = True
            solution.grid.nodes[node]['value'] = value
        if len(remainder_revealed) == 0:
            break

    return solution


def check_solution(board, solution):
    for n in board.grid.nodes:
        if solution.grid.nodes[n]['solved'] and board.grid.nodes[n]['value'] == -1 \
          and not solution.grid.nodes[n]['flagged']:
            return -1
    for n in board.grid.nodes:
        if not solution.grid.nodes[n]['solved'] and board.grid.nodes[n]['value'] != -1:
            return 0
    return 1


def generate_fair_board(n_rows, n_cols, n_mines, initial, max_depth=1, remainder_cutoff=16, max_attempts=1000):
    for i in range(max_attempts):
        candidate = generate_fun_board(n_rows, n_cols, n_mines, initial, max_attempts=1000)
        solution = solve(candidate, initial, max_depth=max_depth, remainder_cutoff=remainder_cutoff)
        if check_solution(candidate, solution) == 1:
            candidate.reset_reveals()
            print('Generated fair board in ' + str(i + 1) + ' attempts.')
            return candidate
    print('Could not generate fair board.')
    return generate_fun_board(n_rows, n_cols, n_mines, initial)


def update_solution(solution, revealed):
    for node, value in revealed:
        solution.grid.nodes[node]['solved'] = True
        solution.grid.nodes[node]['value'] = value
