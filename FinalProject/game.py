from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
import numpy as np

# Rules on PDF


class Move(Enum):
    '''
    Selects where you want to place the taken piece. The rest of the pieces are shifted
    '''
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class Player(ABC):
    def __init__(self) -> None:
        '''You can change this for your player if you need to handle state/have memory'''
        pass

    @abstractmethod
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        '''
        The game accepts coordinates of the type (X, Y). X goes from left to right, while Y goes from top to bottom, as in 2D graphics.
        Thus, the coordinates that this method returns shall be in the (X, Y) format.

        game: the Quixo game. You can use it to override the current game with yours, but everything is evaluated by the main game
        return values: this method shall return a tuple of X,Y positions and a move among TOP, BOTTOM, LEFT and RIGHT
        '''
        pass


class Game(object):
    def __init__(self) -> None:
        self._board = np.ones((5, 5), dtype=np.uint8) * -1
        self.current_player_idx = 1

    def get_board(self) -> np.ndarray:
        '''
        Returns the board
        '''
        return deepcopy(self._board)

    def get_current_player(self) -> int:
        '''
        Returns the current player
        '''
        return deepcopy(self.current_player_idx)

    def print(self):
        '''Prints the board. -1 are neutral pieces, 0 are pieces of player 0, 1 pieces of player 1'''
        print(self._board)

    def check_winner(self) -> int:
        '''Check the winner. Returns the player ID of the winner if any, otherwise returns -1'''
        # for each row
        for x in range(self._board.shape[0]):
            # if a player has completed an entire row
            if self._board[x, 0] != -1 and all(self._board[x, :] == self._board[x, 0]):
                # return the relative id
                return self._board[x, 0]
        # for each column
        for y in range(self._board.shape[1]):
            # if a player has completed an entire column
            if self._board[0, y] != -1 and all(self._board[:, y] == self._board[0, y]):
                # return the relative id
                return self._board[0, y]
        # if a player has completed the principal diagonal
        if self._board[0, 0] != -1 and all(
            [self._board[x, x]
                for x in range(self._board.shape[0])] == self._board[0, 0]
        ):
            # return the relative id
            return self._board[0, 0]
        # if a player has completed the secondary diagonal
        if self._board[0, -1] != -1 and all(
            [self._board[x, -(x + 1)]
             for x in range(self._board.shape[0])] == self._board[0, -1]
        ):
            # return the relative id
            return self._board[0, -1]
        return -1

    def play(self, player1: Player, player2: Player) -> int:
        '''Play the game. Returns the winning player'''
        players = [player1, player2]
        winner = -1
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(
                    self)
                ok = self.__move(from_pos, slide, self.current_player_idx)
            winner = self.check_winner()
        return winner

    def __move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.__take((from_pos[1], from_pos[0]), player_id)
        if acceptable:
            acceptable = self.__slide((from_pos[1], from_pos[0]), slide)
            if not acceptable:
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def __take(self, from_pos: tuple[int, int], player_id: int) -> bool:
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (self._board[from_pos] < 0 or self._board[from_pos] == player_id)
        if acceptable:
            self._board[from_pos] = player_id
        return acceptable

    def __slide(self, from_pos: tuple[int, int], slide: Move) -> bool:
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = self._board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                self._board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], self._board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    self._board[(i, from_pos[1])] = self._board[(
                        i - 1, from_pos[1])]
                # move the piece up
                self._board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], self._board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    self._board[(i, from_pos[1])] = self._board[(
                        i + 1, from_pos[1])]
                # move the piece down
                self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable

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




import numpy as np

class SymmetryGenerator:

    ############################
    # SYMMETRIES FOR THE BOARD #
    ############################

    def __init__(self):
        self.transforms = [
            ("identity", self.identity),
            ("rotate_90", self.rotate_90),
            ("rotate_180", self.rotate_180),
            ("rotate_270", self.rotate_270),
            ("reflect_horizontal", self.reflect_horizontal),
            ("reflect_vertical", self.reflect_vertical),
            ("reflect_diagonal", self.reflect_diagonal),
            ("reflect_antidiagonal", self.reflect_antidiagonal)
        ]

    def identity(self, board):
        return board

    def rotate_90(self, board):
        return np.rot90(board)

    def rotate_180(self, board):
        return np.rot90(board, k=2)

    def rotate_270(self, board):
        return np.rot90(board, k=3)

    def reflect_horizontal(self, board):
        return np.fliplr(board)

    def reflect_vertical(self, board):
        return np.flipud(board)

    def reflect_diagonal(self, board):
        return np.transpose(board)

    def reflect_antidiagonal(self, board):
        return np.flip(np.transpose(board), axis=1)

    def get_symmetries(self, board):
        symmetries = [(label, transform(board)) for label, transform in self.transforms]
        return symmetries
    
    ##########################
    # SYMMETRIES FOR ACTIONS #
    ##########################

    def get_base_action(self, from_pos: tuple[int, int], slide: Move, symmetry_to_apply: str):

        # 1. Get the transformation to apply
        transf = getattr(self, symmetry_to_apply)

        # 2. Apply the symmetry to the from_pos
        from_pos = transf(from_pos)

        # 3. Apply the symmetry to the slide
        slide = transf(slide)

        # 4. Return the transformed action
        return from_pos, slide
    
    def get_original_action(self, from_pos: tuple[int, int], slide: Move, symmetry_to_reverse: str):
        



    # COORDINATES SYMMETRIES

    def identity(self, from_pos: tuple[int, int]):
        # Return the position (y, x) unchanged
        return from_pos
    
    def rotate_90(self, from_pos: tuple[int, int]):
        # Rotate a position (y, x) by 90 degrees on a 5x5 board
        return 4-from_pos[1], from_pos[0]
    
    def rotate_180(self, from_pos: tuple[int, int]):
        # Rotate a position (y, x) by 180 degrees on a 5x5 board
        return 4-from_pos[0], 4-from_pos[1]
    
    def rotate_270(self, from_pos: tuple[int, int]):
        # Rotate a position (y, x) by 270 degrees on a 5x5 board
        return from_pos[1], 4-from_pos[0]
    
    def reflect_horizontal(self, from_pos: tuple[int, int]):
        # Reflect a position (y, x) horizontally on a 5x5 board
        return from_pos[0], 4-from_pos[1]

    def reflect_vertical(self, from_pos: tuple[int, int]):
        # Reflect a position (y, x) vertically on a 5x5 board
        return 4-from_pos[0], from_pos[1]
    
    def reflect_diagonal(self, from_pos: tuple[int, int]):
        # Reflect a position (y, x) along the diagonal on a 5x5 board
        return from_pos[1], from_pos[0]

    def reflect_antidiagonal(self, from_pos: tuple[int, int]):
        # Reflect a position (y, x) along the antidiagonal on a 5x5 board
        return 4-from_pos[1], 4-from_pos[0]
    
    # SLIDE MOVE SYMMETRIES
    def identity(self, slide: Move):
        # Return the slide unchanged
        return slide
    
    def rotate_90(self, slide: Move):
        # Rotate a slide by 90 degrees
        if slide == Move.TOP: return Move.RIGHT
        elif slide == Move.BOTTOM: return Move.LEFT
        elif slide == Move.LEFT: return Move.TOP
        elif slide == Move.RIGHT: return Move.BOTTOM

    def rotate_180(self, slide: Move):
        # Rotate a slide by 180 degrees
        if slide == Move.TOP: return Move.BOTTOM
        elif slide == Move.BOTTOM: return Move.TOP
        elif slide == Move.LEFT: return Move.RIGHT
        elif slide == Move.RIGHT: return Move.LEFT

    def rotate_270(self, slide: Move):
        # Rotate a slide by 270 degrees
        if slide == Move.TOP: return Move.LEFT
        elif slide == Move.BOTTOM: return Move.RIGHT
        elif slide == Move.LEFT: return Move.BOTTOM
        elif slide == Move.RIGHT: return Move.TOP

    def reflect_horizontal(self, slide: Move):
        # Reflect a slide horizontally
        if slide == Move.TOP: return Move.TOP
        elif slide == Move.BOTTOM: return Move.BOTTOM
        elif slide == Move.LEFT: return Move.RIGHT
        elif slide == Move.RIGHT: return Move.LEFT

    def reflect_vertical(self, slide: Move):
        # Reflect a slide vertically
        if slide == Move.TOP: return Move.BOTTOM
        elif slide == Move.BOTTOM: return Move.TOP
        elif slide == Move.LEFT: return Move.LEFT
        elif slide == Move.RIGHT: return Move.RIGHT

    def reflect_diagonal(self, slide: Move):
        # Reflect a slide along the diagonal
        if slide == Move.TOP: return Move.LEFT
        elif slide == Move.BOTTOM: return Move.RIGHT
        elif slide == Move.LEFT: return Move.TOP
        elif slide == Move.RIGHT: return Move.BOTTOM

    def reflect_antidiagonal(self, slide: Move):
        # Reflect a slide along the antidiagonal
        if slide == Move.TOP: return Move.RIGHT
        elif slide == Move.BOTTOM: return Move.LEFT
        elif slide == Move.LEFT: return Move.BOTTOM
        elif slide == Move.RIGHT: return Move.TOP
    

        


