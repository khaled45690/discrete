#!/usr/bin/env python3
"""
Connect Four GUI using Pygame with Minimax + Alpha-Beta pruning AI
- Click a column to drop your piece (Player = RED)
- AI is YELLOW
- Command line options:
    python3 connect4_gui.py         # play against AI (default depth=4)
    python3 connect4_gui.py --depth 5  # set AI search depth

Install dependency:
    pip install -r requirements.txt

"""
import sys
import math
import random
import pygame
import time

# Game settings
ROWS = 8
COLS = 8
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS+1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
FPS = 60

# Pieces
EMPTY = 0
PLAYER = 1  # human (red)
AI = 2      # ai (yellow)

# Colors
BLUE = (28, 107, 160)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
YELLOW = (240, 220, 60)
WHITE = (255,255,255)

# RSA-like minimax helpers (alpha-beta) copied/adapted from previous script
WINDOW_LENGTH = 4

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def winning_move(board, piece):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # pos diag
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # neg diag
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

# Heuristic functions
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI
    count_piece = window.count(piece)
    count_empty = window.count(EMPTY)
    count_opp = window.count(opp_piece)
    if count_piece == 4:
        score += 100
    elif count_piece == 3 and count_empty == 1:
        score += 5
    elif count_piece == 2 and count_empty == 2:
        score += 2
    if count_opp == 3 and count_empty == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    # center column
    center_array = [board[r][COLS//2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3
    # horizontal
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLS)]
        for c in range(COLS-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # vertical
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # pos diag
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # neg diag
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

# Minimax with alpha-beta pruning
def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, AI)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [r.copy() for r in board]
            drop_piece(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Pygame drawing
def draw_board(screen, board):
    # Draw board background and holes. Draw rows normally so logical row 0
    # is at the top of the grid area (but the grid area itself starts
    # below the top hover bar). Pieces will stack from the bottom visually
    # because get_next_open_row fills higher row indices first.
    for c in range(COLS):
        for r in range(ROWS):
            x = int(c * SQUARESIZE + SQUARESIZE / 2)
            y = int((r + 1) * SQUARESIZE + SQUARESIZE / 2)
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (x, y), RADIUS)

    # Draw pieces using the same mapping so circles and holes align. The
    # logical bottom row (r == ROWS-1) will appear at the bottom of the
    # blue grid area.
    for c in range(COLS):
        for r in range(ROWS):
            x = int(c * SQUARESIZE + SQUARESIZE / 2)
            y = int((r + 1) * SQUARESIZE + SQUARESIZE / 2)
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, (x, y), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, (x, y), RADIUS)
    pygame.display.update()

def main(depth=4):
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Connect Four - Minimax AI')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('monospace', 36)

    board = create_board()
    # fill background white so overall background isn't black
    screen.fill(WHITE)
    game_over = False
    turn = random.choice([PLAYER, AI])

    print(f"Starting GUI game — AI depth={depth}. {'You' if turn==PLAYER else 'AI'} goes first.")
    while True:
        # refresh full background each frame so the window stays white
        screen.fill(WHITE)
        # draw a black top hover bar (the area above the grid)
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        draw_board(screen, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                # clear top hover area with black (matches desired image)
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                x_pos = event.pos[0]
                if turn == PLAYER and not game_over:
                    # draw hover circle on the black bar
                    pygame.draw.circle(screen, RED, (x_pos, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # restart
                    board = create_board()
                    game_over = False
                    turn = random.choice([PLAYER, AI])
                    pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                    draw_board(screen, board)
                    continue
                if turn == PLAYER:
                    x = event.pos[0]
                    col = int(math.floor(x/SQUARESIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER)
                        if winning_move(board, PLAYER):
                            label = font.render('You win!', 1, WHITE)
                            screen.blit(label, (40,10))
                            game_over = True
                        turn = AI
                        draw_board(screen, board)

        if not game_over and turn == AI:
            # AI move
            start = time.time()
            col, score = minimax(board, depth, -math.inf, math.inf, True)
            if col is None:
                valid = get_valid_locations(board)
                if not valid:
                    # draw
                    label = font.render('Draw!', 1, WHITE)
                    screen.blit(label, (40,10))
                    game_over = True
                else:
                    col = random.choice(valid)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI)
                if winning_move(board, AI):
                    label = font.render('AI wins!', 1, WHITE)
                    screen.blit(label, (40,10))
                    game_over = True
                draw_board(screen, board)
            end = time.time()
            # optional: show AI thinking time in console
            print(f"AI computed in {end-start:.2f}s, played column {col}")
            turn = PLAYER

        if game_over:
            pygame.display.update()
            # wait until player clicks to restart or closes
            time.sleep(0.5)

        clock.tick(FPS)

if __name__ == '__main__':
    depth = 4
    if '--depth' in sys.argv:
        try:
            idx = sys.argv.index('--depth')
            depth = int(sys.argv[idx+1])
        except Exception:
            pass
    main(depth=depth)
