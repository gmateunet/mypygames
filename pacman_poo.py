import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 750  # Dimensiones totales de la pantalla
HEADER_HEIGHT = 50  # Altura del encabezado
PADDING = 50  # Espacio alrededor del área de juego
WIDTH, HEIGHT = SCREEN_WIDTH - 2 * PADDING, SCREEN_HEIGHT - 2 * PADDING - HEADER_HEIGHT  # Dimensiones del área de juego
TILE_SIZE = 40  # Tamaño de cada celda del laberinto
FPS = 60  # Fotogramas por segundo

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (0, 255, 0)  # Color de fondo verde

class Header:
    def __init__(self, total_pills):
        self.font = pygame.font.SysFont(None, 36)
        self.pills_left = total_pills
        self.message = ""

    def eat_pill(self):
        self.pills_left -= 1

    def set_message(self, message):
        self.message = message

    def draw(self, screen):
        screen.fill(BLACK, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
        pills_text = self.font.render(f"Pills Left: {self.pills_left}", True, WHITE)
        screen.blit(pills_text, (10, 10))
        message_text = self.font.render(self.message, True, WHITE)
        screen.blit(message_text, (SCREEN_WIDTH // 2, 10))

class Maze:
    def __init__(self):
        self.maze = [
            "####################",
            "#........#..........",
            "#.####.###.####.###.",
            "#.####.###.####.###.",
            "#...................",
            "#.####.#####.######.",
            "#.................#.",
            "#####.#.###.#.###.#.",
            "#.....#.#.#.#.#.#.#.",
            "###.###.#.#.#.#.#.#.",
            "#.................#.",
            "#.###.###.###.###.#.",
            "#.###.###.###.###.#.",
            "#.....#.....#.....#.",
            "#.###########.#####.",
        ]
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.total_pills = sum(row.count('.') for row in self.maze)

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * TILE_SIZE + PADDING
                y = row * TILE_SIZE + HEADER_HEIGHT + PADDING
                if self.maze[row][col] == '#':
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    if self.maze[row][col] == '.':
                        pygame.draw.circle(screen, RED, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 5)

    def is_wall(self, x, y):
        return self.maze[y][x] == '#'

    def eat_pill(self, x, y):
        if self.maze[y][x] == '.':
            self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
            return True
        return False

class Pacman:
    def __init__(self, maze, eat_sound):
        self.maze = maze
        self.pos = [1 * TILE_SIZE + PADDING, 1 * TILE_SIZE + HEADER_HEIGHT + PADDING]
        self.speed = 4
        self.dir = [0, 0]
        self.next_dir = [0, 0]
        self.eat_sound = eat_sound
        self.image = pygame.image.load("pacman.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def draw(self, screen):
        rotated_image = self.get_rotated_image()
        screen.blit(rotated_image, (self.pos[0], self.pos[1]))

    def get_rotated_image(self):
        if self.dir == [1, 0]:  # Derecha
            return self.image
        elif self.dir == [-1, 0]:  # Izquierda
            return pygame.transform.flip(self.image, True, False)
        elif self.dir == [0, -1]:  # Arriba
            return pygame.transform.rotate(self.image, 90)
        elif self.dir == [0, 1]:  # Abajo
            return pygame.transform.rotate(self.image, -90)
        return self.image

    def can_move(self, new_pos):
        # Verificar las cuatro esquinas del sprite de Pac-Man
        corners = [
            (new_pos[0], new_pos[1]),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1]),
            (new_pos[0], new_pos[1] + TILE_SIZE - 1),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1] + TILE_SIZE - 1)
        ]
        for (x, y) in corners:
            if x < PADDING or x >= WIDTH + PADDING or y < HEADER_HEIGHT + PADDING or y >= HEIGHT + HEADER_HEIGHT + PADDING or self.maze.is_wall((x - PADDING) // TILE_SIZE, (y - HEADER_HEIGHT - PADDING) // TILE_SIZE):
                return False
        return True

    def move(self):
        # Intentar cambiar la dirección si es posible
        new_pos = [self.pos[0] + self.next_dir[0] * self.speed, self.pos[1] + self.next_dir[1] * self.speed]
        if self.can_move(new_pos):
            self.dir = self.next_dir

        # Mover en la dirección actual
        new_pos = [self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed]
        if self.can_move(new_pos):
            self.pos = new_pos
            # Comer la píldora si está en una
            if self.maze.eat_pill((self.pos[0] - PADDING) // TILE_SIZE, (self.pos[1] - HEADER_HEIGHT - PADDING) // TILE_SIZE):
                self.eat_sound.play()
                return True
        else:
            # Alinear a la cuadrícula si se choca con una pared
            if self.dir == [0, -1] or self.dir == [0, 1]:  # Movimiento vertical
                self.pos[0] = ((self.pos[0] - PADDING) // TILE_SIZE) * TILE_SIZE + PADDING
            else:  # Movimiento horizontal
                self.pos[1] = ((self.pos[1] - HEADER_HEIGHT - PADDING) // TILE_SIZE) * TILE_SIZE + HEADER_HEIGHT + PADDING
        return False

    def set_direction(self, direction):
        self.next_dir = direction

class Ghost:
    def __init__(self, maze):
        self.maze = maze
        self.pos = [9 * TILE_SIZE + PADDING, 9 * TILE_SIZE + HEADER_HEIGHT + PADDING]
        self.speed = 2
        self.dir = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.image = pygame.image.load("ghost.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def draw(self, screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))

    def can_move(self, new_pos):
        # Verificar las cuatro esquinas del sprite del fantasma
        corners = [
            (new_pos[0], new_pos[1]),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1]),
            (new_pos[0], new_pos[1] + TILE_SIZE - 1),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1] + TILE_SIZE - 1)
        ]
        for (x, y) in corners:
            if x < PADDING or x >= WIDTH + PADDING or y < HEADER_HEIGHT + PADDING or y >= HEIGHT + HEADER_HEIGHT + PADDING or self.maze.is_wall((x - PADDING) // TILE_SIZE, (y - HEADER_HEIGHT - PADDING) // TILE_SIZE):
                return False
        return True

    def move(self):
        # Detectar bifurcaciones y cambiar de dirección
        possible_directions = []
        if self.can_move([self.pos[0] + self.speed, self.pos[1]]):  # Derecha
            possible_directions.append([1, 0])
        if self.can_move([self.pos[0] - self.speed, self.pos[1]]):  # Izquierda
            possible_directions.append([-1, 0])
        if self.can_move([self.pos[0], self.pos[1] + self.speed]):  # Abajo
            possible_directions.append([0, 1])
        if self.can_move([self.pos[0], self.pos[1] - self.speed]):  # Arriba
            possible_directions.append([0, -1])

        # Si hay más de una dirección posible, eliminar la dirección opuesta actual
        if len(possible_directions) > 1:
            opposite_dir = [-self.dir[0], -self.dir[1]]
            if opposite_dir in possible_directions:
                possible_directions.remove(opposite_dir)
        
        # Cambiar de dirección si hay opciones disponibles
        if possible_directions:
            self.dir = random.choice(possible_directions)

        # Mover en la dirección actual
        new_pos = [self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed]
        if self.can_move(new_pos):
            self.pos = new_pos

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.maze = Maze()
        self.header = Header(self.maze.total_pills)
        self.eat_sound = pygame.mixer.Sound("chomp.wav")
        self.pacman = Pacman(self.maze, self.eat_sound)
        self.ghost = Ghost(self.maze)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pacman.set_direction([-1, 0])
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_direction([1, 0])
                    elif event.key == pygame.K_UP:
                        self.pacman.set_direction([0, -1])
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_direction([0, 1])

            # Mover Pac-Man
            if self.pacman.move():
                self.header.eat_pill()

            # Mover el fantasma
            self.ghost.move()

            # Limpiar la pantalla
            self.screen.fill(BACKGROUND_COLOR)

            # Dibujar el encabezado
            self.header.draw(self.screen)

            # Dibujar el laberinto
            self.maze.draw(self.screen)

            # Dibujar Pac-Man
            self.pacman.draw(self.screen)

            # Dibujar el fantasma
            self.ghost.draw(self.screen)

            # Actualizar la pantalla
            pygame.display.flip()

            # Controlar la velocidad del bucle
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
