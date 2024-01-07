**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]
- Richard S. Sutton, Andrew G. Barto, *Reinforcement Learning: An Introduction* [2nd Edition]
- Useful site to better understand Monte Carlo method [analyticsvidhya.com](https://www.analyticsvidhya.com/blog/2018/11/reinforcement-learning-introduction-monte-carlo-learning-openai-gym/)

.

.

# Final Project: Quixo Player

## Introduction
The aim of this project is to develop a player for the game Quixo, a board game invented by Thierry Chapeau and published by Gigamic in 1991.

### Game description
Quixo is played on a 5x5 board. Each square of the board initially contains a neutral piece, represented by -1 in the code. The game is played by two players:
- Player 0: ❌
- Player 1: 🔘

Players take turns to play. A turn consists of two actions: 
1. Taking a piece from the board.
2. Then sliding it back onto the board.

A piece can only be taken from the edge of the board if it is either neutral or already belongs to that player. Once a piece is taken, the player marks it as their own.
- ⬜⬜⬜⬜⬇️⬜⬜
- ⬜🟥🟥🟥🟥🟥⬜
- ⬜🟥⬜⬜⬜🟥⬜
- ⬜🟥⬜⬜⬜🟥⬜
- ⬜🟥⬜⬜⬜🟥⬜
- ➡️🟥🟥🟥🟨🟥⬅️
- ⬜⬜⬜⬜⬆️⬜⬜


The player then slides the piece back onto the board from a different edge, pushing the other pieces to make room.
- 🟥🟥🟥🟥🟥
- 🟥⬜⬜⬜🟥
- 🟥⬜⬜🟥🟥
- 🟥⬜⬜⬜🟥
- 🟥🟥🟥🟨🟥
