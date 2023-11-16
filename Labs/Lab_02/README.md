**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]

.

.

# Lab 2: Nim game

The game of Nim is a well-known **combinatorial misère game** in which we have a number of objects (say coins 🪙 in this case) arranged in different rows. In each turn, a player can remove one or more objects from a single row and the player who takes the last object loses. The game is usually played with a number of rows and a maximum number of objects that can be removed in a turn. 

| Row | Objects |
| --- | --- |
| 0 | 🪙 |
| 1 | 🪙 🪙 🪙 |
| 2 | 🪙 🪙 🪙 🪙 🪙 |

## Task 1: nim-sum expert agent

### Nim-sum
At any state of the game, we can define the **nim-sum** as the cumulative XOR value of the number of coins in each row. 

| Row | Objects | Binary |
| --- | --- | --- |
| 0 | 🪙 | 001 |
| 1 | 🪙 🪙 🪙 | 011 |
| 2 | 🪙 🪙 🪙 🪙 🪙 | 111 |

`nim-sum` = 001 XOR 011 XOR 111 = 101 = 5

### Winning strategy
To develop a rule-based winning strategy for my agent, I made the following observations based on the state of the game.

#### [1] - Initial phase
If the nim-sum is non-zero and the player to move is playing optimally, then he's guaranteed to win. 
- `nim-sum` = 0 $\implies$ losing position
- `nim-sum` != 0 $\implies$ winning position

> Therefore, the optimal strategy is to always leave the nim-sum equal to zero for the opponent.

> ⚠️ The k constraint complicates the situation. We must be sure that the number of objects to remove is less than k. If it is not, we must avoid to put the opponent in a favourable position.

#### [2] - Scarcity State
When the game is near the end, we must pay attention to the case in which there is only one row with more than one object. 

1. The number of remaining rows is even $\implies$ we want to remove entirely the abundant row
2. The number of remaining rows is odd $\implies$ we want to leave only one object in the abundant row

### Agents implementation
I implemented different agents with different strategies in order to compare their performance:
1. `expert_agent`: it implements the winning strategy described above
2. `random_agent`: it chooses a random row and a random number of objects to remove
3. `sloppy_agent`: it chooses an optimal move with probability 1-distraction_rate, otherwise choose a random move
4. `silly_agent`: it always chooses to take all the objects (or k) in the min objects row

The expert agent should always win when:
- the Nim state to a winning position for the expert agent
- `k = None` (i.e. no constraint on the number of objects that can be removed in a turn)

## Task 2: ES agent
For this task, I want create an agent that uses ES to learn the optimal strategy to play Nim. The main idea is to create a population of agents, each one with a different set of weighted rules, and evolve them over time. To test their performance, they will play against the previously created agents.

### Rule representation
I designed a generic rule as a combination of the following elements:
- ❓ `condition` = it evaluates certain aspects of the game state
- 📍 `position` = it indicates the row to which the action must be applied
- 🫱🏻 `action` = it indicates the number of objects to remove from the row

```python
conditions = [if_odd_rows, if_even_rows, if_scarcity]
positions = [min_position, max_position, random_position]
actions = [get_one, get_all_but_one, get_max, get_random]
```

To explore a wide range of strategies, we want to generate all possible combinations of conditions, positions, and actions. This exhaustive approach allows us to experiment with various rule sets and observe how different combinations impact the agent's performance.

> To check if the ES is working properly, we can insert a special set of **advanced rules** `directly derived from the expert agent`. In this way, we can see if the ES is able to maximize the weights of these rules and to learn the optimal strategy after a certain number of generations.

### ES individuals
The ESIndividual class represents an individual within the Evolutionary Strategy (ES) framework for the Nim game. Each individual is characterized by:
- 📃 `rules`: a list of all possible rules
- 🎚️ `weights`: a list of weights corresponding to the importance of selecting each rule
- 📏 `sigmas`: a list of standard deviations corresponding to self-adapt the weights
- 🏋🏻 `fitness`: a measure of the individual's performance

#### Rule selection
The pick_rule method selects a rule based on the weights and conditions. It considers rules whose conditions hold true for the current game state, computes the probability of each rule, and selects one accordingly.

> 🛞 This method is inspired by the roulette wheel selection method used in genetic algorithms.

#### Mutation
The mutate method applies a mutation to the individual's weights and sigmas, with a certain probability. The mutation is a Gaussian random number with `mean 0` and standard deviation `sigma[i]`.

#### Fitness evaluation
To evaluate the fitness of an individual, we will make it play a certain number of games against other agents. The fitness is the proportion of wins in these games.
