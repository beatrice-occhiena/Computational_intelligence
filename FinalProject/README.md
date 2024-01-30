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

### Game description
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

#### Winning condition
A player wins by forming a continuous line of five of their pieces, either horizontally, vertically, or diagonally. The game checks for a winner after each turn. If a player has formed such a line, they are declared the winner.

The game continues with players alternating turns until one player wins.

## Preliminary analysis

### Game state representation
The game state of Quixo is represented by the **active player** and a **5x5 matrix**, where each element can be:
- -1: neutral piece
- 0: player ❌ piece
- 1: player 🔘 piece

The plain game state is stored in the already provided `class Game`.

> It's important to note that, unlike other games like [Tic-Tac-Toe](../Labs/Lab_10/tictactoe.ipynb), the active player cannot be determined by the distribution of the pieces on the board. This is because the player can take an already owned piece and move it to another position. 

#### State-space size

Given the characteristics of the game, the state-space size is not excessively large. In fact, the number of possible states is **upper-bounded** by $2 \cdot 3^{25}$, which is approximately $1.5 \cdot 10^{12}$.

Although it is possible to fill the 25 squares of the board with 3 different pieces, considering one of the 2 players as active, the number of `unique states` is luckily much lower than the upper bound.

> Some states are **infeasible**, i.e. they cannot be reached by playing the game.

For example, a state where there are 2 or more X pieces but no O pieces is infeasible, because once the second player moves a neutral piece, it will be marked as O.

> However, the most important factor that reduces the number of unique states is the symmetric nature of the board. The board has **8 symmetries**:
- 4 rotations *(0°, 90°, 180°, 270°)*
- 4 reflections *(horizontal, vertical, diagonal, anti-diagonal)*

Given a state, we can therefore generate a maximum of 8 `equivalent states` by applying each of the 8 symmetries. 

#### State-space structure

In choosing a strategy, it is fundamental to consider that  the state-space cannot be perfectly represented as a tree due to the nature of the gameplay. Particularly towards the end of the game, when the board is nearly full, most moves don't add new pieces. Instead, they just move the pieces that are already there. This creates **cycles** in the game, where we might see the same arrangement of pieces more than once.

> Because of this looping, we have to think of the game more like a **graph**, where these repeated patterns can happen.

##### Consequences
1. **Complexity in Game Tree Search Algorithms** - The possibility of revisiting states in Quixo complicates algorithms like Minimax, as they need to account for cycles and repeated states to avoid infinite loops and redundant computations.
2. **Memory Management** - In AI implementations, especially those using search strategies, it's crucial to remember which states have been visited to prevent redundant evaluations and infinite loops. This requires more sophisticated memory management than a simple tree traversal.

## Implementation

### Quixo extended class
We've created 

### Symmetry Management
As mentioned in the previous section, the board has 8 symmetries. This means that, given a state, we can generate up to 8 equivalent states.

In the file [`symmetry.py`](symmetry.py) we've implemented ...


#TODO
- Switch 0s and 1s in the board before searching in the Q-table WHEN RL_player moves second
- Approximating Q function with a Neural Network???


# MiniMax

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




