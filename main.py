import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Tiro Parabólico")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Parámetros del tiro parabólico
x0, y0 = 100, HEIGHT - 100  # Posición inicial
v0 = 50  # Velocidad inicial
angle = 45  # Ángulo de lanzamiento en grados
g = 9.81  # Aceleración de la gravedad

# Convertir ángulo a radianes
angle_rad = math.radians(angle)

# Componentes de la velocidad inicial
vx = v0 * math.cos(angle_rad)
vy = -v0 * math.sin(angle_rad)

# Tiempo inicial
t = 0
dt = 0.1  # Incremento de tiempo

# Lista para almacenar las posiciones del proyectil
trajectory = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcular posición del proyectil
    x = x0 + vx * t
    y = y0 + vy * t + 0.5 * g * t**2

    # Actualizar tiempo
    t += dt

    # Almacenar la posición actual en la lista de trayectoria
    trajectory.append((int(x), int(y)))

    # Limpiar la pantalla
    screen.fill(WHITE)

    # Dibujar el rastro del proyectil
    for pos in trajectory:
        pygame.draw.circle(screen, BLUE, pos, 3)

    # Dibujar el proyectil actual
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), 5)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.delay(30)

pygame.quit()
