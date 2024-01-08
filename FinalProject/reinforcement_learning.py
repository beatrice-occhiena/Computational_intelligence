"""
reinforcement_learning.py

This file contains the code for the reinforcement learning algorithm used to create
"""

from game import Game, Move, Player, Quixo
from random import choice, random

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
    
    def _get_action(self, game: 'Quixo', training_phase: bool = False) -> Move:
        """Returns a new action based on the current state balancing exploration and exploitation"""

        # 1. Get the current state representation
        state = game.get_hashable_state()

        # 2. Get all possible actions
        possible_actions = game.get_possible_actions()

        # 3. EXLORATION: Choose a random action (only during training)
        if training_phase and random() < self.epsilon:
            return choice(possible_actions)
        
        # 4. EXPLOITATION: Choose the action with the highest Q-value
        else:
            # 4.1. Get the Q-values for all possible actions (0 if not in Q-table)
            q_values = [self.q_table.get((state, action), 0) for action in possible_actions]

            # 4.2. Get the index of the action with the highest Q-value
            max_index = q_values.index(max(q_values))

            # 4.3. Return the action with the highest Q-value
            return possible_actions[max_index]


    def make_move(self, game: 'Quixo'):
        """Make a move based on the learned policy"""

        # 1. Get the action balancing exploration and exploitation
        action = self._get_action(game)

        # 2. Make the move
        game.make_move(action)

   def _get_action_reward(self, game: 'Quixo', action) -> in