from abc import ABC, abstractmethod
from game_components import Board, PlayerID

class Algo(ABC):
    """Abstract base class for all Congklak AI algorithms."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_best_choice(self, board: Board, player_id: PlayerID) -> tuple[int, int | None]:
        """
        Analyzes the board and returns the best move.

        Args:
            board: The current board state.
            player_id: The ID of the player making the move.

        Returns:
            A tuple containing (best_score, best_move).
            best_move can be None if no move is possible.
        """
        pass