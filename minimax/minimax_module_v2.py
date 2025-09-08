import math
from game_components import Board, PlayerID, GameStatus
from algo import Algo

# This is a tunable parameter.
DEFAULT_DEPTH = 4

class MinimaxAlgoV2(Algo):
    def __init__(self, depth: int = DEFAULT_DEPTH):
        super().__init__(f"Minimax (Depth: {depth})")
        self.depth = depth

    def _evaluate_board(self, board: Board, player_id: PlayerID) -> int:
        """
        A more advanced heuristic evaluation function.
        It considers silo score, on-board seeds, and stealing potential.
        """
        # --- Weights for each component (tune these to change AI behavior) ---
        W_SILO = 10.0  # Weight for seeds in the silo
        W_ON_BOARD = 1.0   # Weight for seeds still on the player's side
        W_STEAL_OFF = 2.0  # Weight for potential to steal from opponent
        W_STEAL_DEF = -2.0 # Weight for opponent's potential to steal from us

        # --- Basic Score Components ---
        my_silo_index = board.get_player_silo_index(player_id)
        opponent_id = (
            PlayerID.PLAYER_TWO if player_id == PlayerID.PLAYER_ONE else PlayerID.PLAYER_ONE
        )
        opponent_silo_index = board.get_player_silo_index(opponent_id)

        my_holes_range = board.get_player_holes_range(player_id)
        opponent_holes_range = board.get_player_holes_range(opponent_id)

        # Component 1: Silo score difference
        silo_score = board.board[my_silo_index] - board.board[opponent_silo_index]

        # Component 2: On-board seed difference
        my_seeds_on_board = sum(board.board[i] for i in my_holes_range)
        opponent_seeds_on_board = sum(board.board[i] for i in opponent_holes_range)
        on_board_score = my_seeds_on_board - opponent_seeds_on_board

        # --- Stealing Potential Score ---
        my_stealing_potential = 0
        opponent_stealing_potential = 0

        # My potential to steal from the opponent
        for my_hole_idx in my_holes_range:
            if board.board[my_hole_idx] == 0:
                opposite_idx = (2 * board.board_size) - my_hole_idx
                my_stealing_potential += board.board[opposite_idx]

        # Opponent's potential to steal from me
        for opp_hole_idx in opponent_holes_range:
            if board.board[opp_hole_idx] == 0:
                opposite_idx = (2 * board.board_size) - opp_hole_idx
                opponent_stealing_potential += board.board[opposite_idx]

        # --- Final Weighted Score ---
        final_score = (
            (W_SILO * silo_score) +
            (W_ON_BOARD * on_board_score) +
            (W_STEAL_OFF * my_stealing_potential) +
            (W_STEAL_DEF * opponent_stealing_potential)
        )
        
        # print('final score:', final_score)

        return int(final_score)

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