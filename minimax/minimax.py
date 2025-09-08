# ai.py
import math
from main import Board, PlayerID, GameStatus # Assuming your Board class is in board.py

# This is a tunable parameter. Start with 3 or 4.
# Higher values mean a stronger but much slower AI.
MAX_DEPTH = 4

def evaluate_board(board: Board, player_id: PlayerID) -> int:
    """
    A simple heuristic evaluation function.
    It calculates the score from the perspective of the given player_id.
    """
    my_silo_index = board.get_player_silo_index(player_id)
    opponent_id = (
        PlayerID.PLAYER_TWO if player_id == PlayerID.PLAYER_ONE else PlayerID.PLAYER_ONE
    )
    opponent_silo_index = board.get_player_silo_index(opponent_id)

    my_score = board.board[my_silo_index]
    opponent_score = board.board[opponent_silo_index]

    return my_score - opponent_score


def minimax(board: Board, depth: int, maximizing_player_id: PlayerID) -> tuple[int, int | None]:
    """
    Minimax algorithm to find the optimal move.
    Returns a tuple: (best_score, best_move_index).
    """
    # --- Base Cases: Stop recursion if... ---

    # 1. The game is over (a player has won or it's a draw)
    if board.game_status != GameStatus.ONGOING:
        if board.game_status == GameStatus.PLAYER_ONE_WINS:
            # Return a very high or low score depending on who the maximizer is
            return (math.inf if maximizing_player_id == PlayerID.PLAYER_ONE else -math.inf, None)
        elif board.game_status == GameStatus.PLAYER_TWO_WINS:
            return (-math.inf if maximizing_player_id == PlayerID.PLAYER_ONE else math.inf, None)
        else: # Draw
            return (0, None)

    # 2. The maximum search depth is reached
    if depth == 0:
        return (evaluate_board(board, maximizing_player_id), None)

    # --- Recursive Step ---

    legal_moves = board.get_legal_moves()
    if not legal_moves:
        # If a player has no moves, the game state might be terminal.
        # The board's internal logic should handle this, but we can evaluate.
        return (evaluate_board(board, maximizing_player_id), None)

    # Check if it's the MAXIMIZING player's turn
    if board.current_player == maximizing_player_id:
        max_eval = -math.inf
        best_move = legal_moves[0] # Default to the first move
        for move in legal_moves:
            # CRITICAL: Get the new board state from make_move's return value
            next_board = board.make_move(move)
            # The recursive call is for the NEXT state and DECREMENTED depth
            current_eval, _ = minimax(next_board, depth - 1, maximizing_player_id)

            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
        return max_eval, best_move

    # Otherwise, it's the MINIMIZING player's turn
    else:
        min_eval = math.inf
        best_move = legal_moves[0] # Default to the first move
        for move in legal_moves:
            # CRITICAL: Get the new board state from make_move's return value
            next_board = board.make_move(move)
            # The recursive call is for the NEXT state and DECREMENTED depth
            current_eval, _ = minimax(next_board, depth - 1, maximizing_player_id)

            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
        return min_eval, best_move