import math
from game_components import Board, PlayerID, GameStatus
from algo import Algo

# This is a tunable parameter.
DEFAULT_DEPTH = 4

class MinimaxAlgo(Algo):
    def __init__(self, depth: int = DEFAULT_DEPTH):
        super().__init__(f"Minimax (Depth: {depth})")
        self.depth = depth

    def _evaluate_board(self, board: Board, player_id: PlayerID) -> int:
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

    def get_best_choice(self, board: Board, player_id: PlayerID) -> tuple[int, int | None]:
        """
        Public method to start the minimax calculation.
        """
        return self._minimax(board, self.depth, player_id)

    def _minimax(self, board: Board, depth: int, maximizing_player_id: PlayerID) -> tuple[int, int | None]:
        """
        Minimax algorithm to find the optimal move.
        Returns a tuple: (best_score, best_move_index).
        """
        # --- Base Cases ---
        if board.game_status != GameStatus.ONGOING:
            if board.game_status == GameStatus.PLAYER_ONE_WINS:
                return (math.inf if maximizing_player_id == PlayerID.PLAYER_ONE else -math.inf, None)
            elif board.game_status == GameStatus.PLAYER_TWO_WINS:
                return (-math.inf if maximizing_player_id == PlayerID.PLAYER_ONE else math.inf, None)
            else: # Draw
                return (0, None)

        if depth == 0:
            return (self._evaluate_board(board, maximizing_player_id), None)

        # --- Recursive Step ---
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return (self._evaluate_board(board, maximizing_player_id), None)

        best_move = legal_moves[0]

        if board.current_player == maximizing_player_id: # Maximizing player
            max_eval = -math.inf
            for move in legal_moves:
                next_board = board.make_move(move)
                current_eval, _ = self._minimax(next_board, depth - 1, maximizing_player_id)
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
            return max_eval, best_move
        else: # Minimizing player
            min_eval = math.inf
            for move in legal_moves:
                next_board = board.make_move(move)
                current_eval, _ = self._minimax(next_board, depth - 1, maximizing_player_id)
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
            return min_eval, best_move