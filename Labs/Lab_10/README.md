
**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]
- Richard S. Sutton, Andrew G. Barto, *Reinforcement Learning: An Introduction* [2nd Edition]

.

.
# Lab 10: Tic-Tac-Toe with Reinforcement Learning

My starting point was the original code from the official course repository.

### Magic Square Trick

A magic square, in the context of this game, is a specific arrangement of numbers that plays a crucial role in simplifying the win condition check. In a standard 3x3 magic square, each cell contains a unique number from 1 to 9, and the sum of the numbers in any row, column, or diagonal is always the same.

`MAGIC = [2, 7, 6, 9, 5, 1, 4, 3, 8]`

- **Efficient win check**: In Tic-Tac-Toe, a player wins if they can line up three of their marks (either X or O) in a row, column, or diagonal. By using a magic square, if the sum of the magic square numbers corresponding to a player's marks is `15`, then that player has achieved a winning combination


### Integrating Symmetry Recognition

The game of Tic-Tac-Toe has a number of both **rotational and reflective symmetries** that can be exploited to reduce the number of states that need to be learned. In fact, a borad rotated or mirrored represents the `same strategic situation`. 

In considering this peculiaity, we can obtain:
1. **Reduced state space**: There are fewer unique states to learn.
2. **Faster Convergence**: The learning process can converge more quickly as it leverages knowledge gained from one state across its symmetrical equivalents.
3. **Improved Generalization**: The agent can generalize its knowledge to new states more effectively.

To implement this idea, I needed to:
1. **Identify symmetrical states** implementing a method to recognize when different board configurations are symmetrical equivalents.
2. **Consolidate learning across symmetrical states**: Once symmetrical states are identified, we need to treat them as a single state in the learning process.

Having said that, should we always attribute the same value to symmetrical states?
- `Theoretically, yes.` In a perfect information game like tic-tac-toe, symmetrically equivalent positions hold the same strategic value, as they lead to equivalent outcomes with optimal play.
- `Practically, maybe not.` Against an imperfect or asymmetrically playing opponent, there could be a strategic benefit to treating these positions differently, as it might exploit the opponent's lack of symmetry awareness.

### Implementing Self-Play

In order to train the agent, I also implemented a self-play version, in which each agent is essentially **learning from itself**. This can lead to a rapid refinement of strategies, as each agent quickly adapts to the strategies of the other.

Since the context of learning is different (playing against itself rather than a random or static opponent), I expected the algorithm to likely develop a different set of policies. In the process of constantly trying to outdo itself, the algorithm may discover and learn more advanced tactics and strategies that might not surface when playing against a less sophisticated or predictable opponent.

