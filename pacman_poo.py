from globals import *
from maze_definition import Maze  # Importar la clase Maze

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

class Banner:
    def __init__(self, message, with_options=False):
        self.font = pygame.font.SysFont(None, 72)
        self.message = message
        self.with_options = with_options
        self.option_font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        banner_width = SCREEN_WIDTH // 2
        banner_height = SCREEN_HEIGHT // 4
        banner_x = (SCREEN_WIDTH - banner_width) // 2
        banner_y = (SCREEN_HEIGHT - banner_height) // 2

        pygame.draw.rect(screen, BLACK, (banner_x, banner_y, banner_width, banner_height), border_radius=20)
        pygame.draw.rect(screen, WHITE, (banner_x, banner_y, banner_width, banner_height), 5, border_radius=20)
        text = self.font.render(self.message, True, YELLOW)
        screen.blit(text, (banner_x + 20, banner_y + 20))

        if self.with_options:
            options_text = self.option_font.render("N: Nueva partida | S: Salir", True, WHITE)
            screen.blit(options_text, (banner_x + 20, banner_y + banner_height - 50))

class Pacman:
    def __init__(self, maze, header, eat_sound):
        self.maze = maze
        self.header = header
        self.pos = self.get_random_position()
        self.speed = 4
        self.dir = [0, 0]
        self.next_dir = [0, 0]
        self.eat_sound = eat_sound
        self.image = pygame.image.load("pacman.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.pills_eaten = 0  # Contador de píldoras comidas

    def get_random_position(self):
        col, row = self.maze.get_random_valid_position()
        x = col * TILE_SIZE + PADDING
        y = row * TILE_SIZE + HEADER_HEIGHT + PADDING
        return [x, y]

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
            if x < PADDING or x >= SCREEN_WIDTH - PADDING or y < HEADER_HEIGHT + PADDING or y >= SCREEN_HEIGHT - PADDING:
                return False
            if self.maze.is_wall((x - PADDING) // TILE_SIZE, (y - HEADER_HEIGHT - PADDING) // TILE_SIZE):
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
                self.pills_eaten += 1
                self.header.eat_pill()  # Actualizar el header
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
    def __init__(self, maze, pacman_pos):
        self.maze = maze
        self.pos = self.get_random_position(pacman_pos)
        self.speed = 2
        self.dir = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.image = pygame.image.load("ghost.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def get_random_position(self, pacman_pos):
        while True:
            col, row = self.maze.get_random_valid_position()
            x = col * TILE_SIZE + PADDING
            y = row * TILE_SIZE + HEADER_HEIGHT + PADDING
            if (x, y) != pacman_pos:
                return [x, y]

    def can_move(self, new_pos):
        # Verificar las cuatro esquinas del sprite del fantasma
        corners = [
            (new_pos[0], new_pos[1]),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1]),
            (new_pos[0], new_pos[1] + TILE_SIZE - 1),
            (new_pos[0] + TILE_SIZE - 1, new_pos[1] + TILE_SIZE - 1)
        ]
        for (x, y) in corners:
            if x < PADDING or x >= SCREEN_WIDTH - PADDING or y < HEADER_HEIGHT + PADDING or y >= SCREEN_HEIGHT - PADDING:
                return False
            if self.maze.is_wall((x - PADDING) // TILE_SIZE, (y - HEADER_HEIGHT - PADDING) // TILE_SIZE):
                return False
        return True

    def move(self):
        new_pos = [self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed]
        if not self.can_move(new_pos):
            self.dir = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        else:
            self.pos = new_pos

    def draw(self, screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    maze = Maze()
    header = Header(maze.total_pills)
    eat_sound = pygame.mixer.Sound("chomp.wav")
    pacman = Pacman(maze, header, eat_sound)
    ghosts = [Ghost(maze, pacman.pos)]  # Lista de fantasmas inicial
    banner = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if banner and banner.with_options:
                    if event.key == pygame.K_n:
                        main()  # Reiniciar el juego
                    elif event.key == pygame.K_s:
                        running = False
                else:
                    if event.key == pygame.K_UP:
                        pacman.set_direction([0, -1])
                    elif event.key == pygame.K_DOWN:
                        pacman.set_direction([0, 1])
                    elif event.key == pygame.K_LEFT:
                        pacman.set_direction([-1, 0])
                    elif event.key == pygame.K_RIGHT:
                        pacman.set_direction([1, 0])

        if not banner:
            pacman.move()

            # Añadir nuevo fantasma si Pac-Man ha comido 10 píldoras
            if pacman.pills_eaten % 10 == 0 and pacman.pills_eaten > 0 and len(ghosts) < (pacman.pills_eaten // 10):
                ghosts.append(Ghost(maze, pacman.pos))

            if header.pills_left == 0:
                banner = Banner("¡Has ganado!", with_options=True)

        screen.fill(BLACK)
        maze.draw(screen, TILE_SIZE, PADDING, HEADER_HEIGHT)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.move()
            ghost.draw(screen)
        header.draw(screen)
        if banner:
            banner.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
