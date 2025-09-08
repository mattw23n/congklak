from game_components import Board, PlayerID, GameStatus
from minimax.minimax_module import MinimaxAlgo
from algo import Algo

available_algos = {
    "minimax": MinimaxAlgo(depth=4),
    "random": None
}

# --- Player Class (Decision Maker) ---
class Player:
    def __init__(self, player_id: PlayerID, algo: Algo | None = None):
        self.player_id = player_id
        self.algo = algo

    def choose_move(self, board: Board):
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None

        if self.algo:
            print(f"AI ({self.player_id.name}) is thinking using {self.algo.name}...")
            best_score, best_move = self.algo.get_best_choice(board, self.player_id)
            print(f"AI chose move {best_move} with an estimated score of {best_score}.")
            return best_move
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
    def __init__(self):
        self.board = Board(initial_seeds=7, board_size=7)
        self.players = {
            PlayerID.PLAYER_ONE: Player(PlayerID.PLAYER_ONE),
            PlayerID.PLAYER_TWO: Player(PlayerID.PLAYER_TWO),
        }
        self.available_algos = available_algos

    def _select_player_type(self, player_id: PlayerID):
        """Prompts user to select Human or AI for a player."""
        while True:
            choice = input(f"Select type for {player_id.name}: (1) Human, (2) AI: ").strip()
            if choice == '1':
                return None # No algorithm for Human
            elif choice == '2':
                # In the future, you can add more algo choices here
                print("Available AI algorithms:")
                for idx, algo_name in enumerate(self.available_algos.keys(), start=1):
                    print(f"({idx}) {algo_name}")
                algo_choice = input("Choose an AI algorithm by number: ").strip()
                try:
                    algo_index = int(algo_choice) - 1
                    algo_name = list(self.available_algos.keys())[algo_index]
                    print(f"{player_id.name} will use {algo_name} AI.")
                    return self.available_algos[algo_name]
                except (ValueError, IndexError):
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def setup_game(self):
        """Sets up the players (Human or AI) before starting."""
        print("--- Game Setup ---")
        p1_algo = self._select_player_type(PlayerID.PLAYER_ONE)
        self.players[PlayerID.PLAYER_ONE].algo = p1_algo

        p2_algo = self._select_player_type(PlayerID.PLAYER_TWO)
        self.players[PlayerID.PLAYER_TWO].algo = p2_algo
        print("="*20)


    def play(self):
        self.setup_game()
        print("Congklak Game Start!")
        while self.board.game_status == GameStatus.ONGOING:
            print(self.board)
            current_player_obj = self.players[self.board.current_player]
            print(f"Turn: {current_player_obj.player_id.name}")

            move = current_player_obj.choose_move(self.board)

            if move is None:
                print(f"{current_player_obj.player_id.name} has no moves. Turn skipped.")
                self.board.current_player = (
                    PlayerID.PLAYER_TWO
                    if self.board.current_player == PlayerID.PLAYER_ONE
                    else PlayerID.PLAYER_ONE
                )
                continue

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
    game = CongklakGame()
    game.play()