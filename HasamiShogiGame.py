# Author: Kodie Artmayer
# Date: 11/18/2021
# Description: Program to play the abstract board gamed called Hasami Shogi.

class HasamiShogiGame:
    """class to represent all aspects of the Hasami Shogi game """

    def __init__(self):
        """constructor for the class, takes no parameters, initializes required
        data members.  All data members are private"""
        self._black = "BLACK"
        self._red = "RED"
        self._pieces = ["RED", "BLACK"]
        self._turn = "BLACK"
        self._state = "UNFINISHED"
        self._captured = {piece: 0 for piece in self._pieces}
        self._position = dict.fromkeys(self._pieces, None)
        self._board = [[0 if i == 0 else (1 if i == 8 else None) for j in range(9)] for i in range(9)]
        self._rowID = "abcdefghi"
        self._numID = dict(enumerate(self._pieces))
        self._numID[None] = None

    def get_game_state(self):
        """takes no parameters, returns the status of the game, finished, Red_won,
        or Black_won"""
        return self._state

    def get_active_player(self):
        """takes no parameters, returns whose turn it is, red or black"""
        return self._turn

    def get_num_captured_pieces(self, player):
        """takes one parameter player red or black, returns the number of pieces
        of that color that has been captured """
        return self._captured[player]

    def make_move(self, from_space, to_space):
        """method that makes a move for the game, if the wrong player has moved,
        the player moves the wrong colored piece, or if the move is illegal,
        or if the game has been won, returns false.  Otherwise completes the move,
        removes captured pieces, updates the game state and returns true"""
        #get the from space and the to space
        from_rowID, from_columnID = list(from_space)
        to_rowID, to_columnID = list(to_space)
        from_row_id, from_column_id = self._rowID.index(from_rowID), int(from_columnID)-1
        to_row_id, to_column_id = self._rowID.index(to_rowID), int(to_columnID)-1

        #check if move is valid
        if self._turn != self._numID[self._board[from_row_id][from_column_id]]:
            return False

        elif self._state != "UNFINISHED":
            return False

        elif from_row_id != to_row_id and from_column_id != to_column_id:
            return False

        else:
            #move the piece on the board
            self._board[from_row_id][from_column_id] = None
            self._board[to_row_id][to_column_id] = self._pieces.index(self._turn)
            #capture piece in row
            for rowID, row in enumerate(self._board):
                moving_piece = None
                last_piece = None
                captured = []
                check = False
                for place in row:
                    if place is not None and last_piece is not None:
                        moving_piece = place
                        check = True
                        captured = []
                    elif place is not None and last_piece is not None and check and place != moving_piece:
                        captured.append(row.index(place))
                    elif place is not None and last_piece is not None and check and place == moving_piece:
                        check = False
                        for spot_id in captured:
                            self._board[rowID][spot_id] = None
                            self._captured[self._turn] += 1
                        captured = []
                    elif place is None:
                        moving_piece = None
                        captured = []
                        check = False
                    last_piece = place

                #capture piece in column
                for row in zip(*self._board):
                    moving_piece = None
                    last_piece = None
                    captured = []
                    check = False
                    for place in row:
                        if place is not None and last_piece is None:
                            moving_piece = place
                            check = True
                            captured = []
                        elif place is not None and last_piece is not None and check and place != moving_piece:
                            captured.append(row.index(place))
                        elif place is not None and last_piece is not None and check and place == moving_piece:
                            check = False
                            for spot_id in captured:
                                self._board[spot_id][rowID] = None
                                self._captured[self._turn] += 1
                            captured = []
                        elif place is None:
                            moving_piece = None
                            captured = []
                            check = False
                        last_piece = place
                    rowID += 1

                #capture in corner
                for i in range(-1, 1):
                    for spot_id, value in enumerate(self._board[i]):
                        if value is not None and value != self._pieces.index(self._turn):
                            possible_id = spot_id - 1, spot_id + 1
                            if all(0 <= j < len(self._board[i]) for j in possible_id):
                                if (self._board[i][spot_id - 1] == self._pieces.index(self._turn)) or (
                                        self._board[i][spot_id + 1] == self._pieces.index(self._turn)):
                                    if i == -1:
                                        if self._board[i - 1][spot_id] == self._pieces.index(self._turn):
                                            self._board[i][spot_id] = None
                                            self._captured[self._turn] += 1
                            elif 0 < spot_id - 1 < len(self._board[i]):
                                if self._board[i][spot_id - 1] == self._pieces.index(self._turn):
                                    if i == -1:
                                        if self._board[i - 1][spot_id] == self._pieces.index(self._turn):
                                            self._board[i][spot_id] = None
                                            self._captured[self._turn] += 1
                            elif 0 < spot_id + 1 < len(self._board[i]):
                                if self._board[i][spot_id + 1] == self._pieces.index(self._turn):
                                    if i == -1:
                                        if self._board[i - 1][spot_id] == self._pieces.index(self._turn):
                                            self._board[i][spot_id] = None
                                            self._captured[self._turn] += 1
                #update game
                if any(self._captured[piece] >= 8 for piece in self._captured):
                    if self._captured[self._red] >= 8:
                        self._state = "RED WON"
                    else:
                        self._state = "BLACK WON"
                else:
                    self._state = "UNFINISHED"
            self._turn = "BLACK" if self._turn == "RED" else "RED"
            return True

    def get_square_occupant(self, position):
        """method that takes one parameter, a string that represents a square
        on the board and returns what piece Red, Black, or None depending on what
        occupies that square"""
        rowID, columnID = list(position)
        row_id, column_id = self._rowID.index(rowID), int(columnID)-1
        return self._numID[self._board[row_id][column_id]] if self._board[row_id][column_id] else 'NONE'

    def print_board(self):
        """method that takes no parameters, used to display the board
        in the current state of the game"""
        dict_value = {0: 'R', 1: 'B', None: '.'}
        for num in range(0,10):
            if num == 0:
                print(" ", end=" ")
            elif num != 9:
               print(num, end=" ")
            else:
                print(num, end="\n")

        for id, row in enumerate(self._board):
            for i, spot in enumerate(row):
                if i == 0:
                    print(self._rowID[id]+" "+dict_value[spot], end=" ")
                elif i != len(row) - 1:
                    print(dict_value[spot], end=" ")
                else:
                    print(dict_value[spot], end="\n")
        print("")