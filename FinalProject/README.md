**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]
- Richard S. Sutton, Andrew G. Barto, *Reinforcement Learning: An Introduction* [2nd Edition]
- Tanaka, Satoshi & Bonnet, François & Tixeuil, Sebastien & Tamura, Yasumasa. (2020). *Quixo Is Solved.*
- Anurag Bhatt, Pratul Varshney, Kalyanmoy Deb. (KanGAL Report Number 2007002). *Evolution of No-loss Strategies for the Game of Tic-Tac-Toe*

**Collaborators:** This project was developed in collaboration with [Alessandro Chiabodo s309234](https://github.com/AChiabodo/compIntelligence.git)
.

.

# Final Project: Quixo Player

## Table of Contents
- [Introduction](#introduction)
- [Preliminary Analysis](#preliminary-analysis)
  - [Game State Representation](#game-state-representation)
  - [State-Space Size](#state-space-size)
    - [Infeasible States](#infeasible-states)
    - [Symmetric Nature of the Board](#symmetric-nature-of-the-board)
    - [Players Equivalence](#players-equivalence)
  - [State-Space Structure](#state-space-structure)
    - [Consequences](#consequences)
  - [Maximum Possible Actions](#maximum-possible-actions)
  - [Our Considerations](#our-considerations)
    - [MiniMax Agent](#minimax-agent)
    - [Reinforcement Learning Agent](#reinforcement-learning-agent)
- [Implementation](#implementation)
  - [Quixo Extended Class](#quixo-extended-class)
    - [Initialization](#initialization)
    - [Move Count](#move-count)
    - [Printing](#printing)
    - [Possible Actions](#possible-actions)
    - [Making Moves](#making-moves)
    - [Sequence Checking](#sequence-checking)
    - [Checking for a Winner](#checking-for-a-winner)
    - [Changing Players](#changing-players)
    - [Playing a Game](#playing-a-game)
  - [MiniMax Agent](#minimax-agent)
    - [Game Tree Representation](#game-tree-representation)
    - [Recursive Evaluation](#recursive-evaluation)
    - [Maximizing and Minimizing Players](#maximizing-and-minimizing-players)
    - [Alpha-Beta Pruning Optimization](#alpha-beta-pruning-optimization)
  - [Reinforcement Learning Agent](#reinforcement-learning-agent-1)
    - [Symmetry Management](#symmetry-management)
    - [Rewarding System](#rewarding-system)
    - [Guided Extension](#guided-extension)
- [Results](#results)


## Introduction
The aim of this project is to develop a player for the game Quixo, a board game invented by Thierry Chapeau and published by Gigamic in 1991.

### Game Description
Quixo is played on a 5x5 board. Each square of the board initially contains a neutral piece, represented by -1 in the code. The game is played by two players:
- Player 0: ❌
- Player 1: 🔘

#### Rules
Players take turns to play. A turn consists of two actions: 
1. Taking a piece from the board.
2. Then sliding it back onto the board.

A piece can only be taken from the edge of the board if it is either neutral or already belongs to that player. Once a piece is taken, the player marks it as their own.
- ⬜⬜⬜⬜⬇️⬜⬜
- ⬜🟥🟥🟥🟥🟥⬜
- ⬜🟥🟨🟨🟨🟥⬜
- ⬜🟥🟨🟨🟨🟥⬜
- ⬜🟥🟨🟨🟨🟥⬜
- ➡️🟥🟥🟥🟦🟥⬅️
- ⬜⬜⬜⬜⬜⬜⬜


The player then slides the piece back onto the board from a different edge, pushing the other pieces to make room.
> The direction in which a piece can be slid back onto the board depends on its position. Pieces not in a corner can be moved in 3 directions (parallel to the edge they are on and from the opposite edge). Pieces in a corner can only be moved in 2 directions (from the opposite edges).

#### Winning Condition
A player wins by forming a continuous line of five of their pieces, either horizontally, vertically, or diagonally. The game checks for a winner after each turn. If a player has formed such a line, they are declared the winner.

The game continues with players alternating turns until one player wins.

## Preliminary Analysis

### Game State Representation

The game state of Quixo is represented by:
- The currently **active player**
- The arrangement of the pieces on a **5x5 matrix**, where each element can be:
  - -1: neutral piece
  - 0: player ❌'s piece
  - 1: player 🔘's piece

> It's important to note that, unlike other games like [Tic-Tac-Toe](../Labs/Lab_10/tictactoe.ipynb), the active player cannot be determined by the distribution of the pieces on the board. This is because the player can take an already owned piece and move it to another position.

### State-Space Size

Since we have 25 squares on the board, 3 possible symbols for each square, and 2 possible players, we can set the **upper-bound estimate** of possible states to approximately $2 \cdot 3^{25}$, which equals about $1.5 \cdot 10^{12}$.

While the state-space size is theoretically pretty large, we can assume that the actual number of unique states is significantly lower than the upper bound.

#### 🚫 Infeasible States

Some states in Quixo are infeasible, meaning they cannot be reached through regular gameplay. For instance, a state with multiple X pieces but no O pieces is infeasible since the second player will necessarily place an O piece when making their move.

#### ♊ Symmetric Nature of the Board

Another crucial factor that reduces the number of unique states in Quixo is the symmetry inherent in the game board. The board exhibits eight symmetrical transformations:

- **4 rotations** (0°, 90°, 180°, 270°)
- **4 reflections** (horizontal, vertical, diagonal, anti-diagonal)

Given any state, we can generate up to eight `equivalent states` by applying each of these eight symmetries.

#### 🟰 Players Equivalence

In Quixo, both players share the **same winning strategy** as their counterpart if the pieces on the board are **reversed**. Consequently, by considering the current player as `always X`, we can simplify our analysis to just the state of the board.

By focusing solely on the current state of the board and ignoring the identity of the player, we effectively halve the state-space size and streamline the decision-making process for our AI algorithms.

### State-Space Structure

In choosing a strategy, it is fundamental to consider that  the state-space cannot be perfectly represented as a tree due to the nature of the gameplay. Particularly towards the end of the game, when the board is nearly full, most moves don't add new pieces. Instead, they just move the pieces that are already there. This creates **cycles** in the game, where we might see the same arrangement of pieces more than once.

> Because of this looping, we have to think of the game more like a **graph**, where these repeated patterns can happen.

#### Consequences
1. **Complexity in Game Tree Search Algorithms** - The possibility of revisiting states in Quixo complicates algorithms like Minimax, as they need to account for cycles and repeated states to avoid infinite loops and redundant computations.
2. **Memory Management** - In AI implementations, especially those using search strategies, it's crucial to remember which states have been visited to prevent redundant evaluations and infinite loops. This requires more sophisticated memory management than a simple tree traversal.

### Maximum Possible Actions
The maximum number of possible actions for each state depends on several factors:
- **Empty Spaces**: The number of empty spaces on the board determines the potential moves.
- **Player Turn**: Whether it's player X's or player O's turn influences which pieces can be moved.
- **Pieces Arrangement**: Available pieces on the corners offer less movement options.

Considering the initial empty board, we can calculate the upper bound for the number of possible actions as follows: 

> $( 3_{border pieces} * 3_{directions} + 1_{corner piece} * 2_{directions}) * 4_{sides} =44$ possible actions.

This implies that the game-state tree has a maximum of 44 children for each node.

### Our Considerations

In light of the above, both MiniMax and Reinforcement Learning (RL) agents seemed like good choices for developing our players.

#### 🔸 MiniMax Agent
MiniMax is a classic algorithm for making decisions in adversarial games like Quixo. It explores the game tree by recursively evaluating possible moves up to a certain depth, maximizing its chances of winning while minimizing the opponent's. 
- `Deterministic Nature`: Quixo is a deterministic, turn-based game with perfect information. The deterministic nature allows us to easily explore sections of the game-state tree.
- `Branching Factor`: The relatively low branching factor (maximum 44 moves per turn) of the game tree makes MiniMax particularly effective in Quixo.
- `Sound Strategy`: MiniMax could potentially guarantee a very good strategy by exploring the tree in depth.
- `Player Symmetry`: The symmetric nature of the game, where players share winning strategies, aligns well with MiniMax's approach, simplifying the decision-making process.

#### 🔹 Reinforcement Learning Agent
Reinforcement Learning is a powerful paradigm for learning optimal strategies through trial and error. RL agents, such as those based on Monte Carlo algorithm, can adapt and improve their performance over time by interacting with the environment and receiving feedback in the form of rewards. 
- `State-Space Complexity`: Despite the large state space, the symmetric properties of Quixo can help mitigate the complexity, making RL a viable option. 
- `Player Equivalence`: The equivalence of strategies between players makes RL particularly suitable, as the agent can learn a comprehensive policy without differentiating between the two players.
- `Adaptability`: RL agents have the potential to discover nuanced strategies that might not be immediately apparent to human players.

By combining the strengths of both MiniMax and RL agents, we aim to create a versatile AI system capable of optimal decision-making in Quixo, leveraging the deterministic nature and strategic symmetry of the game.


## Implementation

### Quixo Extended Class

The `Quixo` class serves as a wrapper for the provided `Game` class, offering additional functionalities and modifications to best suit the implementation of our AI agents.

#### Initialization
- We've added the `moves_count` attribute to keep track of the number of moves made during the game.
- This new feature is useful to determine if the game is in a opening, mid-game, or end-game state, and can be used to adjust the strategy of the AI agent accordingly.

#### Move Count
- The `get_move_count` method returns the number of moves made so far.

#### Printing
- The `print` method prints the current board state along with the players' pieces in a user-friendly format, indicating neutral pieces as ⬜, pieces of player 0 as ❌, and pieces of player 1 as 🔘.
- If a winner is determined, it displays the winning player. Otherwise, it shows the current player.

#### Possible Actions
- The `get_possible_actions` method returns a list of possible actions, consisting of tuples containing the position of the piece to move and the direction in which to move it.
- An action is considered possible if the piece is neutral or belongs to the current player and if the piece is on the edge of the board.
- This method is very useful to get a faster and more efficient evaluation of the game tree.

#### Making Moves
- The `make_move` method updates the board by making a move from the specified position in the given direction.
- It also increments the `moves_count` counter.

#### Sequence Checking
> 🔆 This is one of the most important methods in the class, as it is used by all the AI agents as starting point for the heuristic evaluation of the board state.
- The `check_sequences` method checks for the number of adjacent 2, 3, 4, and 5 pieces for each player, along with the number of 4 pieces in a line, even if they are not adjacent.
- It returns the counts of sequences for both players.

#### Checking for a Winner
- The `check_winner` method checks if there is a winner based on the current board state.

#### Changing Players
- The `change_player` method switches the current player.

#### Playing a Game
- The `play` method initiates a game between two players, taking them as arguments and providing an option for verbosity and debugging. 
- It mantains the same structure as the `play` method in the `Game` class, but it uses our `print` method to give a more user-friendly output.

### MiniMax Agent

The minimax algorithm is a decision-making algorithm used in two-player turn-based games. It is particularly popular in board games like chess, tic-tac-toe, and Quixo. 
- The goal of the minimax algorithm is to find the optimal move for a player, assuming that the opponent also plays optimally.
- The algorithm explores the game tree, representing all possible moves and counter-moves, and assigns a value to each node in the tree.

The file [`minimax.py`](minimax.py) contains the implementation of our MiniMax agent.

#### 🌳 Game Tree Representation

The game state is represented as a tree, where each node corresponds to a possible state of the game. Nodes at even depths represent the current player's turn, and nodes at odd depths represent the opponent's turn.

#### ♻️ Recursive Evaluation

The algorithm recursively evaluates the nodes of the tree by assigning a value to each node.
For terminal nodes (leaves of the tree), the algorithm uses our `evaluate` function to determine the utility or score of the state.
- The function is based on the number of sequences of 2, 3, 4, and 5 pieces for each player.
- It returns a positive value if the current player has more combinations than the opponent.
- It returns the maximum/minumum possible value if the current player has won/lost the game.

#### 🔃 Maximizing and Minimizing Players

- For nodes representing the current player's turn (*maximizing player*), the algorithm selects the child node with the maximum value.
- For nodes representing the opponent's turn (*minimizing player*), the algorithm selects the child node with the minimum value.

#### ✂️ Alpha-Beta Pruning Optimization

To improve efficiency, our algorithm uses alpha-beta pruning, which eliminates branches that cannot possibly affect the final decision.
- Alpha represents the best value found by the maximizing player.
- Beta represents the best value found by the minimizing player.

### Reinforcement Learning Agent

Reinforcement Learning is a machine learning paradigm that allows an agent to learn an optimal policy by interacting with the environment and receiving rewards. We decided to use the **Monte Carlo** algorithm, which is a model-free RL algorithm that learns directly from episodes of experience without any prior knowledge of the environment's dynamics.
- It is based on the idea of averaging sample returns for each state-action pair to estimate the expected return for that state-action pair.
- The algorithm learns by playing games against a Random Player and updating the Q-table based on the rewards received.
- It stores the episode information in a trajectory, which is a list of tuples containing the state, the action, and the reward received.

The file [`reinforcement_learning.py`](reinforcement_learning.py) contains the implementation of our RL agent.

#### ♊ Symmetry Management
As mentioned in the preliminar analysis section, the board has 8 symmetries. This means that, given a state, we can generate up to 8 equivalent states. We can use this to our advantage by reducing the number of states we need to explore.

The file [`symmetry.py`](symmetry.py) contains the implementation of our symmetry management class.

##### Trastrormations
The class handles the 8 transformations for different elements of the game in these 3 main code blocks. Each method is associated with a specific label that indicates the type of transformation.
1. `self.board_transforms` - A collection of methods that transform the board.
2. `self.coor_transforms` - A collection of methods that transform the coordinates of the action to be performed.
3. `self.slide_transforms` - A collection of methods that transform the direction of action to be performed.

##### Base State and Action
The `base state` is the state with the *lowest lexicographical order* among all the equivalent symmetries of the board. The `base action` is the action that is performed on the base state.
- When updating the Q-table, we always use the base state and the base action.
- When we want to exploit the learned policy, we need to apply the inverse transformation to the base action to get the actual action to be performed on the board.

##### Q-Table Base State

The function `_get_base_state`, belonging to the RL agent class, is finally used to get the base state of the board to be used for updating the Q-table.
- It transforms the board to the viewpoint of player X.
- It get the base state of the board.
- It retrieves the label of the transformation applied to the board.

#### 🪙 Rewarding System

During the development, we've tried different rewarding systems to see which one would work best for our agent. 

- Since the number of possible states is very large, we initially thought that the agent would have been guided by the rewards to learn the optimal policy. Therefore, we tried to integrate a reward for each action based on a similar heuristic to the one used in the MiniMax agent. We tried multiple variants of this system, however we noticed that the agent was **too biased** by the rewards and it was not able to learn a good policy. 
- Finally, we decided to base the rewards mainly on the final outcome of the game, keeping for each action a small negative reward to discourage the agent from taking too long to win.
  - `_get_action_reward` - Returns -1 for an action that moves a neutral piece and -2 for an action that moves a player's piece.
  - `_get_end_reward` - Returns 100 if the agent wins, -100 if the agent loses.

#### 🗺️ Guided Extension

Even though we tried our best to minimize the number of states to explore, the state space is still too large to be explored in a reasonable amount of time. After 500000 episodes, the agent was still not able to learn a good policy.
- **Q_table size**: 9_885_394
- **Average win rate**: 0.59

The objective of the guided extension is to modify the agent's decision-making process during gameplay.Initially, the agent follows its learned policy for opening moves. However, once the game progresses beyond a certain number of opening moves, the agent transitions to a strategy that selects actions maximizing the value of the next state, aiming to guide the agent towards more favorable positions as the game progresses. 
- This transition is facilitated by the `_get_next_state_value` function, which provides a heuristic evaluation of the value of the next state after simulating a given action, encouraging the agent to choose actions that lead to states with higher values.

## Results

To explore the performance of our AI agents, we invite you to check out our [Quixo Jupyter Notebook](quixo.ipynb), where we've included a detailed analysis of the results and a comparison between the two agents.