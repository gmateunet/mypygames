import pygame
#https://bigsoundbank.com/
# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40  # Tamaño de cada celda del laberinto
FPS = 60  # Fotogramas por segundo

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

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
            "####################",
        ]
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == '#':
                    pygame.draw.rect(screen, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif self.maze[row][col] == '.':
                    pygame.draw.circle(screen, WHITE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), 5)

    def is_wall(self, x, y):
        return self.maze[y][x] == '#'
    
    def eat_pill(self, x, y):
        if self.maze[y][x] == '.':
            self.maze[y] = self.maze[y][:x] + ' ' + self.maze[y][x+1:]
            return True
        return False

class Pacman:
    def __init__(self, maze,eat_sound):
        self.maze = maze
        self.pos = [1 * TILE_SIZE, 1 * TILE_SIZE]
        self.speed = 4
        self.dir = [0, 0]
        self.next_dir = [0, 0]
        self.eat_sound = eat_sound


    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.pos[0] + TILE_SIZE // 2, self.pos[1] + TILE_SIZE // 2), TILE_SIZE // 2)

    def can_move(self, new_pos):
        # Verificar las cuatro esquinas del sprite de Pac-Man
        corners = [
            (new_pos[0], new_pos[1]),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1]),
            (new_pos[0], new_pos[1] + TILE_SIZE - 1),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1] + TILE_SIZE - 1)
        ]
        for (x, y) in corners:
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or self.maze.is_wall(x // TILE_SIZE, y // TILE_SIZE):
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
            if self.maze.eat_pill(self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE):
                self.eat_sound.play()
        else:
            # Alinear a la cuadrícula si se choca con una pared
            self.pos[0] = (self.pos[0] // TILE_SIZE) * TILE_SIZE
            self.pos[1] = (self.pos[1] // TILE_SIZE) * TILE_SIZE

    def set_direction(self, direction):
        self.next_dir = direction

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.maze = Maze()
        self.eat_sound = pygame.mixer.Sound("chomp.wav")
        self.pacman = Pacman(self.maze,self.eat_sound)


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
            self.pacman.move()

            # Limpiar la pantalla
            self.screen.fill(BLACK)

            # Dibujar el laberinto
            self.maze.draw(self.screen)

            # Dibujar Pac-Man
            self.pacman.draw(self.screen)

            # Actualizar la pantalla
            pygame.display.flip()

            # Controlar la velocidad del bucle
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
