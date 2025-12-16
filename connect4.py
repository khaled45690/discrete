#!/usr/bin/env python3
"""
Connect Four with Minimax + Alpha-Beta pruning (Python)
- Playable from terminal (human vs AI)
- `--test` runs an automated AI vs random player quick test

Usage:
  python3 connect4.py        # interactive human vs AI
  python3 connect4.py --test # automated AI vs random test (no input)

AI uses alpha-beta pruning minimax with a simple heuristic.
"""
import random
import sys
import time

ROWS = 8
COLS = 8
PLAYER = 1
AI = 2
EMPTY = 0
WINDOW_LENGTH = 4

# Board helpers
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

def print_board(board):
    # print so that bottom row is at bottom
    for r in range(ROWS):
        print('|', end='')
        for c in range(COLS):
            v = board[r][c]
            if v == PLAYER:
                ch = 'X'
            elif v == AI:
                ch = 'O'
            else:
                ch = ' '
            print(f" {ch} |", end='')
        print()
    print('  ' + '   '.join(map(str, range(COLS))))

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
    # positively sloped diag
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # negatively sloped diag
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

# Heuristic evaluation
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
    # Score center column
    center_array = [board[r][COLS//2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLS)]
        for c in range(COLS-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Vertical
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Positive diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # Negative diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -float('inf')
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = [r.copy() for r in board]
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

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
            else: # no more moves
                return (None, 0)
        else: # depth == 0
            return (None, score_position(board, AI))
    if maximizingPlayer:
        value = -float('inf')
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
        value = float('inf')
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

# Simple interactive game
def play_game(depth=4):
    board = create_board()
    game_over = False
    turn = random.choice([PLAYER, AI])
    print(f"Starting a new game — depth={depth}. {'You' if turn==PLAYER else 'AI'} goes first.")
    print_board(board)

    while not game_over:
        if turn == PLAYER:
            valid_cols = get_valid_locations(board)
            col = None
            while True:
                try:
                    inp = input('Your move (0-6): ')
                    col = int(inp)
                    if col in valid_cols:
                        break
                    else:
                        print('Invalid move, column full or out of range.')
                except Exception:
                    print('Please enter a valid column number 0-6.')
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER)
            if winning_move(board, PLAYER):
                print_board(board)
                print('You win!')
                game_over = True
            turn = AI
        else:
            print('AI is thinking...')
            col, minimax_score = minimax(board, depth, -float('inf'), float('inf'), True)
            if col is None:
                col = random.choice(get_valid_locations(board))
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI)
            print(f'AI played column {col}')
            if winning_move(board, AI):
                print_board(board)
                print('AI wins!')
                game_over = True
            turn = PLAYER
        print_board(board)
        if len(get_valid_locations(board)) == 0 and not game_over:
            print('Draw!')
            game_over = True

# Automated test: AI vs random for a few games
def automated_test(games=3, depth=4):
    print(f'Running automated test: AI(depth={depth}) vs Random — {games} games')
    results = {"AI":0, "Random":0, "Draw":0}
    for g in range(games):
        board = create_board()
        turn = random.choice([PLAYER, AI])
        while True:
            if turn == PLAYER:
                # random player
                valid = get_valid_locations(board)
                if not valid:
                    results['Draw'] += 1
                    break
                col = random.choice(valid)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER)
                if winning_move(board, PLAYER):
                    results['Random'] += 1
                    break
                turn = AI
            else:
                valid = get_valid_locations(board)
                if not valid:
                    results['Draw'] += 1
                    break
                col, score = minimax(board, depth, -float('inf'), float('inf'), True)
                if col is None:
                    col = random.choice(get_valid_locations(board))
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI)
                if winning_move(board, AI):
                    results['AI'] += 1
                    break
                turn = PLAYER
        print(f'Game {g+1}/{games} finished — current tally: {results}')
    print('Automated test complete.')
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # run quick automated test
        automated_test(games=5, depth=4)
    else:
        try:
            play_game(depth=4)
        except KeyboardInterrupt:
            print('\nExiting.')
