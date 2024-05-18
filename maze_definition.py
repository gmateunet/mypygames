from globals import *
from mazes import mazes
import random

class Maze:
    def __init__(self, rows=15, cols=20):
        self.rows = rows
        self.cols = cols
        self.maze = self.select_random_maze()
        self.total_pills = sum(row.count('.') for row in self.maze)
        self.valid_positions = self.get_valid_positions()

    def select_random_maze(self):
        return random.choice(mazes)

    def get_valid_positions(self):
        valid_positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == '.':
                    valid_positions.append((col, row))
        return valid_positions

    def draw(self, screen, tile_size, padding, header_height):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * tile_size + padding
                y = row * tile_size + header_height + padding
                if self.maze[row][col] == '#':
                    pygame.draw.rect(screen, BLUE, (x, y, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, WHITE, (x, y, tile_size, tile_size))
                    if self.maze[row][col] == '.':
                        pygame.draw.circle(screen, RED, (x + tile_size // 2, y + tile_size // 2), 5)

    def is_wall(self, x, y):
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.maze[y][x] == '#'
        return False

    def eat_pill(self, x, y):
        if 0 <= y < self.rows and 0 <= x < self.cols and self.maze[y][x] == '.':
            self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
            return True
        return False

    def get_random_valid_position(self):
        return random.choice(self.valid_positions)
