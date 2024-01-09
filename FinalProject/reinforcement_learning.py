"""
reinforcement_learning.py

This file contains the code for the reinforcement learning algorithm used to create
"""

from game import Game, Move, Player
from main import RandomPlayer
from symmetry import SymmetryGenerator
from quixo import Quixo
from random import choice, random
from abc import abstractmethod
from tqdm.auto import tqdm

class RL_Player(Player):
    
    def __init__(self, epsilon=0.1, alpha=0.2, gamma=0.9, e_decay=0.9999, e_min=0.01) -> None:
        super().__init__()

        # Parameters
        self.epsilon = epsilon    # Exploration rate
        self.alpha = alpha        # Learning rate
        self.gamma = gamma        # Discount rate
        self.e_decay = e_decay    # Exploration decay rate
        self.e_min = e_min        # Minimum exploration rate

        # Structures
        self.q_table = {}        # Q(s, a)
        self.q_counters = {}     # N(s, a)
    
    def make_move(self, game: 'Quixo') -> tuple[tuple[int, int], Move]:
        """Select a move based on the learned policy"""
        from_pos, slide, _ = self._get_action(game)

    def _get_base_state(self, game: 'Quixo') -> tuple[str, str]:
        """ 
        Returns:
        1. the `label` of the transformation applied to the board
        2. the hashable equivalent of the board `base state`

        If this method is called when the current player is O(1),
        the copy of the board is first transformed to the pov of player X(0)
        before generating the base state:
        - cells with value 0 become 1
        - cells with value 1 become 0

        This is done to make sure that the strategy learned by the agent is the same
        regardless of the player it is playing as.
        
        => Therefore, in the Q-table, the states are always saved from the pov of player X(0).
        """

        # 1. Get a copy of the current board
        current_board = game.get_board()

        # 2. Check if the player is O
        player_is_O = game.get_current_player() == 1

        # 3. If the player is O, transform the board to take the pov of player X
        if player_is_O:
            for i in range(5):
                for j in range(5):
                    current_board[i][j] = (1 - current_board[i][j]) if current_board[i][j] in [0, 1] else current_board[i][j]
            
        # 4. Generate the base state of the current board
        SG = SymmetryGenerator()
        transf_label, board_base_state = SG.get_base_state(current_board)

        # 5. Return the values
        return transf_label, str(board_base_state)
    
    def _get_action(self, game: 'Quixo', training_phase: bool=False):
        """
        Find the best action to perform balancing exploration and exploitation.

        Returns:
        1. the position of the piece to move
        2. the direction in which to move it
        3. the base state and best base action (used to update the Q-table)
        """

        # 1. Get all possible actions based on the current game state
        possible_actions = game.get_possible_actions()

        # 2. EXLORATION: Choose a random action (only during training)
        if training_phase and random() < self.epsilon:
            return choice(possible_actions)
        
        # 4. EXPLOITATION: Choose the action with the highest Q-value
        else:
            
            # 4.0. Set the symmetry generator
            SG = SymmetryGenerator()
            
            # 4.1. Get the hashable base state of the current board and the transformation applied
            transf_label, base_state = self._get_base_state(game)

            # 4.2. Transform the actions to base actions
            base_actions = []
            for from_pos, slide in possible_actions:
                base_actions.append(SG.get_base_action(from_pos, slide, transf_label))

            # 4.3. Get the Q-values of the base actions
            q_values = []
            for base_action in base_actions:
                q_values.append(self.q_table.get((base_state, base_action), 0))

            # 4.4. Get the action with the highest Q-value
            max_q_value = max(q_values)
            max_q_value_idx = q_values.index(max_q_value)
            best_base_action = base_actions[max_q_value_idx]

            # 4.5. Transform the action to the original action to be used in the game
            best_action = SG.get_original_action(best_base_action[0], best_base_action[1], transf_label)
            from_pos, slide = best_action

            # 4.6. Return all the necessary values
            return from_pos, slide, (base_state, best_base_action)

    def _get_action_reward(self, game: 'Quixo', action: tuple[tuple[int, int], Move]) -> int:
        """Returns the reward of the given action"""
        #TODO
        reward = 0        
        return reward
    
    def _get_end_reward(self, rl_player_id: int, winner: int) -> int:
        """Get the reward based on the winner of the game"""
        # 1. Give a big positive reward if the RL player wins
        if winner == rl_player_id:
            return 10
        # 2. Do not give any reward if there is no winner
        elif winner == -1:
            return 0
        # 3. Give a big negative reward if the RL player loses
        else:
            return -10

    @abstractmethod
    def _update_q_table(self, state: tuple[str, str], action: tuple[tuple[int, int], Move], reward: int, next_state: tuple[str, str]):
        """Update the Q-table"""
        pass
    
    @abstractmethod
    def train(self, episodes: int = 1000, verbose: bool = False):
        """Train the agent for the given number of episodes"""
        pass
    
    def _save_q_table(self, path: str):
        """Save the Q-table to a file to retrieve it later"""
        with open(path, "w") as f:
            for key, value in self.q_table.items():
                f.write(f"{key[0]},{key[1][0]},{key[1][1]},{value}\n")

class MonteCarloPlayer(RL_Player):
    
    def __init__(self, epsilon=0.3, alpha=0.2, gamma=0.9, e_decay=0.999, e_min=0.01) -> None:
        super().__init__(epsilon, alpha, gamma, e_decay, e_min)

    def _update_q_table(self, trajectory):
        """Update the Q-table based on the trajectory of the episode"""
        # 1. Initialize the return
        G = 0

        # 2. Iterate over the trajectory in reverse order
        for base_state, base_action, reward in reversed(trajectory):

            # 2.1. Update the return
            G = self.gamma * G + reward

            # 2.2. Update the Q-value
            if (base_state, base_action) not in self.q_table:
                # Initialize the Q-value
                self.q_counters[(base_state, base_action)] = 0
                self.q_table[(base_state, base_action)] = 0.0
            
            self.q_counters[(base_state, base_action)] += 1
            self.q_table[(base_state, base_action)] += self.learning_rate * (G - self.q_table[(base_state, base_action)]) / self.q_counters[(base_state, base_action)]

    def train(self, episodes: int = 1000):
        
        # 0. Initialize the symmetry generator
        SG = SymmetryGenerator()

        # 1. Define the players
        mc_player = self
        mc_player_id = 0
        random_player = RandomPlayer()
        players = (mc_player, random_player)

        # 2. Play the given number of episodes (games)
        for _ in tqdm(range(episodes)):

            # 2.1. Initialize the game
            game = Quixo()
            winner = -1

            # 2.2. Initialize the episode
            reward_counter = 0    # Total reward of the episode
            trajectory = []       # List of (state, action, reward) tuples representing the steps of the episode
            players = (players[1], players[0])      # Switch the players
            mc_player_id = 1 - mc_player_id         # Switch the player ID

            # 2.3. Play the episode
            while winner < 0:

                # 2.3.0. Get the current player
                game.change_player()
                current_player = players[game.get_current_player()]

                # 2.3.1. Act according to the current player
                if current_player == mc_player: # Monte Carlo player
                    
                    # Get the action to perform and the base action
                    from_pos, slide, base_state_action = current_player._get_action(game, training_phase=True)
                    base_state = base_state_action[0]
                    base_action = base_state_action[1]
                    
                    # Get the reward of the action
                    reward = current_player._get_action_reward(game, (from_pos, slide))
                    reward_counter += reward

                    # Make the move
                    game.make_move(from_pos, slide)

                    # Store the base state-action-reward in the trajectory
                    trajectory.append((base_state, base_action, reward))

                else: # Random player
                    # Make a random move
                    from_pos, slide = current_player.make_move(game)
                    game.make_move(from_pos, slide)

                # 2.3.2. Check if there is a winner
                winner = game.check_winner()
                if winner >= 0:
                    
                    # Get the final reward
                    end_reward = self._get_end_reward(mc_player_id, winner)
                    reward_counter += end_reward - reward # Discount the last partial reward

                    # Update the last state-action pair in the trajectory with the final reward
                    trajectory[-1] = (trajectory[-1][0], trajectory[-1][1], end_reward)

            # ..EPISODE ENDS..............................................  

            # 2.4. Update the Q-table
            self._update_q_table(trajectory)

            # 2.5. Update the exploration rate
            self.epsilon = max(self.e_min, self.epsilon * self.e_decay)

        # ..TRAINING ENDS..................................................

        # 3. Save the Q-table
        self._save_q_table("q_table.csv")
            

    
