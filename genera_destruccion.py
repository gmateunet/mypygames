import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial de Pygame")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BRICK_OUTLINE = (0, 0, 0)

# Posición y tamaño del rectángulo
rect_x = WIDTH // 2 - 50
rect_y = HEIGHT - 30
rect_w = 100
rect_h = 20
rect_speed = 10  # Velocidad del rectángulo

# Posición y radio de la bola
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 15

# Velocidad inicial de la bola
initial_ball_speed = 4

# Velocidad de la bola
ball_speed_x = initial_ball_speed * random.choice([-1, 1])
ball_speed_y = initial_ball_speed * random.choice([-1, 1])

# Incremento de velocidad después de cada colisión con el rectángulo
speed_increment = 0.5

# Dimensiones de los ladrillos
brick_rows = 5
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 30

# Cargar la textura del ladrillo
brick_texture = pygame.image.load("brick_texture.png")
brick_texture = pygame.transform.scale(brick_texture, (brick_width, brick_height))

# Clase para manejar los fragmentos de los ladrillos
class BrickFragment:
    def __init__(self, image, pos, speed):
        self.image = image
        self.pos = pos
        self.speed = speed

    def update(self):
        self.pos[1] += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.pos)

# Clase para los ladrillos con animación de destrucción
class Brick:
    def __init__(self, rect):
        self.rect = rect
        self.destroyed = False
        self.fragments = []

    def destroy(self):
        self.destroyed = True
        num_pieces = 6
        piece_width = self.rect.width // 3
        piece_height = self.rect.height // 2
        for j in range(num_pieces):
            piece = brick_texture.subsurface(
                (j % 3) * piece_width, (j // 3) * piece_height, piece_width, piece_height
            )
            pos = [self.rect.left + (j % 3) * piece_width, self.rect.top + (j // 3) * piece_height]
            speed = random.randint(2, 5)
            self.fragments.append(BrickFragment(piece, pos, speed))

    def update(self):
        if self.destroyed:
            for fragment in self.fragments:
                fragment.update()
            self.fragments = [f for f in self.fragments if f.pos[1] < HEIGHT]

    def draw(self, screen):
        if not self.destroyed:
            screen.blit(brick_texture, self.rect.topleft)
            pygame.draw.rect(screen, BRICK_OUTLINE, self.rect, 2)
        else:
            for fragment in self.fragments:
                fragment.draw(screen)

# Crear ladrillos intercalados
bricks = []
for row in range(brick_rows):
    offset = (brick_width // 2) if (row % 2 != 0) else 0
    for col in range(brick_cols):
        brick_x = col * brick_width + offset
        if brick_x + brick_width > WIDTH:
            continue
        brick_y = row * brick_height
        bricks.append(Brick(pygame.Rect(brick_x, brick_y, brick_width, brick_height)))

# Cargar el sonido de rebote
bounce_sound = pygame.mixer.Sound("bounce.wav")

# Cargar el sonido de explosión
explosion_sound = pygame.mixer.Sound("explosion.wav")

def check_collision(rect, ball_x, ball_y, ball_radius):
    return rect.collidepoint(ball_x, ball_y)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rect_x > 0:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT] and rect_x < WIDTH - rect_w:
        rect_x += rect_speed

    # Actualizar la posición de la bola
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Verificar colisión de la bola con los límites de la pantalla
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_x *= -1
        bounce_sound.play()  # Reproducir sonido en el rebote lateral

    if ball_y - ball_radius <= 0:
        ball_speed_y *= -1
        bounce_sound.play()  # Reproducir sonido en el rebote superior

    # Verificar colisión de la bola con el rectángulo
    paddle_rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
    if check_collision(paddle_rect, ball_x, ball_y, ball_radius):
        ball_speed_y *= -1  # Cambiar solo la dirección vertical para simular un rebote en la parte superior del rectángulo
        ball_y = rect_y - ball_radius  # Reubicar la bola justo por encima del rectángulo para evitar múltiples colisiones
        bounce_sound.play()  # Reproducir sonido en el rebote con el rectángulo
        
        # Incrementar la velocidad de la bola
        if ball_speed_x > 0:
            ball_speed_x += speed_increment
        else:
            ball_speed_x -= speed_increment

        if ball_speed_y > 0:
            ball_speed_y += speed_increment
        else:
            ball_speed_y -= speed_increment

    # Verificar colisión de la bola con los ladrillos
    for brick in bricks:
        if not brick.destroyed and check_collision(brick.rect, ball_x, ball_y, ball_radius):
            brick.destroy()
            ball_speed_y *= -1  # Cambiar solo la dirección vertical
            bounce_sound.play()  # Reproducir sonido en el rebote con el ladrillo

    # Actualizar los ladrillos
    for brick in bricks:
        brick.update()

    # Si la bola cae por debajo del rectángulo (game over scenario)
    if ball_y + ball_radius >= HEIGHT:
        explosion_sound.play()  # Reproducir sonido de explosión en game over
        pygame.time.delay(1000)  # Esperar un segundo para que el sonido se reproduzca completamente
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x = initial_ball_speed * random.choice([-1, 1])
        ball_speed_y = initial_ball_speed * random.choice([-1, 1])

    # Limpiar la pantalla
    screen.fill(WHITE)

    # Dibujar el rectángulo
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_w, rect_h))

    # Dibujar la bola en el centro
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

    # Dibujar los ladrillos
    for brick in bricks:
        brick.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.delay(30)

# Salir de Pygame
pygame.quit()
