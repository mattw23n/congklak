from enum import Enum

from minimax import minimax

# --- Enums (Unchanged) ---
class PlayerID(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class GameStatus(Enum):
    ONGOING = 0
    PLAYER_ONE_WINS = 1
    PLAYER_TWO_WINS = 2
    DRAW = 3

# --- The Core Game Engine: Board Class ---
class Board:
    def __init__(self, initial_seeds=7, board_size=7):
        self.board_size = board_size
        # Player 1 holes: 0-6, P1 silo: 7
        # Player 2 holes: 8-14, P2 silo: 15
        self.board = (
            [initial_seeds] * self.board_size
            + [0]
            + [initial_seeds] * self.board_size
            + [0]
        )
        self.current_player = PlayerID.PLAYER_ONE
        self.game_status = GameStatus.ONGOING

    def clone(self):
        """Creates a deep copy of the board state."""
        new_board = Board(0, self.board_size)
        new_board.board = list(self.board)
        new_board.current_player = self.current_player
        new_board.game_status = self.game_status
        return new_board

    def get_player_silo_index(self, player_id):
        return (
            self.board_size
            if player_id == PlayerID.PLAYER_ONE
            else len(self.board) - 1
        )

    def get_player_holes_range(self, player_id):
        if player_id == PlayerID.PLAYER_ONE:
            return range(0, self.board_size)
        else:
            return range(self.board_size + 1, len(self.board) - 1)

    def get_legal_moves(self):
        """Returns a list of legal moves (hole indices 0-6) for the current player."""
        legal_moves = []
        player_holes_range = self.get_player_holes_range(self.current_player)
        for i in player_holes_range:
            if self.board[i] > 0:
                legal_moves.append(i - player_holes_range.start)
        return legal_moves

    def make_move(self, hole_index):
        """
        Performs a move for the current player.
        Returns a NEW Board object with the updated state.
        The original board is NOT modified.
        """
        # 1. Validate the move
        legal_moves = self.get_legal_moves()
        if hole_index not in legal_moves:
            raise ValueError(f"Illegal move: {hole_index} is not in {legal_moves}")

        # 2. Create a new board state to modify (Immutability)
        next_board = self.clone()
        player_id = next_board.current_player
        player_holes_range = next_board.get_player_holes_range(player_id)
        real_index = hole_index + player_holes_range.start

        # 3. Perform the sowing logic
        print('hole_index:', hole_index)
        print('real_index:', real_index)
        
        last_sown_index = real_index
        seeds_to_sow = next_board.board[real_index]
        next_board.board[real_index] = 0

        while seeds_to_sow > 0:
            last_sown_index = (last_sown_index + 1) % len(next_board.board)
            if last_sown_index == next_board.get_player_silo_index(
                PlayerID.PLAYER_TWO
                if player_id == PlayerID.PLAYER_ONE
                else PlayerID.PLAYER_ONE
            ):
                continue
            next_board.board[last_sown_index] += 1
            seeds_to_sow -= 1

        # If the last seed lands in a non-empty hole (now > 1), continue sowing
        while next_board.board[last_sown_index] > 1 and last_sown_index != next_board.get_player_silo_index(player_id):
            seeds_to_sow = next_board.board[last_sown_index]
            next_board.board[last_sown_index] = 0
            while seeds_to_sow > 0:
                last_sown_index = (last_sown_index + 1) % len(next_board.board)
                if last_sown_index == next_board.get_player_silo_index(
                    PlayerID.PLAYER_TWO
                    if player_id == PlayerID.PLAYER_ONE
                    else PlayerID.PLAYER_ONE
                ):
                    continue
                next_board.board[last_sown_index] += 1
                seeds_to_sow -= 1

        # 4. Handle Capture ("Stealing") Logic
        player_silo_index = next_board.get_player_silo_index(player_id)
        if (
            next_board.board[last_sown_index] == 1
            and last_sown_index in player_holes_range
        ):
            opposite_index = (2 * self.board_size) - last_sown_index
            if next_board.board[opposite_index] > 0:
                stolen_seeds = next_board.board[opposite_index]
                next_board.board[opposite_index] = 0
                next_board.board[last_sown_index] = 0
                next_board.board[player_silo_index] += stolen_seeds + 1

        # 5. Determine the next player
        if last_sown_index == player_silo_index:
            # Player gets another turn, current_player remains the same
            pass
        else:
            next_board.current_player = (
                PlayerID.PLAYER_TWO
                if player_id == PlayerID.PLAYER_ONE
                else PlayerID.PLAYER_ONE
            )

        # 6. Check for game over condition and return the new state
        next_board._check_and_update_game_status()
        
        return next_board

    def _check_and_update_game_status(self):
        """Checks if the game has ended and updates the status and final scores."""
        p1_holes_range = self.get_player_holes_range(PlayerID.PLAYER_ONE)
        p2_holes_range = self.get_player_holes_range(PlayerID.PLAYER_TWO)

        p1_side_empty = all(self.board[i] == 0 for i in p1_holes_range)
        p2_side_empty = all(self.board[i] == 0 for i in p2_holes_range)

        if p1_side_empty or p2_side_empty:
            # Game ends, sweep remaining seeds into silos
            if p1_side_empty:
                p2_remaining = sum(self.board[i] for i in p2_holes_range)
                self.board[self.get_player_silo_index(PlayerID.PLAYER_TWO)] += p2_remaining
                for i in p2_holes_range:
                    self.board[i] = 0
            if p2_side_empty:
                p1_remaining = sum(self.board[i] for i in p1_holes_range)
                self.board[self.get_player_silo_index(PlayerID.PLAYER_ONE)] += p1_remaining
                for i in p1_holes_range:
                    self.board[i] = 0

            # Determine winner
            p1_score = self.board[self.get_player_silo_index(PlayerID.PLAYER_ONE)]
            p2_score = self.board[self.get_player_silo_index(PlayerID.PLAYER_TWO)]

            if p1_score > p2_score:
                self.game_status = GameStatus.PLAYER_ONE_WINS
            elif p2_score > p1_score:
                self.game_status = GameStatus.PLAYER_TWO_WINS
            else:
                self.game_status = GameStatus.DRAW

    def __str__(self):
        p2_holes_range = self.get_player_holes_range(PlayerID.PLAYER_TWO)
        p2_holes = self.board[p2_holes_range.start : p2_holes_range.stop]
        p2_str = " ".join(f"{h:2}" for h in reversed(p2_holes))
        p2_indices = " ".join(f"{i:2}" for i in reversed(range(self.board_size)))

        p1_holes_range = self.get_player_holes_range(PlayerID.PLAYER_ONE)
        p1_holes = self.board[p1_holes_range.start : p1_holes_range.stop]
        p1_str = " ".join(f"{h:2}" for h in p1_holes)
        p1_indices = " ".join(f"{i:2}" for i in range(self.board_size))

        p1_silo = self.board[self.get_player_silo_index(PlayerID.PLAYER_ONE)]
        p2_silo = self.board[self.get_player_silo_index(PlayerID.PLAYER_TWO)]

        board_width = len(p1_str)

        return (
            f"\n--- Player 2 (Holes {self.board_size-1}-{0}) ---\n"
            f"      {p2_str}\n"
            f"      {p2_indices}\n"
            f"P2 [{p2_silo:2}]" + " " * (board_width - 2) + f"[{p1_silo:2}] P1\n"
            f"      {p1_str}\n"
            f"      {p1_indices}\n"
            f"--- Player 1 (Holes {0}-{self.board_size-1}) ---\n"
        )

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
            # return legal_moves[0]
            return minimax(board, self.player_id)  # Placeholder for actual minimax call
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
            PlayerID.PLAYER_TWO: Player(PlayerID.PLAYER_TWO, is_ai=player_two_is_ai),
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