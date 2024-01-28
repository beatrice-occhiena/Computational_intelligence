"""
A minimax player for Quixo
"""

from game import Game, Player, Move
from quixo import Quixo
from copy import deepcopy
from tqdm.auto import tqdm


class MinimaxPlayer(Player):

    def __init__(self, depth: int=2) -> None:
        """
          Initializes the player

          - `depth`: The maximum number of levels or moves ahead 
            that the algorithm explores in the game tree to make its decision.
        """
        self.depth = depth

    def make_move(self, game: 'Quixo') -> tuple[tuple[int, int], Move]:
        """Returns the best action for the current player using minimax algorithm"""

        # 1. Get the current player and save it as the maximizing player
        minimax_player_id = game.get_current_player()
        maximizing_player = True

        # 2. Call minimax recursively for the current player
        _, best_action = self.minimax(game, self.depth, float('-inf'), float('inf'), maximizing_player, minimax_player_id)
        return best_action
    
    def minimax(self, game: 'Quixo', depth: int, alpha: int, beta: int, maximizing_player: bool, minimax_player_id: int) -> tuple[int, tuple[tuple[int, int], Move]]:
        """
        Minimax recursive algorithm for Quixo with alpha-beta pruning
        """

        # 0. TERMINAL CONDITIONS
        # If we have reached the maximum depth or the game is over
        winner = game.check_winner()
        if depth == 0 or winner != -1:
            # Return the heuristic value of the game state
            return self.evaluate(game, winner, minimax_player_id), None

        # 1. Get the possible actions for the current player
        possible_actions = game.get_possible_actions()

        # 2. If the current player is the MAXIMIZING PLAYER
        # *************************************************
        if maximizing_player:
            
            # 2.1. Initialize the best value and the best action
            best_value = float('-inf')
            best_action = None

            # 2.2. For each possible action
            for from_pos, slide in possible_actions:
                
                # 2.2.1. Make a copy of the game and perform the action
                game_copy = deepcopy(game)
                game_copy.make_move(from_pos, slide)

                # 2.2.2. Call minimax recursively for the opponent
                value, _ = self.minimax(game_copy, depth - 1, alpha, beta, False, minimax_player_id)

                # 2.2.3. If the value is better than the current best value
                if value > best_value:
                    best_value = value
                    best_action = (from_pos, slide)

                # 2.2.4. Update alpha
                alpha = max(alpha, best_value)

                # 2.2.5. Check if we can prune
                if best_value >= beta:
                    break
            
            # 2.3. Return the best value and the best action
            return best_value, best_action
        
        # 3. If the current player is the MINIMIZING PLAYER
        # *************************************************
        else:
            
            # 3.1. Initialize the best value and the best action
            best_value = float('inf')
            best_action = None

            # 3.2. For each possible action
            for from_pos, slide in possible_actions:
                
                # 3.2.1. Make a copy of the game and perform the action
                game_copy = deepcopy(game)
                game_copy.make_move(from_pos, slide)

                # 3.2.2. Call minimax recursively for the opponent
                value, _ = self.minimax(game_copy, depth - 1, alpha, beta, True, minimax_player_id)

                # 3.2.3. If the value is better than the current best value
                if value < best_value:
                    best_value = value
                    best_action = (from_pos, slide)
                
                # 3.2.4. Update beta
                beta = min(beta, best_value)
                
                # 3.2.5. Check if we can prune
                if best_value <= alpha:
                    break
            
            # 3.3. Return the best value and the best action
            return best_value, best_action

    def evaluate(self, game: 'Quixo', winner: int, minimax_player_id: int) -> int:
        """
        Heuristic function for Quixo
        """
        # A. Get the value for a winning/losing game
        # ..........................................
        if winner != -1:
            if winner == minimax_player_id:
                return 100
            else:
                return -100
            
        # B. Get the value for a game that is not over
        # ............................................
            
        # 1. Get the sequences of the current player and the opponent
        x_sequences, o_sequences = game.check_sequences()

        # 2. Get the sequences of the minimax player and its opponent
        if minimax_player_id == 0:
            player_sequences = x_sequences
            opponent_sequences = o_sequences
        else:
            player_sequences = o_sequences
            opponent_sequences = x_sequences
        
        # 3. Get the total score
        player_score = player_sequences[0] + player_sequences[1] * 3 + player_sequences[2] * 5
        opponent_score = opponent_sequences[0] + opponent_sequences[1] * 3 + opponent_sequences[2] * 5
        return player_score - opponent_score


