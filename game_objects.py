import time

import pygame
import pygame.freetype
from solver_implementation import *
import game_state as gs
from pygame_utility.text import Text
from pygame_utility.group import Group
from pygame_utility.button import Button
from pygame_utility.element import Element


class Tile(Button):
    CELL_FONT = pygame.freetype.SysFont("Courier New", 24)
    CELL_FONT_COLOR = (0, 0, 0)
    SAFE_COLOR = (169, 160, 216)
    MINE_COLOR = (243, 32, 19)
    UNKNOWN_COLOR = (195, 189, 216)
    SELECTED_COLOR = (175, 169, 196)

    highlighted = {}

    def __init__(self, index=(0, 0), size=(20, 20), position=(0, 0)):
        super().__init__(size, position)
        self.index = index

    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONUP and gs.state == 0:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if event.button == 1:
                    gs.updated_solver = False
                    if gs.player_solution.grid.nodes[self.index]['flagged']:
                        return
                    revealed = gs.board.reveal_node(self.index)
                    update_solution(gs.player_solution, revealed)
                    update_solution(gs.solver_solution, revealed)
                elif event.button == 3:
                    gs.player_solution.grid.nodes[self.index]['flagged'] = \
                        not gs.player_solution.grid.nodes[self.index]['flagged']

    def draw(self, surface):
        solved = gs.player_solution.grid.nodes[self.index]['solved']
        value = gs.player_solution.grid.nodes[self.index]['value']
        flagged = gs.player_solution.grid.nodes[self.index]['flagged']

        if solved:
            if value == -1:
                self.image.fill(self.MINE_COLOR)
            elif value != 0:
                self.image.fill(self.SAFE_COLOR)
                self.CELL_FONT.render_to(self.image, (7, 4), str(value), self.CELL_FONT_COLOR)
            else:
                self.image.fill(self.SAFE_COLOR)
        else:
            if flagged:
                self.image.fill(Tile.highlighted[self.index]
                                if self.index in Tile.highlighted else self.UNKNOWN_COLOR)
                self.CELL_FONT.render_to(self.image, (7, 4), 'P', self.CELL_FONT_COLOR)
            elif pygame.mouse.get_pressed(3)[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and gs.state == 0:
                self.image.fill(self.SELECTED_COLOR)
            else:
                self.image.fill(Tile.highlighted[self.index]
                                if self.index in Tile.highlighted else self.UNKNOWN_COLOR)
        surface.blit(self.image, (self.rect.x, self.rect.y))


class SolveStepButton(Button):
    def __init__(self, size=(20, 20), position=(0, 0), fill_color=(255, 255, 255), click_color=(0, 0, 0)):
        super().__init__(size, position, fill_color, click_color)

    def on_click(self):
        if gs.state != 0:
            return
        gs.used_solver = True
        gs.updated_solver = False
        for n in gs.solver_solution.grid.nodes:
            if gs.solver_solution.grid.nodes[n]['solved'] and not gs.player_solution.grid.nodes[n]['solved']:
                if not gs.solver_solution.grid.nodes[n]['flagged']:
                    gs.player_solution.grid.nodes[n]['solved'] = True
                    gs.player_solution.grid.nodes[n]['value'] = gs.solver_solution.grid.nodes[n]['value']
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
        next_revealed = gs.board.reveal_nodes([n for n in list(next_solved)
                                               if not gs.solver_solution.grid.nodes[n]['flagged']])
        update_solution(gs.solver_solution, next_revealed)
        update_solution(gs.player_solution, next_revealed)


class ResetStateButton(Button):
    def __init__(self, size=(20, 20), position=(0, 0), fill_color=(255, 255, 255), click_color=(0, 0, 0)):
        super().__init__(size, position, fill_color, click_color)
        self.guarantee_solvability = False

    def on_click(self):
        gs.new_state(force_solvable=self.guarantee_solvability)


class FlagsRemainingLabel(Element):
    def __init__(self, size=(20, 20), position=(0, 0),
                 font=pygame.freetype.SysFont('Arial', 24), fill_color=(0, 0, 0, 0)):
        super().__init__(size, position)
        self.image.fill(fill_color)
        self.fill_color = fill_color
        self.font = font

    def draw(self, surface):
        n_flagged = sum(1 for n in gs.player_solution.grid.nodes
                        if gs.player_solution.grid.nodes[n]['flagged']
                        and not gs.player_solution.grid.nodes[n]['solved'])

        self.image.fill(self.fill_color)
        self.font.render_to(self.image, (0, 0), str(gs.board.n_mines - n_flagged),
                            fgcolor=(222, 222, 222))
        super().draw(surface)


class Timer(Element):
    def __init__(self, size=(20, 20), position=(0, 0),
                 font=pygame.freetype.SysFont('Arial', 24), fill_color=(0, 0, 0, 0), font_color=(0, 0, 0, 255)):
        super().__init__(size, position)
        self.image.fill(fill_color)
        self.fill_color = fill_color
        self.font = font
        self.font_color = font_color
        self.last_time = 0

    def draw(self, surface):
        if gs.state == 0:
            self.last_time = time.time()
        self.image.fill(self.fill_color)
        self.font.render_to(self.image, (0, 0), time.strftime('%M:%S', time.gmtime(self.last_time - gs.start_time)),
                            fgcolor=self.font_color)
        super().draw(surface)


class StatisticsDisplay(Element):
    def __init__(self, size=(20, 20), position=(0, 0),
                 title_font=pygame.freetype.SysFont('Consolas', 40), font=pygame.freetype.SysFont('Arial', 24),
                 fill_color=(0, 0, 0, 0), font_color=(0, 0, 0, 255)):
        super().__init__(size, position)
        self.image.fill(fill_color)
        self.fill_color = fill_color
        self.font = font
        self.font_color = font_color
        self.title_font = title_font

    def draw(self, surface):
        if not self.enabled:
            return

        wins = gs.statistics[gs.mode()][0]
        losses = gs.statistics[gs.mode()][1]

        self.image.fill(self.fill_color)
        if gs.state == 1:
            self.title_font.render_to(self.image, (0, 0), '*WIN*', fgcolor=self.font_color)
        elif gs.state == -1:
            self.title_font.render_to(self.image, (0, 0), '*LOSS*', fgcolor=self.font_color)
        if gs.used_solver:
            self.font.render_to(self.image, (0, 60), 'Stats are', fgcolor=self.font_color)
            self.font.render_to(self.image, (0, 100), 'disabled b/c', fgcolor=self.font_color)
            self.font.render_to(self.image, (0, 140), 'solver was', fgcolor=self.font_color)
            self.font.render_to(self.image, (0, 180), 'used.', fgcolor=self.font_color)
        else:
            self.font.render_to(self.image, (0, 60), 'Wins: ' + str(wins), fgcolor=self.font_color)
            self.font.render_to(self.image, (0, 100), 'Losses: ' + str(losses), fgcolor=self.font_color)
            win_ratio = wins / (wins + losses) if wins + losses > 0 else 0
            self.font.render_to(self.image, (0, 140), f'{win_ratio:.1%}', fgcolor=self.font_color)
            self.font.render_to(self.image, (0, 180), 'Record: ' + time.strftime('%M:%S', time.gmtime(gs.records[gs.mode()])))
        super().draw(surface)


class SizeSelect(Group):
    def __init__(self, size=(20, 20), position=(0, 0), options=None, initial=0,
                 font=pygame.freetype.SysFont('Consolas', 24), fill_color=(0, 0, 0, 0), font_color=(0, 0, 0, 255)):
        super().__init__(size, position)

        if options is None:
            options = []
        self.options = options
        for i in range(len(options)):
            n_rows, n_cols, n_mines = options[i]
            self.add_element(i, Text(position=(0, 25 * i), size=(190, 20),
                                     text=f' {n_rows} x {n_cols}, {n_mines} mines',
                                     font=pygame.freetype.SysFont('Consolas', 18), font_color=font_color))

        self.image.fill(fill_color)
        self.fill_color = fill_color
        self.font = font
        self.font_color = font_color
        self.selected_index = initial

    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for index, element in self.elements.items():
                if element.rect.collidepoint(mouse_pos):
                    self.selected_index = index


    def draw(self, surface):
        for index, element in self.elements.items():
            if index == self.selected_index:
                self.elements[index].fill_color = (222, 222, 222, 127)
            else:
                self.elements[index].fill_color = (0, 0, 0, 0)
        surface.blit(self.image, (self.rect.x, self.rect.y))
        for name, element in self.elements.items():
            element.draw(surface)
