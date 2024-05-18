from globals import *

class Maze:
    def __init__(self, rows=15, cols=20):
        self.rows = rows
        self.cols = cols
        self.maze = self.generate_maze(rows, cols)
        self.total_pills = sum(row.count('.') for row in self.maze)
        self.valid_positions = self.get_valid_positions()

    def generate_maze(self, rows, cols):
        # Inicializar el laberinto con paredes
        maze = [['#' for _ in range(cols)] for _ in range(rows)]
        
        # Elegir un punto inicial
        start_row, start_col = 1, 1
        maze[start_row][start_col] = '.'

        # Lista de direcciones (arriba, abajo, izquierda, derecha)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        def is_valid(row, col):
            return 0 <= row < rows and 0 <= col < cols

        def carve_path(row, col):
            random.shuffle(directions)
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if is_valid(new_row, new_col) and maze[new_row][new_col] == '#':
                    wall_row, wall_col = row + dr // 2, col + dc // 2
                    maze[wall_row][wall_col] = '.'
                    maze[new_row][new_col] = '.'
                    carve_path(new_row, new_col)

        # Empezar a tallar el laberinto desde el punto inicial
        carve_path(start_row, start_col)

        # Convertir el laberinto a una lista de cadenas
        maze_str = [''.join(row) for row in maze]
        return maze_str

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
        return self.maze[y][x] == '#'

    def eat_pill(self, x, y):
        if self.maze[y][x] == '.':
            self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
            return True
        return False

    def get_random_valid_position(self):
        return random.choice(self.valid_positions)
