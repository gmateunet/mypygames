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
BANNER_BACKGROUND = (50, 50, 50)  # Color de fondo del banner
BANNER_BORDER_COLOR = (255, 255, 255)  # Color del borde del banner
