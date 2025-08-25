def minimax(board, player_id):
    
    if is_terminal_state(board):
        return value(board)
    
    # Maximizing player
    if player_id == 2:
        max_eval = float('-inf')
        for move in board.get_legal_moves(player_id):
            new_board = board.clone()
            new_board.make_move(move)
            eval = max(max_eval, minimax(new_board, 2))
        return eval
    
    # Minimizing player
    if player_id == 1:
        min_eval = float('inf')
        for move in board.get_legal_moves(player_id):
            new_board = board.clone()
            new_board.make_move(move)
            eval = min(min_eval, minimax(new_board, 1))
        return eval
    
def is_terminal_state(board):
    # Check if the game is over (no legal moves left)
    return len(board.get_legal_moves(board.current_player)) == 0

def value(board):
    # Simple evaluation function: difference in scores
    return -1