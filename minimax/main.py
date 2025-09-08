from game_components import Board, PlayerID, GameStatus
from minimax_module import minimax

MAX_DEPTH = 4 # Tunable parameter for AI depth

# --- Player Class (Decision Maker) ---
class Player:
    def __init__(self, player_id, is_ai=False):
        self.player_id = player_id
        self.is_ai = is_ai

    def choose_move(self, board: Board):
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None # No moves possible

        if self.is_ai:
            # This is where you will plug in your AI algorithms!
            # For now, a simple AI: pick the first legal move.
            print(f"AI ({self.player_id.name}) is thinking...")
            return minimax(board, MAX_DEPTH, self.player_id)[1]
        else:
            # Human player input
            while True:
                try:
                    choice = int(
                        input(
                            f"{self.player_id.name}, choose a hole (0-{board.board_size - 1}): "
                        )
                    )
                    if choice in legal_moves:
                        return choice
                    else:
                        print(f"Invalid move. Please choose from {legal_moves}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

# --- Game Orchestrator ---
class CongklakGame:
    def __init__(self, player_one_is_ai=False, player_two_is_ai=True):
        self.board = Board(initial_seeds=7, board_size=7)
        self.players = {
            PlayerID.PLAYER_ONE: Player(PlayerID.PLAYER_ONE, is_ai=player_one_is_ai),
            PlayerID.PLAYER_TWO: Player(PlayerID.PLAYER_TWO, is_ai=True),
        }

    def play(self):
        print("Congklak Game Start!")
        while self.board.game_status == GameStatus.ONGOING:
            print(self.board)
            current_player_obj = self.players[self.board.current_player]
            print(f"Turn: {current_player_obj.player_id.name}")

            move = current_player_obj.choose_move(self.board)

            if move is None:
                print(f"{current_player_obj.player_id.name} has no moves. Turn skipped.")
                # Switch player manually if one side is stuck but game isn't over
                self.board.current_player = (
                    PlayerID.PLAYER_TWO
                    if self.board.current_player == PlayerID.PLAYER_ONE
                    else PlayerID.PLAYER_ONE
                )
                continue

            # The core update step: the current board is replaced by the new board state
            self.board = self.board.make_move(move)

        # Game Over
        print("\n" + "=" * 30)
        print("--- GAME OVER ---")
        print(self.board)
        print(f"Status: {self.board.game_status.name}")
        p1_score = self.board.board[self.board.get_player_silo_index(PlayerID.PLAYER_ONE)]
        p2_score = self.board.board[self.board.get_player_silo_index(PlayerID.PLAYER_TWO)]
        print(f"Final Score -> Player 1: {p1_score}, Player 2: {p2_score}")


if __name__ == "__main__":
    # To play, set player_one_is_ai=False
    game = CongklakGame(player_one_is_ai=False, player_two_is_ai=False)
    game.play()