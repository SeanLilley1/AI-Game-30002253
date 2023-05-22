import pygame
import random

pygame.init()

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

SHAPES = [
    [[1], [1], [1], [1]],
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[0, 1], [1, 1], [0, 1]],
    [[1, 0], [1, 1], [0, 1]],
    [[0, 1], [1, 1], [1, 0]],
    [[0, 1], [0, 1], [1, 1]],
    [[1, 1], [0, 1], [0, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0], [1, 1], [1, 0]],
    [[1, 0], [1, 1], [1, 0]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 0], [1, 0], [1, 1]],
    [[1, 1], [1, 0], [1, 0]]
]

COLOURS = [RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, WHITE]

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WINDOW_WIDTH, y))

def draw_shape(shape, offset, colour, screen):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                pygame.draw.rect(screen, colour, (offset[1] * CELL_SIZE + col * CELL_SIZE,
                                                  offset[0] * CELL_SIZE + row * CELL_SIZE,
                                                  CELL_SIZE, CELL_SIZE))

def rotate_shape(shape):
    num_rows = len(shape)
    num_cols = len(shape[0])
    rotated_shape = [[0] * num_rows for _ in range(num_cols)]
    
    for row in range(num_rows):
        for col in range(num_cols):
            rotated_shape[col][num_rows - 1 - row] = shape[row][col]
    
    return rotated_shape

def place_shape(shape, offset, grid):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] != 0:
                grid[offset[0] + row][offset[1] + col] = 1

def check_collision(shape, offset, grid):
    num_rows = len(shape)
    num_cols = len(shape[0])

    for row in range(num_rows):
        for col in range(num_cols):
            if shape[row][col] != 0:
                if (offset[0] + row >= GRID_HEIGHT or offset[1] + col < 0 or offset[1] + col >= GRID_WIDTH or
                        grid[offset[0] + row][offset[1] + col] != 0):
                    return True
    return False

def remove_completed_rows(grid):
    completed_rows = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            completed_rows.append(row)
            for r in range(row, 0, -1):
                grid[r] = grid[r - 1][:]
            grid[0] = [0] * GRID_WIDTH
    return completed_rows

def game_loop():

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_shape = random.choice(SHAPES)
    current_offset = [0, GRID_WIDTH // 2 - len(current_shape[0]) // 2]
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    new_offset = [current_offset[0], current_offset[1] - 1]
                    if not check_collision(current_shape, new_offset, grid):
                        current_offset = new_offset
                elif event.key == pygame.K_d:
                    new_offset = [current_offset[0], current_offset[1] + 1]
                    if not check_collision(current_shape, new_offset, grid):
                        current_offset = new_offset
                elif event.key == pygame.K_s:
                    new_offset = [current_offset[0] + 1, current_offset[1]]
                    if not check_collision(current_shape, new_offset, grid):
                        current_offset = new_offset
                elif event.key == pygame.K_r:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(rotated_shape, current_offset, grid):
                        current_shape = rotated_shape

        new_offset = [current_offset[0] + 1, current_offset[1]]
        if not check_collision(current_shape, new_offset, grid):
            current_offset = new_offset
        else:
            place_shape(current_shape, current_offset, grid)

            completed_rows = remove_completed_rows(grid)
            if completed_rows:
                score += len(completed_rows)

            if any(grid[0]):
                print("GAME OVER")
                print("YOUR SCORE: ", score)
                pygame.quit()
                return
            
            current_shape = random.choice(SHAPES)
            current_offset = [0, GRID_WIDTH // 2 - len(current_shape[0]) // 2]

        screen.fill(BLACK)

        draw_grid(screen)

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col] != 0:
                    pygame.draw.rect(screen, COLOURS[grid[row][col] - 1],
                                     (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        draw_shape(current_shape, current_offset, COLOURS[SHAPES.index(current_shape) % 7], screen)

        pygame.display.update()

        clock.tick(5)

game_loop()