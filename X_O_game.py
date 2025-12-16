first_diagonal_traversal = [(0,0),(1,1),(2,2)]
second_diagonal_traversal = [(0,2),(1,1),(2,0)]

def horizontal_traversal(num):
    max_val = 3
    list_indices = []
    for i in range(max_val):
        list_indices.append((num,i))
    return list_indices

def vertical_traversal(num):
    max_val = 3
    list_indices = []
    for i in range(max_val):
        list_indices.append((i,num))
    return list_indices

def check_winner(board):
    """Check if there's a winner on the board"""
    # Check all rows
    for i in range(3):
        row = horizontal_traversal(i)
        if board[row[0][0]][row[0][1]] == board[row[1][0]][row[1][1]] == board[row[2][0]][row[2][1]] != ' ':
            return board[row[0][0]][row[0][1]]
   
    # Check all columns
    for i in range(3):
        col = vertical_traversal(i)
        if board[col[0][0]][col[0][1]] == board[col[1][0]][col[1][1]] == board[col[2][0]][col[2][1]] != ' ':
            return board[col[0][0]][col[0][1]]
   
    # Check first diagonal
    if board[first_diagonal_traversal[0][0]][first_diagonal_traversal[0][1]] == \
       board[first_diagonal_traversal[1][0]][first_diagonal_traversal[1][1]] == \
       board[first_diagonal_traversal[2][0]][first_diagonal_traversal[2][1]] != ' ':
        return board[first_diagonal_traversal[0][0]][first_diagonal_traversal[0][1]]
   
    # Check second diagonal
    if board[second_diagonal_traversal[0][0]][second_diagonal_traversal[0][1]] == \
       board[second_diagonal_traversal[1][0]][second_diagonal_traversal[1][1]] == \
       board[second_diagonal_traversal[2][0]][second_diagonal_traversal[2][1]] != ' ':
        return board[second_diagonal_traversal[0][0]][second_diagonal_traversal[0][1]]
   
    return None

def is_board_full(board):
    """Check if the board is full"""
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True

def get_empty_cells(board):
    """Get list of empty cells"""
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                empty_cells.append((i,j))
    return empty_cells

def minimax(board, depth, is_maximizing, player, opponent):
    """
    Minimax algorithm implementation
    board: current game board state
    depth: current depth in game tree
    is_maximizing: True if maximizing player's turn, False otherwise
    player: symbol for AI player (typically 'O')
    opponent: symbol for human player (typically 'X')
    """
    winner = check_winner(board)
   
    # Base cases
    if winner == player:
        return 10 - depth
    if winner == opponent:
        return depth - 10
    if is_board_full(board):
        return 0
   
    if is_maximizing:
        max_eval = float('-inf')
        empty_cells = get_empty_cells(board)
       
        for cell in empty_cells:
            i, j = cell
            board[i][j] = player
            eval_score = minimax(board, depth + 1, False, player, opponent)
            board[i][j] = ' '
            max_eval = max(max_eval, eval_score)
       
        return max_eval
    else:
        min_eval = float('inf')
        empty_cells = get_empty_cells(board)
       
        for cell in empty_cells:
            i, j = cell
            board[i][j] = opponent
            eval_score = minimax(board, depth + 1, True, player, opponent)
            board[i][j] = ' '
            min_eval = min(min_eval, eval_score)
       
        return min_eval

def find_best_move(board, player, opponent):
    """
    Find the best move for the AI player
    Returns tuple (row, col) of best move
    """
    best_score = float('-inf')
    best_move = None
    empty_cells = get_empty_cells(board)
   
    for cell in empty_cells:
        i, j = cell
        board[i][j] = player
        score = minimax(board, 0, False, player, opponent)
        board[i][j] = ' '
       
        if score > best_score:
            best_score = score
            best_move = (i, j)
   
    return best_move

def print_board(board):
    """Print the board in a readable format"""
    print("\n  0   1   2")
    for i in range(3):
        print(f"{i} {board[i][0]} | {board[i][1]} | {board[i][2]}")
        if i < 2:
            print("  ---------")
    print()

def initialize_random_board():
    """Randomly initialize the board with 0-2 moves"""
    import random
    board = [[' ' for _ in range(3)] for _ in range(3)]
   
    # Randomly decide how many initial moves (0, 1, or 2)
    num_moves = random.randint(0, 2)
   
    for move_num in range(num_moves):
        while True:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if board[i][j] == ' ':
                # Alternate between X and O
                board[i][j] = 'X' if move_num % 2 == 0 else 'O'
                break
   
    return board

def get_user_move(board):
    """Get valid move from user"""
    while True:
        try:
            move = input("Enter your move (row col): ").strip().split()
            if len(move) != 2:
                print("Please enter row and column separated by space")
                continue
           
            row, col = int(move[0]), int(move[1])
           
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Row and column must be between 0 and 2")
                continue
           
            if board[row][col] != ' ':
                print("That cell is already occupied")
                continue
           
            return (row, col)
        except ValueError:
            print("Please enter valid numbers")
        except KeyboardInterrupt:
            print("\nGame ended by user")
            exit()

# Example usage
if __name__ == "__main__":
    import random
   
    # Initialize random board
    board = initialize_random_board()
   
    print("Welcome to Tic-Tac-Toe!")
    print("You are X, AI is O")
    print_board(board)
   
    # Determine who goes first based on current state
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    user_turn = x_count <= o_count
   
    # Game loop
    while True:
        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            print_board(board)
            break
       
        if is_board_full(board):
            print("It's a draw!")
            print_board(board)
            break
       
        if user_turn:
            # User's turn
            print("Your turn:")
            row, col = get_user_move(board)
            board[row][col] = 'X'
            print_board(board)
            user_turn = False
        else:
            # AI's turn
            print("AI is thinking...")
            best_move = find_best_move(board, 'O', 'X')
            if best_move:
                board[best_move[0]][best_move[1]] = 'O'
                print(f"AI plays at {best_move}")
                print_board(board)
            user_turn = True