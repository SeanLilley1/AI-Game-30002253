import pygame
import random

pygame.init()

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Magenta = (255, 0, 255)
Cyan = (0, 255, 255)

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

Colours = [Red, Green, Blue, Yellow, Magenta, Cyan, White]

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, White, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, White, (0, y), (WINDOW_WIDTH, y))

def draw_shape(shape, offset, colour, screen):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                pygame.draw.rect(screen, colour, (offset[1] * CELL_SIZE + col * CELL_SIZE,
                                                    offset[0] * CELL_SIZE + row * CELL_SIZE,
                                                    CELL_SIZE, CELL_SIZE))

def place_shape(shape, offset, grid):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                grid[offset[0] + row][offset[1] + col] = 1