"""
    quixo.py

    #TODO: Add a description of the file
"""

from game import Game, Move


class Quixo(Game):
    def __init__(self) -> None:
        super().__init__()
    
    def print(self):
        """
        Prints the board in a more readable way
        - ⬜ are neutral pieces
        - ❌ are pieces of player 0
        - 🔘 are pieces of player 1
        """
        for row in self._board:
            for cell in row:
                if cell == -1:
                    print("⬜", end=" ")
                elif cell == 0:
                    print("❌", end=" ")
                elif cell == 1:
                    print("🔘", end=" ")
            print()
        print()

    def get_hashable_state(self) -> str:
        """Converts the game state to a hashable string"""
        return str(self._board)
    
    def get_possible_actions(self) -> list[tuple[tuple[int, int], Move]]:
        """
        Returns a list of possible actions.

        An action is a tuple of:
        - the position of the piece to move
        - the direction in which to move it

        An action is possible if:
        - the piece is neutral or belongs to the current player
        - the piece is on the edge of the board

        The direction in which a piece can be moved depends on its position:
        - all pieces can be moved from the opposite edge(s) of the board
        - pieces not in a corner can be also moved in directions parallel to the edge they were taken from
        """
        # 1. Initialize the list of possible actions
        possible_actions = []

        # 2. Check the edges of the board for possible actions
        for i in range(5):

            # 2.1. Check TOP and BOTTOM edges
            for row in [0, 4]:
                # 2.1.1. Get the piece at the current position
                piece = self._board[row, i]
                # 2.1.2. If the piece is neutral or belongs to the current player
                if piece == -1 or piece == self.current_player_idx:
                    # 2.1.2.1. Add the option to move it from the opposite edge
                    if row == 0: possible_actions.append(((i, row), Move.BOTTOM))
                    else: possible_actions.append(((i, row), Move.TOP))
                    # 2.1.2.2. If the piece is not in a corner, also add the option to move it from parallel edges
                    if i != 0 and i != 4:
                        possible_actions.append(((i, row), Move.LEFT))
                        possible_actions.append(((i, row), Move.RIGHT))

            # 2.2. Check LEFT and RIGHT edges
            for col in [0, 4]:
                # 2.2.1. Get the piece at the current position
                piece = self._board[i, col]
                # 2.2.2. If the piece is neutral or belongs to the current player
                if piece == -1 or piece == self.current_player_idx:
                    # 2.2.2.1. Add the option to move it from the opposite edge
                    if col == 0: possible_actions.append(((col, i), Move.RIGHT))
                    else: possible_actions.append(((col, i), Move.LEFT))
                    # 2.2.2.2. If the piece is not in a corner, also add the option to move it from parallel edges
                    if i != 0 and i != 4:
                        possible_actions.append(((col, i), Move.TOP))
                        possible_actions.append(((col, i), Move.BOTTOM))

        # 3. Return the list of possible actions
        return possible_actions