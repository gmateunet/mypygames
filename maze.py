import pygame

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40  # Tamaño de cada celda del laberinto
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Definición del laberinto
maze = [
    "###################.",
    "#........#..........",
    "#.####.###.####.###.",
    "#.####.###.####.###.",
    "....................",
    "#.####.#####.######.",
    "#.................#.",
    "#####.#.###.#.###.#.",
    "#.....#.#.#.#.#.#.#.",
    "###.###.#.#.#.#.#.#.",
    "#.................#.",
    "#.###.###.###.###.#.",
    "#.###.###.###.###.#.",
    "......#.....#.....#.",
    "###################.",
]

# Dimensiones del laberinto
ROWS = len(maze)
COLS = len(maze[0])

# Posición inicial de Pac-Man
pacman_pos = [1 * TILE_SIZE, 1 * TILE_SIZE]
pacman_speed = 4
pacman_dir = [0, 0]
next_dir = [0, 0]

# Reloj para controlar la tasa de fotogramas
clock = pygame.time.Clock()
FPS = 60  # Fotogramas por segundo

# Función para dibujar el laberinto
def draw_maze(screen):
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == '#':
                pygame.draw.rect(screen, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif maze[row][col] == '.':
                pygame.draw.circle(screen, WHITE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), 5)

# Función para verificar si Pac-Man puede moverse a la nueva posición
def can_move(new_pos):
    # Verificar las cuatro esquinas del sprite de Pac-Man
    corners = [
        (new_pos[0], new_pos[1]),
        (new_pos[0] + TILE_SIZE - 1, new_pos[1]),
        (new_pos[0], new_pos[1] + TILE_SIZE - 1),
        (new_pos[0] + TILE_SIZE - 1, new_pos[1] + TILE_SIZE - 1)
    ]
    for (x, y) in corners:
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or maze[y // TILE_SIZE][x // TILE_SIZE] == '#':
            return False
    return True

# Función para mover a Pac-Man
def move_pacman():
    global pacman_pos, pacman_dir, next_dir
    # Intentar cambiar la dirección si es posible
    new_pos = [pacman_pos[0] + next_dir[0] * pacman_speed, pacman_pos[1] + next_dir[1] * pacman_speed]
    if can_move(new_pos):
        pacman_dir = next_dir

    # Mover en la dirección actual
    new_pos = [pacman_pos[0] + pacman_dir[0] * pacman_speed, pacman_pos[1] + pacman_dir[1] * pacman_speed]
    if can_move(new_pos):
        pacman_pos = new_pos
    else:
        # Alinear a la cuadrícula si se choca con una pared
        pacman_pos[0] = (pacman_pos[0] // TILE_SIZE) * TILE_SIZE
        pacman_pos[1] = (pacman_pos[1] // TILE_SIZE) * TILE_SIZE

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_dir = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                next_dir = [1, 0]
            elif event.key == pygame.K_UP:
                next_dir = [0, -1]
            elif event.key == pygame.K_DOWN:
                next_dir = [0, 1]

    # Mover Pac-Man
    move_pacman()

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar el laberinto
    draw_maze(screen)

    # Dibujar Pac-Man
    pygame.draw.circle(screen, YELLOW, (pacman_pos[0] + TILE_SIZE // 2, pacman_pos[1] + TILE_SIZE // 2), TILE_SIZE // 2)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    clock.tick(FPS)

# Salir de Pygame
pygame.quit()
