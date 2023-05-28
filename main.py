import random
import pygame

# Game settings
width = 10
height = 10
num_mines = 10

# Initialize pygame
pygame.init()

# Display settings
cell_width = 40
cell_height = 40
screen_width = width * cell_width
screen_height = height * cell_height

# Color settings
BACKGROUND_COLOR = (192, 192, 192)
CLOSED_CELL_COLOR = (192, 192, 192)
OPEN_CELL_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
MINE_COLOR = (0, 0, 0)
NUMBER_COLOR = (0, 0, 255)
FLAG_COLOR = (255, 0, 0)

# Game state
finish_game = False
game_over = False
board = [[0] * width for _ in range(height)]
revealed = [[False] * width for _ in range(height)]
flagged = [[False] * width for _ in range(height)]

# Pygame setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minesweeper')
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 30)
menu_font = pygame.font.SysFont(None, 30)

# Load images
mine_image = pygame.image.load('mine.png')
mine_image = pygame.transform.scale(mine_image, (cell_width - 4, cell_height - 4))
flag_image = pygame.image.load('flag.png')
flag_image = pygame.transform.scale(flag_image, (cell_width - 4, cell_height - 4))

# Function to draw the game board
def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for y in range(height):
        for x in range(width):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, CLOSED_CELL_COLOR, cell)

            if revealed[y][x]:
                pygame.draw.rect(screen, OPEN_CELL_COLOR, cell)
                if board[y][x] == -1:
                    screen.blit(mine_image, (x * cell_width + 2, y * cell_height + 2))
                elif board[y][x] > 0:
                    number_text = font.render(str(board[y][x]), True, NUMBER_COLOR)
                    number_rect = number_text.get_rect(center=(x * cell_width + cell_width // 2, y * cell_height + cell_height // 2))
                    screen.blit(number_text, number_rect)

            if flagged[y][x]:
                pygame.draw.rect(screen, FLAG_COLOR, cell)
                screen.blit(flag_image, (x * cell_width + 2, y * cell_height + 2))

    pygame.display.flip()

# Function to place the mines on the board
def place_mines():
    mines_placed = 0
    while mines_placed < num_mines:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if board[y][x] != -1:
            board[y][x] = -1
            mines_placed += 1

# Function to count the number of neighboring mines for each cell
def count_neighbor_mines():
    for y in range(height):
        for x in range(width):
            if board[y][x] != -1:
                count = 0
            for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (i != 0 or j != 0) and 0 <= y + i < height and 0 <= x + j < width:
                                if board[y + i][x + j] == -1:
                                    count += 1
            board[y][x] = count

# Function to reveal empty cells
def reveal_empty_cells(x, y):
    if not 0 <= y < height or not 0 <= x < width or revealed[y][x]:
        return

    revealed[y][x] = True

    if board[y][x] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                reveal_empty_cells(x + j, y + i)

# Function to handle cell clicks
def handle_cell_click(x, y):
    global game_over
    if flagged[y][x] or revealed[y][x]:
        return

    if board[y][x] == -1:
        game_over = True
    else:
        reveal_empty_cells(x, y)

# Function to handle flagging/unflagging cells
def handle_cell_flag(x, y):
    if revealed[y][x]:
        return

    flagged[y][x] = not flagged[y][x]

# Function to handle game restart
def restart_game():
    global finish_game, game_over, board, revealed, flagged
    finish_game = False
    game_over = False
    board = [[0] * width for _ in range(height)]
    revealed = [[False] * width for _ in range(height)]
    flagged = [[False] * width for _ in range(height)]
    place_mines()
    count_neighbor_mines()

# Function to display game over message
def show_game_over_message():
    text = menu_font.render('Game Over!', True, TEXT_COLOR)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    restart_text = font.render('Press R to Restart', True, TEXT_COLOR)
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(restart_text, restart_rect)

# Function to display game won message
def show_game_won_message():
    text = menu_font.render('You Win!', True, TEXT_COLOR)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    restart_text = font.render('Press R to Restart', True, TEXT_COLOR)
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(restart_text, restart_rect)

# Game menu
def game_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        start_text = menu_font.render('Start Game', True, TEXT_COLOR)
        start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_text, start_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_text_rect.collidepoint(event.pos):
                    restart_game()
                    game_loop()

        pygame.display.flip()

# Game loop
def game_loop():
    global finish_game
    while not finish_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    x, y = event.pos
                    x = x // cell_width
                    y = y // cell_height
                    if event.button == 1:
                        handle_cell_click(x, y)
                    elif event.button == 3:
                        handle_cell_flag(x, y)

        draw_board()

        if game_over:
            show_game_over_message()
        elif all(all(revealed_row) for revealed_row in revealed):
            show_game_won_message()

        pygame.display.flip()
        clock.tick(60)

# Run the game menu
game_menu()

# Quit the game
pygame.quit()


               
