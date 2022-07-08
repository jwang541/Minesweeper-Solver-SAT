from solver_implementation import *
import game_state as gs
import pygame.freetype
from pygame_utility.group import Group
from pygame_utility.checkbox import Checkbox
from pygame_utility.text import Text
from game_objects import *


gs.new_state()
gs.load_statistics()

pygame.init()
window = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('100% Skill Minesweeper')

tiles = Group(size=(1000, 500), position=(30, 170))
for i, j in gs.player_solution.grid.nodes:
    x = j * (24 + 1)
    y = i * (24 + 1)
    tiles.add_element((i, j), Tile((i, j), size=(24, 24), position=(x, y)))
last_size = (gs.player_solution.n_rows, gs.player_solution.n_cols)

interface = {
    'timer': Timer(size=(200, 40), position=(30, 135), font=pygame.freetype.SysFont('Consolas', 24),
                   font_color=(222, 222, 222)),
    'flags_remaining': FlagsRemainingLabel(size=(300, 40), position=(660, 135),
                                           font=pygame.freetype.SysFont('Consolas', 24)),
    'solver_checkbox': Checkbox(position=(30, 30), size=(20, 20)),
    'solver_text': Text(position=(60, 33), size=(120, 20), text='Show solver',
                        font=pygame.freetype.SysFont('Consolas', 18)),
    'solver_step_button': SolveStepButton(position=(30, 60), size=(150, 45),
                                          fill_color=(127, 127, 0), click_color=(63, 63, 0)),
    'solver_step_text': Text(position=(55, 75), size=(120, 20), text='Solve step',
                             font=pygame.freetype.SysFont('Consolas', 18)),
    'fair_board_checkbox': Checkbox(position=(210, 30), size=(20, 20)),
    'fair_board_text': Text(position=(240, 33), size=(400, 20), text='Only generate solvable boards',
                            font=pygame.freetype.SysFont('Consolas', 18)),
    'reset_state_button': ResetStateButton(size=(225, 45), position=(210, 60),
                                           fill_color=(0, 127, 127), click_color=(0, 63, 63)),
    'reset_state_text': Text(position=(235, 75), size=(400, 20), text='Generate new game',
                             font=pygame.freetype.SysFont('Consolas', 18)),
    'size_select': SizeSelect(position=(560, 33), size=(200, 400),
                              options=[(8, 8, 10), (16, 16, 40), (16, 30, 99)], initial=2,
                              font_color=(0, 0, 0)),
    'tiles': tiles,
    'statistics': StatisticsDisplay(position=(800, 180), size=(400, 400),
                                    font=pygame.freetype.SysFont('Consolas', 24), font_color=(0, 0, 0))
}

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        for key, element in interface.items():
            element.event_update(event)

    gs.state = check_solution(gs.board, gs.player_solution)
    if gs.state != 0 and not gs.updated_statistics:
        if not gs.used_solver:
            if gs.state == -1:
                gs.statistics[gs.mode()][1] += 1
            elif gs.state == 1:
                gs.statistics[gs.mode()][0] += 1
                time_taken = time.time() - gs.start_time
                gs.records[gs.mode()] = min(gs.records[gs.mode()], time_taken)
            gs.save_statistics()
        gs.updated_statistics = True

    if (gs.player_solution.n_rows, gs.player_solution.n_cols) != last_size:
        print('generate new tile set')
        tiles = Group(size=(1000, 500), position=(30, 170))
        for i, j in gs.player_solution.grid.nodes:
            x = j * (24 + 1)
            y = i * (24 + 1)
            tiles.add_element((i, j), Tile((i, j), size=(24, 24), position=(x, y)))
        interface['tiles'] = tiles
        last_size = (gs.player_solution.n_rows, gs.player_solution.n_cols)

    interface['statistics'].enabled = gs.updated_statistics

    interface['flags_remaining'].rect.x = 25 * gs.player_solution.n_cols
    interface['statistics'].rect.x = 60 + 25 * gs.player_solution.n_cols

    if interface['solver_checkbox'].state:
        gs.used_solver = True
        if not gs.updated_solver:
            gs.updated_solver = True
            next_solved = set()
            for i in range(1000):
                start_len = len(next_solved)
                for n in gs.solver_solution.grid.nodes:
                    if gs.solver_solution.grid.nodes[n]['flagged']:
                        gs.solver_solution.grid.nodes[n]['solved'] = True
                        gs.solver_solution.grid.nodes[n]['value'] = -1
                next_solved.update(solve_remainder(gs.solver_solution, cutoff=16))
                for n in gs.solver_solution.grid.nodes:
                    next_solved.update(sat_inspect_cell(gs.solver_solution, n, depth=1))
                end_len = len(next_solved)
                if start_len == end_len:
                    break
            solver_tiles = {}
            for n in next_solved:
                solver_tiles[n] = gs.solver_solution.grid.nodes[n]['flagged']
            for n in gs.solver_solution.grid.nodes:
                if gs.solver_solution.grid.nodes[n]['flagged']:
                    solver_tiles[n] = True
            Tile.highlighted.clear()
            for node, flagged in solver_tiles.items():
                Tile.highlighted[node] = (168, 125, 125) if flagged else (117, 129, 107)
    else:
        Tile.highlighted.clear()
        gs.updated_solver = False

    interface['reset_state_button'].guarantee_solvability = interface['fair_board_checkbox'].state

    gs.n_rows = interface['size_select'].options[interface['size_select'].selected_index][0]
    gs.n_cols = interface['size_select'].options[interface['size_select'].selected_index][1]
    gs.n_mines = interface['size_select'].options[interface['size_select'].selected_index][2]
    gs.initial = (int(gs.n_rows / 2), int(gs.n_cols / 2))

    window.fill((137, 138, 221))
    for name, element in interface.items():
        element.draw(window)
    pygame.display.update()

    pygame.time.Clock().tick(60)

pygame.quit()
