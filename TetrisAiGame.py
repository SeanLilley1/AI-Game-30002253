import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width, window_height = 500, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("AI plays tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Define the block shapes
SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]

# Define the colors for the blocks
COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]


class TetrisAI: #every function is held in the TetrisAI class
    def __init__(self):
        self.board_width = 10 #initialises the width for the grid
        self.board_height = 20 #initialises the height for the grid
        #sets the grid size based on the previous two variables
        self.board = [[BLACK] * self.board_width for _ in range(self.board_height)]
        self.current_shape = None #no current shape is made
        self.current_shape_rotation = 0 #will be used in rotating the shape
        self.current_shape_x = 0 #sets the x coord
        self.current_shape_y = 0 #sets the y coord
        self.score = 0 #set the score

    def reset(self): #This function will be called every time the game is over
        #resets all variables back to 0
        self.board = [[BLACK] * self.board_width for _ in range(self.board_height)]
        self.current_shape = None 
        self.current_shape_x = 0
        self.current_shape_y = 0
        self.score = 0

    def draw_board(self): #Draws the borders when initialised
        for y in range(self.board_height):
            for x in range(self.board_width):
                pygame.draw.rect(window, self.board[y][x], (x * 30, y * 30, 30, 30))

    def draw_shape(self): #Draws the shapes using the SHAPES array
        if self.current_shape is not None:
            shape = SHAPES[[self.current_shape][self.current_shape_rotation]][self.current_shape_rotation]
            for i in range(4): # down for figure
                for j in range(4): # across for figure
                    for k in range(4): # number of blocks in a shape
                        if shape[k] == (i*4 + j):
                            pygame.draw.rect(
                                window,
                                COLORS[self.current_shape],
                                (
                                    (self.current_shape_x + j) * 30,
                                    (self.current_shape_y + i) * 30,
                                    30,
                                    30,
                                ),
                            )

    def check_collision(self): #Will check collision with the borders and other shapes
        shape = SHAPES[[self.current_shape][self.current_shape_rotation]][self.current_shape_rotation]
        for y in range(4): # down for figure
            for x in range(4): # across for figure
                for k in range(4): # number of blocks in a shape
                    if (
                        shape[k] == (y*4 + x) #Sets the collided shapes as an object in the borders
                        and (
                            self.current_shape_x + x < 0
                            or self.current_shape_x + x >= self.board_width
                            or self.current_shape_y + y >= self.board_height
                            or self.board[self.current_shape_y + y][
                                self.current_shape_x + x
                            ]
                            != BLACK #changes the background from black to be filled by the shape colour
                        )
                    ):
                        return True
        return False

    def place_shape(self): #This is for the shapes falling and being placed in the grid
        shape = SHAPES[[self.current_shape][self.current_shape_rotation]][self.current_shape_rotation]
        print(shape)
        for i in range(4): # down for figure
            for j in range(4): # across for figure
                for k in range(4): # number of blocks in a shape
                    if shape[k] == (i*4 + j):
                         self.board[self.current_shape_y + i][self.current_shape_x + j] = COLORS[self.current_shape]
                        

    def check_lines(self): #Checks to see if a full line has been made
        lines_cleared = 0
        y = self.board_height - 1
        while y >= 0:
            if BLACK not in self.board[y]: #If so thenthe line will be set to black and the score goes up
                del self.board[y]
                self.board.insert(0, [BLACK] * self.board_width)
                lines_cleared += 1
            else:
                y -= 1
        self.score += lines_cleared ** 2

    def update(self): #Updates the game so a new shape is selected
        self.current_shape_y += 1
        if self.check_collision():
            self.current_shape_y -= 1
            self.place_shape()
            self.check_lines()
            self.current_shape = None

    def move_shape(self, direction): #For moving the shape on the grid
        new_x = self.current_shape_x + direction
        if (
            new_x >= 0 #take the x coord based on grid location and updates to new grid x location
            and new_x <= self.board_width - len(SHAPES[self.current_shape][0])
            and not self.check_collision() #Checks if the shape collides when moving
        ):
            self.current_shape_x = new_x

    def rotate_shape(self): #For rotating the shape on the grid
        new_shape = SHAPES[[self.current_shape][self.current_shape_rotation]] #create a new shape from the rotation based on the SHAPES array
        if (
            self.current_shape_x <= self.board_width - len(new_shape[0])
            and not self.check_collision()
        ):
            self.current_shape = (self.current_shape + 1) % len(SHAPES)
            self.current_shape_y += 1 

    def is_game_over(self):
        return any(
            color != BLACK for color in self.board[0]
        )  # Check if there is any colored block in the top row
    




# Create the AI instance
ai = TetrisAI()

# Set up the game clock
clock = pygame.time.Clock()

# AI Logic
AI_MOVE_DELAY = 10  # Delay between AI moves (in frames)
ai_move_counter = 0



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI Logic
    if ai.current_shape is None:
        ai.current_shape = random.randint(0, len(SHAPES) - 1)
        ai.current_shape_x = ai.board_width // 2 - len(SHAPES[ai.current_shape][0]) // 2
        ai.current_shape_y = 0
    else:
        # Make AI moves every AI_MOVE_DELAY frames
        if ai_move_counter >= AI_MOVE_DELAY:
            # Randomly choose an action: move left, move right, rotate, or do nothing
            action = random.choices(["left", "right", "rotate", "none"], weights=[0.1, 0.1, 0.0, 0.1], k=1)[0]
            if action == "left":
                ai.move_shape(-1)
            elif action == "right":
                ai.move_shape(1)
            elif action == "rotate":
                ai.rotate_shape()
            ai_move_counter = 0
        else:
            ai_move_counter += 1

    # Update game state
    ai.update()

    # Draw game board
    window.fill(BLACK)
    ai.draw_board()
    ai.draw_shape()

    # Check if game is over
    if ai.is_game_over():
        ai.reset()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(5)

# Quit the game
pygame.quit()