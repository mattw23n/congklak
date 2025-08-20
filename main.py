from enum import Enum

# --- Enums for clarity ---
class PlayerID(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class GameStatus(Enum):
    ONGOING = 0
    PLAYER_ONE_WINS = 1
    PLAYER_TWO_WINS = 2
    DRAW = 3 # Unlikely in Congklak, but good to have

class Board:
    def __init__(self, initial_seeds=7, board_size=7):
        # Clockwise 1D array containing rows of holes & silos
        # Player 1's holes: 0-6, Player 2's holes: 8-14, silos at 7 and 15
        self.board = [initial_seeds] * board_size + [0] + [initial_seeds] * board_size + [0]
        self.board_size = board_size
        self.last_index = -1 # To track where the last seed was dropped

    def get_player_silo_index(self, player_id):
        return self.board_size if player_id == PlayerID.PLAYER_ONE else len(self.board) - 1

    def get_player_holes_range(self, player_id):
        if player_id == PlayerID.PLAYER_ONE:
            return range(0, self.board_size)
        else:
            return range(self.board_size + 1, len(self.board) - 1)
        
    def make_smaller_move(self, player_id, hole_index):
        """
        Make a move for the given player in the specified hole.
        Returns True if the move was successful, False otherwise.
        """
        curr_index = hole_index % len(self.board)
        
        seeds = self.board[curr_index]
        self.board[curr_index] = 0
        
        opponent_silo_index = self.get_player_silo_index(PlayerID.PLAYER_TWO if player_id == PlayerID.PLAYER_ONE else PlayerID.PLAYER_ONE)
        

        while seeds > 0:
            curr_index = (curr_index + 1) % len(self.board)
            # Skip the opponent's silo
            if curr_index == opponent_silo_index:
                continue
            self.board[curr_index] += 1
            seeds -= 1
        self.last_index = curr_index
        return True
    
    def make_move(self, player_id, hole_index):
        # Check for legal move
        player_holes_range = self.get_player_holes_range(player_id)
        real_index = hole_index + player_holes_range.start
        if not (real_index in player_holes_range and self.board[real_index] > 0):
            return False
        
        if current_player.player_id == PlayerID.PLAYER_TWO:
            hole_index += board.board_size + 1 # Adjust for Player 2's holes

        # Makes a first smaller move, keep making smaller moves until no seeds left
        if self.make_smaller_move(player_id, hole_index):
            while self.board[self.last_index] > 1 and self.last_index != self.get_player_silo_index(player_id):
                last_hole_index = self.last_index

                if not self.make_smaller_move(player_id, last_hole_index):
                    break
            
            # --- Stealing Logic ---
            player_silo_index = self.get_player_silo_index(player_id)
            player_holes = self.get_player_holes_range(player_id)

            # Check if the last seed landed in a previously empty hole (now has 1 seed) on the player's own side.
            if self.board[self.last_index] == 1 and self.last_index in player_holes:
                # Calculate the index of the opposite hole.
                # The board is symmetrical: hole 0 is opposite 14, 1 is opposite 13, etc.
                opposite_index = (2 * self.board_size) - self.last_index
                
                if self.board[opposite_index] > 0:
                    
                    # Take seeds from opponent's hole and the player's own landing hole.
                    stolen_seeds = self.board[opposite_index]
                    landing_seed = self.board[self.last_index] # This will always be 1
                    
                    print(f"Player {player_id.value} captures {stolen_seeds} seeds from the opposite hole!")

                    
                    self.board[opposite_index] = 0
                    self.board[self.last_index] = 0
                    
                    # Add all captured seeds to the player's silo.
                    self.board[player_silo_index] += stolen_seeds + landing_seed
            return True
        self.last_index = -1 # Reset last index if move failed
        return False
        
    def get_legal_moves(self, player_id):
        """Returns a list of legal moves (hole indices 0-6) for the player."""
        legal_moves = []
        player_holes_range = self.get_player_holes_range(player_id)
        for i in player_holes_range:
            if self.board[i] > 0:
                legal_moves.append(i - player_holes_range.start)
        return legal_moves
    
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
            f"Player 2 (Holes {self.board_size-1}-{0})\n"
            f"      {p2_str}\n"
            f"      {p2_indices}\n"
            f"P2 [{p2_silo:2}]" + " " * (board_width - 2) + f"[{p1_silo:2}] P1\n"
            f"      {p1_str}\n"
            f"      {p1_indices}\n"
            f"Player 1 (Holes {0}-{self.board_size-1})\n"
        )
            
        

# --- Player Class ---
class Player:
    def __init__(self, player_id, is_ai=False):
        self.player_id = player_id
        self.is_ai = is_ai

    def choose_move(self, board):
        if self.is_ai:
            # Placeholder for AI logic
            # For now, a very simple AI: pick the first legal move
            legal_moves = board.get_legal_moves(self.player_id)
            if legal_moves:
                return legal_moves[0] # Pick the first available move
            else:
                return -1 # No legal moves
        else:
            # Human player input
            while True:
                try:
                    hole_choice = int(input(f"Player {self.player_id.value}, choose a hole (0-{board.board_size - 1}): "))
                    if 0 <= hole_choice < board.board_size:
                        return hole_choice
                    else:
                        print(f"Invalid choice. Please choose a hole between 0 and {board.board_size - 1}.")
                except ValueError:
                    print(f"Invalid input. Please enter a number between 0 and {board.board_size - 1}.")


if __name__ == "__main__":
    # Example usage
    board = Board(initial_seeds=3, board_size=7)
    player1 = Player(PlayerID.PLAYER_ONE, is_ai=False)
    player2 = Player(PlayerID.PLAYER_TWO, is_ai=False)

    current_player = player1
    while True:
        print("\n" + "="*30)
        print(f"Player 1 Silo: {board.board[board.board_size]}")
        print(f"Player 2 Silo: {board.board[len(board.board) - 1]}")
        print(f"Board: \n {board}")
        print(f"Turn: Player {current_player.player_id.value}")
        
        if not board.get_legal_moves(current_player.player_id):
            print(f"Player {current_player.player_id.value} has no legal moves. Game over.")
            break

        move = current_player.choose_move(board)
        
        if board.make_move(current_player.player_id, move):
            print(f"Player {current_player.player_id.value} made a move in hole {move}.")
        else:
            print(f"Invalid move from hole {move}. Please try again.")
            continue # Let the same player try again
        
        # Switch players unless the last seed landed in the current player's silo
        player_silo = board.get_player_silo_index(current_player.player_id)
        if board.last_index == player_silo:
            print(f"Player {current_player.player_id.value} gets another turn!")
            continue
        
        current_player = player2 if current_player == player1 else player1
    