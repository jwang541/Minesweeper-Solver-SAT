import random

import networkx as nx


class Board:
    def __init__(self, n_rows, n_cols, n_mines=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_mines = n_mines

        self.grid = nx.grid_2d_graph(n_rows, n_cols)
        self.grid.add_edges_from([
                                     ((x, y), (x + 1, y + 1))
                                     for x in range(n_rows - 1)
                                     for y in range(n_cols - 1)
                                 ] + [
                                     ((x + 1, y), (x, y + 1))
                                     for x in range(n_rows - 1)
                                     for y in range(n_cols - 1)
                                 ], weight=1.4)
        for n in self.grid.nodes:
            self.grid.nodes[n]['value'] = 0
            self.grid.nodes[n]['revealed'] = False

        mine_positions = [i for i in range(self.n_rows * self.n_cols)]
        random.shuffle(mine_positions)

        for i in range(self.n_mines):
            x = mine_positions[i] % self.n_rows
            y = int(mine_positions[i] / self.n_rows)
            self.grid.nodes[(x, y)]['value'] = -1

        for n in self.grid.nodes:
            if self.value_at(n) == -1:
                continue
            n_adj_mines = sum(1 for m in nx.neighbors(self.grid, n) if self.value_at(m) == -1)
            self.grid.nodes[n]['value'] = n_adj_mines

    def __str__(self):
        string = ''
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.value_at((i, j)) == -1:
                    string = string + ' * '
                else:
                    if self.value_at((i, j)) == 0:
                        string = string + ' 0 '
                    else:
                        string = string + ' ' + str(self.value_at((i, j))) + ' '
            string = string + '\n'
        return string

    def reveal_node(self, node):
        if self.grid.nodes[node]['revealed']:
            return []
        self.grid.nodes[node]['revealed'] = True
        revealed_nodes = []
        if self.value_at(node) == 0:
            revealed_nodes.append((node, self.value_at(node)))
            for n in self.grid.neighbors(node):
                revealed_nodes = revealed_nodes + self.reveal_node(n)
        else:
            revealed_nodes.append((node, self.value_at(node)))
        return revealed_nodes

    def reveal_nodes(self, nodes):
        revealed_nodes = []
        for n in nodes:
            revealed_nodes = revealed_nodes + self.reveal_node(n)
        return revealed_nodes

    def reset_reveals(self):
        for n in self.grid.nodes:
            self.grid.nodes[n]['revealed'] = False

    def value_at(self, node):
        return self.grid.nodes[node]['value']


def generate_board(rows, cols, mines):
    return Board(rows, cols, mines)


def generate_safe_board(nrows, ncols, nmines, initial, max_attempts=10):
    for i in range(max_attempts):
        candidate_board = Board(nrows, ncols, nmines)
        if candidate_board.grid.nodes[initial]['value'] != -1:
            return candidate_board
    return generate_board(nrows, ncols, nmines)


def generate_fun_board(nrows, ncols, nmines, initial, max_attempts=10):
    for i in range(max_attempts):
        candidate_board = Board(nrows, ncols, nmines)
        if candidate_board.grid.nodes[initial]['value'] == 0:
            return candidate_board
    return generate_safe_board(nrows, ncols, nmines, initial)
