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
from copy import deepcopy
from tqdm.auto import tqdm

class RL_Player(Player):
    
    def __init__(self, epsilon=1, alpha=0.2, gamma=0.9, e_decay=0.99999, e_min=0.2, guided_extension=False, opening_moves=5) -> None:
        super().__init__()

        # Parameters
        self.epsilon = epsilon    # Exploration rate (probability of choosing a random action)
        self.alpha = alpha        # Learning rate (step size)
        self.gamma = gamma        # Discount rate (importance of future rewards)
        self.e_decay = e_decay    # Exploration decay rate
        self.e_min = e_min        # Minimum exploration rate

        # Structures
        self.q_table = {}        # Q(s, a)
        self.q_counters = {}     # N(s, a)

        # Guided Extension
        # If True, the agent will only exploit its learned policy for the first opening_moves
        self.guided_extension = guided_extension
        self.opening_moves = opening_moves
    
    def make_move(self, game: 'Quixo') -> tuple[tuple[int, int], Move]:
        """
        Returns the best action for the current player using the Q-table
        
        (GUIDED EXTENSION)
        - The opening moves are still guided by the learned policy
        - After the opening moves, the agent will choose the action that maximizes the value of the next state
        """

        # 1. GUIDED EXTENSION: Choose the action that maximizes the next state's value
        # The opening moves are still guided by the learned policy
        if self.guided_extension and game.get_move_count()/2 >= self.opening_moves:

            # 1.0. Get all possible actions based on the current game state
            possible_actions = game.get_possible_actions()

            # 1.1. Initialize the variables
            max_value = float('-inf')
            best_action = choice(possible_actions)

            # 1.2. Choose the action that maximizes the next state's value
            for from_pos, slide in possible_actions:

                # 1.2.1. Get the next state's value
                value = self._get_next_state_value(game, from_pos, slide)

                # 1.2.3. Update the best action if necessary
                if value > max_value:
                    max_value = value
                    best_action = (from_pos, slide)

            # 1.4. Return the best action
            return best_action
        
        # 2. POLICY EXPLOITATION: Choose the action based on the learned policy
        else:
            return self._get_action(game, training_phase=False)

    def _get_next_state_value(self, game: 'Quixo', from_pos: tuple[int, int], slide: Move) -> int:
        """
        (GUIDED EXTENSION)
        Heuristic function that returns the value of the next state after simulating the given action.
        - It guides the agent to choose the action that maximizes the value of the next state 
            when the game is not in the opening stage.
        """
        # 1. Make a copy of the game and perform the action
        game_copy = deepcopy(game)
        game_copy.make_move(from_pos, slide)
            
        # 2. Get the new sequences of the player and the opponent
        x_sequences, o_sequences = game_copy.check_sequences()

        # 2. Get the sequences of the minimax player and its opponent
        rl_player_id = game_copy.get_current_player()
        if rl_player_id == 0:
            player_sequences = x_sequences
            opponent_sequences = o_sequences
        else:
            player_sequences = o_sequences
            opponent_sequences = x_sequences
        
        # 3. Get the total score
        player_score = player_sequences[0] + player_sequences[1] * 3 + player_sequences[2] * 15 + player_sequences[3] * 300
        opponent_score = opponent_sequences[0] + opponent_sequences[1] * 3 + opponent_sequences[2] * 15 + opponent_sequences[3] * 300
        return player_score - opponent_score

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
    
    def _get_action(self, game: 'Quixo', training_phase: bool=False) -> tuple[tuple[int, int], Move]:
        """
        Find the best action to perform balancing exploration and exploitation.

        Returns:
        1. the position of the piece to move
        2. the direction in which to move it
        """

        # 1. Get all possible actions based on the current game state
        possible_actions = game.get_possible_actions()

        # 2. EXPLORATION: Choose a random action
        if training_phase and random() < self.epsilon:
            return choice(possible_actions)            
        
        # 3. EXPLOITATION: Choose the action with the highest Q-value
        else:
            
            # 3.0. Set the symmetry generator
            SG = SymmetryGenerator()
            
            # 3.1. Get the hashable base state of the current board and the transformation applied
            transf_label, base_state = self._get_base_state(game)

            # 3.2. Transform the actions to base actions
            base_actions = []
            for from_pos, slide in possible_actions:
                base_actions.append(SG.get_base_action(from_pos, slide, transf_label))

            # 3.3. Get the Q-values of the base actions
            q_values = []
            for base_action in base_actions:

                # 3.3.1. If the state-action pair is not in the Q-table
                # => return a random Q-value between 0 and 1 to inject some variability in choosing the max
                q_values.append(self.q_table.get((base_state, base_action), random()))

            # 3.4. Get the action with the highest Q-value
            max_q_value = max(q_values)
            max_q_value_idx = q_values.index(max_q_value)
            best_base_action = base_actions[max_q_value_idx]

            # 3.5. Transform the action to the original action to be used in the game
            best_action = SG.get_original_action(best_base_action[0], best_base_action[1], transf_label)
            from_pos, slide = best_action

            # 3.6. ERROR-CHECK
            if best_action not in possible_actions:
                print("ERROR: The best action is not in the list of possible actions")
                raise Exception

            # 3.7. Return the action
            return from_pos, slide

    def _get_action_reward(self, game: 'Quixo', action: tuple[tuple[int, int], Move]) -> tuple[bool, int, int]:
        """Returns the reward of the given action"""

        # 0. Initialize the variables
        # The reward is negative to encourage the agent to win as fast as possible
        reward = -2 
        from_pos, slide = action
        winner = -1
        player_id = game.get_current_player()

        # 1. If the piece to move is neutral, get a small reward for occupying it
        if game.get_board()[from_pos[1]][from_pos[0]] == -1:
            reward += 1

        # 2. ERROR-CHECK: if the move is illegal, return false
        ok = game.make_move(from_pos, slide)
        if not ok:
            return ok, 0, -1
        
        """
        # 3. Get the sequences of X and O after the move
        x_sequences, o_sequences = game.check_sequences()

        # 4. Set the sequences to complete and to break based on the current player
        if player_id == 0:
            player_sequences = x_sequences
            opponent_sequences = o_sequences
        else:
            player_sequences = o_sequences
            opponent_sequences = x_sequences

        # 5. (+) REWARD: Get the reward based on the sequences of the current player
        reward += player_sequences[0] * 1 + player_sequences[1] * 3 + player_sequences[2] * 7
        if player_sequences[3] > 0:
            # Win the game
            reward = 100
            winner = player_id

        # 6. (-) REWARD: Get the reward based on the sequences of the opponent
        reward -= opponent_sequences[0] * 1 + opponent_sequences[1] * 3 + opponent_sequences[2] * 7
        if opponent_sequences[3] > 0:
            # Lose the game with its own move
            reward = -200
            winner = 1 - player_id
        """

        return ok, reward, winner
    
    def _get_end_reward(self, rl_player_id: int, winner: int) -> int:
        """Get the reward based on the winner of the game"""
        # 1. Give a big positive reward if the RL player wins
        if winner == rl_player_id:
            return 100
        # 2. Give a big negative reward if the RL player loses
        else:
            return -100

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
    
    def __init__(self, epsilon=1, alpha=0.2, gamma=0.9, e_decay=0.99999, e_min=0.2, guided_extension=False, opening_moves=5) -> None:
        super().__init__(epsilon, alpha, gamma, e_decay, e_min, guided_extension, opening_moves)

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
                self.q_table[(base_state, base_action)] = random() # Inject some variability in the initial Q-values (between 0 and 1)
            
            self.q_counters[(base_state, base_action)] += 1
            self.q_table[(base_state, base_action)] += self.alpha * (G - self.q_table[(base_state, base_action)]) / self.q_counters[(base_state, base_action)]

    def train(self, episodes: int = 1000):
        
        # 0. Initialize useful variables
        SG = SymmetryGenerator()
        min_epsilon_reached = False

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

                # 2.3.1. Try to make a move until it is successful
                ok = False
                while not ok:

                    # 2.3.1.1. Act according to the current player
                    if current_player == mc_player: # Monte Carlo player

                        # Get the base state of the current board
                        transf_label, base_state = mc_player._get_base_state(game)
                        
                        # Get the action to perform and the base action to save in the Q-table
                        from_pos, slide = current_player._get_action(game, training_phase=True)
                        base_action = SG.get_base_action(from_pos, slide, transf_label)

                        #### print(f"MC player board:\n{game.get_board()}")
                        #### print(f"MC player base state:\n{base_state}")
                        #### print(f"MC player action: {from_pos} {slide}")
                        #### print(f"MC player base action: {base_action}")
                        #### print("****************************")

                        # Make the move and get the reward
                        ok, reward, winner = current_player._get_action_reward(game, (from_pos, slide))

                        #### print(f"MC player board:\n{game.get_board()}")
                        #### print(f"MC player reward: {reward}")
                        #### print("---------------------------")
                        
                        # Check if the move was successful
                        if not ok:
                            print("ERROR: The Monte Carlo player tried to make an illegal move")
                        else:
                            # Update the reward counter
                            reward_counter += reward

                            # Store the base state-action-reward in the trajectory
                            trajectory.append((base_state, base_action, reward))

                    else: # Random player

                        # Get the action to perform
                        from_pos, slide = current_player.make_move(game)

                        # Make the move and check if it was successful
                        ok = game.make_move(from_pos, slide)

                # 2.3.2. Check if there is a winner
                if winner >= 0: 
                    
                    # 2.3.2.1. Win due to Monte Carlo player's last move (ONLY IN THE VERSION OF GET REWARD ACTION W/ HEURISTIC)
                    # => update the last state-action pair in the trajectory with the total episode reward
                    trajectory[-1] = (trajectory[-1][0], trajectory[-1][1], reward_counter)
                else:

                    # 2.3.2.2. Possible win due to Random player's last move (OR BOTH IF NOT VERSION OF GET REWARD ACTION W/ HEURISTIC)
                    winner = game.check_winner()
                    if winner >= 0:
                        
                        # Get the final reward
                        end_reward = self._get_end_reward(mc_player_id, winner)
                        reward_counter += end_reward

                        # Update the last state-action pair in the trajectory with the final reward
                        trajectory[-1] = (trajectory[-1][0], trajectory[-1][1], end_reward)                        

            # ..EPISODE ENDS..............................................
                        
            #### print(f"Trajectory: \n{trajectory}\n\n")

            # 2.4. Update the Q-table
            self._update_q_table(trajectory)

            # 2.5. Update the exploration rate
            self.epsilon = max(self.e_min, self.epsilon * self.e_decay)

            # 2.6. Warn the user when the minimum exploration rate is reached
            if min_epsilon_reached == False and self.epsilon == self.e_min:
                print("Minimum exploration rate reached!")
                min_epsilon_reached = True