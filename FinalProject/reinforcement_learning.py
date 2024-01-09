"""
reinforcement_learning.py

This file contains the code for the reinforcement learning algorithm used to create
"""

from game import Game, Move, Player
from symmetry import SymmetryGenerator
from quixo import Quixo
from random import choice, random
from abc import abstractmethod
import tqdm

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
    
    def make_move(self, game: 'Quixo'):
        """Select a move based on the learned policy"""
        return self._get_action(game)

    def _get_action(self, game: 'Quixo', training_phase: bool = False) -> tuple[tuple[int, int], Move]:
        """Returns a new action based on the current state balancing exploration and exploitation"""

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
            transf_label, base_state = game.get_base_state()

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

            # 4.6. Return the best action
            return best_action

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
    def update_q_table(self, state: tuple[str, str], action: tuple[tuple[int, int], Move], reward: int, next_state: tuple[str, str]):
        """Update the Q-table"""
        pass
    
    @abstractmethod
    def train(self, episodes: int = 1000, verbose: bool = False):
        """Train the agent for the given number of episodes"""
        pass
    
    def save_q_table(self, path: str):
        """Save the Q-table to a file to retrieve it later"""
        with open(path, "w") as f:
            for key, value in self.q_table.items():
                f.write(f"{key[0]},{key[1][0]},{key[1][1]},{value}\n")




