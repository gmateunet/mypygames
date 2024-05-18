import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Dimensiones del laberinto
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

# Crear laberinto
maze = [
    "####################",
    "#........#.........#",
    "#.####.###.####.###.#",
    "#.####.###.####.###.#",
    "#...................#",
    "#.####.#####.#####.#",
    "#.....#.....#.....#.#",
    "#####.#.###.#.###.#.#",
    "#.....#.#.#.#.#.#.#.#",
    "###.###.#.#.#.#.#.#.#",
    "#.................#.#",
    "#.###.###.###.###.#.#",
    "#.###.###.###.###.#.#",
    "#.....#.....#.....#.#",
    "####################",
]

# Posición inicial de Pac-Man
pacman_pos = [1 * TILE_SIZE, 1 * TILE_SIZE]
pacman_speed = 2
pacman_dir = [0, 0]

# Clase para manejar los fantasmas
class Ghost:
    def __init__(self, pos):
        self.pos = pos
        self.speed = 2
        self.dir = [0, 0]

    def move(self):
        directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        self.dir = random.choice(directions)
        new_pos = [self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed]
        if maze[new_pos[1] // TILE_SIZE][new_pos[0] // TILE_SIZE] != '#':
            self.pos = new_pos

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.pos, TILE_SIZE, TILE_SIZE))

# Crear fantasmas
ghosts = [Ghost([10 * TILE_SIZE, 10 * TILE_SIZE])]

# Función para dibujar el laberinto
def draw_maze(screen):
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == '#':
                pygame.draw.rect(screen, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif maze[row][col] == '.':
                pygame.draw.circle(screen, WHITE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), 5)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_dir = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                pacman_dir = [1, 0]
            elif event.key == pygame.K_UP:
                pacman_dir = [0, -1]
            elif event.key == pygame.K_DOWN:
                pacman_dir = [0, 1]

    # Mover Pac-Man
    new_pacman_pos = [pacman_pos[0] + pacman_dir[0] * pacman_speed, pacman_pos[1] + pacman_dir[1] * pacman_speed]
    if maze[new_pacman_pos[1] // TILE_SIZE][new_pacman_pos[0] // TILE_SIZE] != '#':
        pacman_pos = new_pacman_pos

    # Mover fantasmas
    for ghost in ghosts:
        ghost.move()

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar el laberinto
    draw_maze(screen)

    # Dibujar Pac-Man
    pygame.draw.circle(screen, YELLOW, (pacman_pos[0] + TILE_SIZE // 2, pacman_pos[1] + TILE_SIZE // 2), TILE_SIZE // 2)

    # Dibujar fantasmas
    for ghost in ghosts:
        ghost.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.delay(30)

# Salir de Pygame
pygame.quit()
