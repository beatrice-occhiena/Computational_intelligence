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

### Reinforcement Learning

#### ♊ Symmetry Management
As mentioned in the previous section, the board has 8 symmetries. This means that, given a state, we can generate up to 8 equivalent states.

In the file [`symmetry.py`](symmetry.py) we've implemented ...

### MiniMax

The minimax algorithm is a decision-making algorithm used in two-player turn-based games. It is particularly popular in board games like chess, tic-tac-toe, and Quixo. The goal of the minimax algorithm is to find the optimal move for a player, assuming that the opponent also plays optimally. The algorithm explores the game tree, representing all possible moves and counter-moves, and assigns a value to each node in the tree.

Game Tree Representation:

The game state is represented as a tree, where each node corresponds to a possible state of the game.
Nodes at even depths represent the current player's turn, and nodes at odd depths represent the opponent's turn.
Recursive Evaluation:

The algorithm recursively evaluates the nodes of the tree by assigning a value to each node.
For terminal nodes (leaves of the tree), the algorithm uses an evaluation function to determine the utility or score of the state.
Maximizing and Minimizing Players:

For nodes representing the current player's turn (maximizing player), the algorithm selects the child node with the maximum value.
For nodes representing the opponent's turn (minimizing player), the algorithm selects the child node with the minimum value.
Backpropagation:

The selected values are propagated back up the tree to update the values of parent nodes.
At each level, the maximizing player seeks to maximize the value, and the minimizing player seeks to minimize the value.
Optimization - Alpha-Beta Pruning:

To improve efficiency, the algorithm uses alpha-beta pruning, which eliminates branches that cannot possibly affect the final decision.
Alpha represents the best value found by the maximizing player, and beta represents the best value found by the minimizing player.
Final Decision:

After exploring the entire tree or reaching a specified depth, the algorithm makes the final decision based on the root node's children.
In summary, the minimax algorithm provides a systematic way to explore the entire game tree, considering all possible moves and counter-moves. The use of alpha-beta pruning helps reduce the number of nodes that need to be evaluated, making the algorithm more efficient.


