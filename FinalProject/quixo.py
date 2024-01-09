"""
    quixo.py

    #TODO: Add a description of the file
"""

from game import Game, Move, Player


class Quixo(Game):
    def __init__(self) -> None:
        super().__init__()
    
    def print(self, win: bool = False):
        """
        Prints the current player and the board in a more readable way
        - ⬜ are neutral pieces
        - ❌ are pieces of player 0
        - 🔘 are pieces of player 1
        """

        # 1. Print the current player or the winner
        symbol = "❌" if self.current_player_idx == 0 else "🔘"
        if win:
            print(f"\nPlayer {symbol} wins the game!")
        else:
            print(f"\nCurrent player: {symbol}")  
        
        # 2. Print the board
        print("*****************")
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
    
    def make_move(self, from_pos: tuple[int, int], slide: Move) -> bool:
        """Makes a move on the board."""
        return super()._Game__move(from_pos, slide, self.current_player_idx)
    
    def check_winner(self) -> int:
        """ Checks if there is a winner."""
        return super().check_winner()

    def change_player(self):
        """Changes the current player."""
        self.current_player_idx = 1 - self.current_player_idx

    def play(self, player1: Player, player2: Player, verbose: bool=False, debug: bool=False) -> int:
        '''
          This function is a modified version of the play() function in the Game class.
          It allows the user to have more control over the visualization of each step of the game.
          - `verbose`: if True, prints the current player, the board and the moves tried by the players
          - `debug`: if True, prints the number and the list of all possible actions for the current player 
        '''

        # 1. Initialize the players
        players = [player1, player2]
            
        # 2. Play the game
        winner = -1
        while winner < 0:
            self.change_player()

            # 2.1. Print the board if verbose
            if verbose:
                self.print()
            
            # 2.2. DEBUG: Print the possible actions
            if debug:
                possible_actions = self.get_possible_actions()
                print("Number of possible actions:", len(possible_actions))
                print("Possible actions: ", possible_actions)
                
            # 2.3. Make the move of the current player
            ok = False
            while not ok:
                
                # 2.2.1. Get the move from the current player
                from_pos, slide = players[self.current_player_idx].make_move(self)
                
                # 2.2.2. Make the move and check if it was successful
                ok = self.make_move(from_pos, slide)

                # 2.2.3. VERBOSE: Print the move's outcome
                if verbose:
                    if ok:
                      print(f"Player {self.current_player_idx} moved ({from_pos}, {slide})")
                    else:
                      print(f"Player {self.current_player_idx} tried to move ({from_pos}, {slide}) but failed")
            
            # 2.4. Check if there is a winner
            winner = self.check_winner()

        # 3. VERBOSE: Print the final board and the winner
        if verbose:
            self.print(win=True)
        
        # 4. Return the winner
        return winner