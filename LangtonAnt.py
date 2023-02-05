# Author: Kodie Artmayer
# Date: 8/3/2021
# Description: A Langton's Ant simulation where a user constructs the size of the board
#              and which direction the ant should move and the program prints the result

def main():
    """
    function to collect input data for simulation
    """
    print("Welcome to Langton's ant simulation!")
    size = int(input("First, Please enter a number no larger than 100 for the size of the square board:"))
    row = int(input("Choose the ant's starting location, please enter a number as the starting row number"
                    "(where 0 is the first row from the top): "))
    column = int(input("Please enter a number a the starting column number"
                       "(where 0 is the first column from the left): "))
    direction = int(input("Please choose the ant's starting orientation, "
                          "0 for up, 1 for right, 2 for down, 3 for left: "))
    number_of_steps = int(input("Please enter the number of steps for the simulation: "))
    ant_placement = Ant(size, row, column, direction)
    for i in range(number_of_steps):
        ant_placement.run_simulation()
    print('')
    ant_placement.print_board()


class Ant:
    """
    class establishing initial data values for the size of the board, direction of the ant
    and the starting position of the ant
    """

    def __init__(self, size, init_row, init_column, direction):
        self.__size = size
        self.__board = [['_' for j in range(size)] for i in range(size)]
        self.__row_position = init_row
        self.__column_position = init_column
        self.__direction = direction

    def run_simulation(self):
        """
        function to carry out the movement of the ant and make changes to the board
        """
        if self.__board[self.__row_position][self.__column_position] == '_':
            self.__board[self.__row_position][self.__column_position] = '#'

        if self.__direction == 0:
            self.__direction = 1
            self.__column_position = self.__column_position + 1
            self.__column_position = self.__column_position % self.__size

        elif self.__direction == 1:
            self.__direction = 2
            self.__row_position = self.__row_position + 1
            self.__row_position = self.__row_position % self.__size

        elif self.__direction == 2:
            self.__direction = 3
            self.__column_position = self.__column_position - 1
            if self.__column_position < 0:
                self.__column_position = self.__size - 1

        elif self.__direction == 3:
            self.__direction = 0
            self.__row_position = self.__row_position - 1
            if self.__row_position < 0:
                self.__row_position = self.__size - 1

        elif self.__board[self.__row_position][self.__column_position] == '#':
            self.__board[self.__row_position][self.__column_position] = '_'

            if self.__direction == 0:
                self.__direction = 3
                self.__column_position = self.__column_position - 1
                if self.__column_position < 0:
                    self.__column_position = self.__size - 1

            elif self.__direction == 1:
                self.__direction = 0
                self.__row_position = self.__row_position - 1
                if self.__row_position < 0:
                    self.__row_position = self.__size - 1

            elif self.__direction == 2:
                self.__direction = 1
                self.__column_position = self.__column_position + 1
                self.__column_position = self.__column_position % self.__size

            elif self.__direction == 3:
                self.__direction = 2
                self.__row_position = self.__row_position + 1
                self.__row_position = self.__row_position % self.__size

    def print_board(self):
        """
        function to display board after moves have been made
        """
        for i in range(self.__size):
            for j in range(self.__size):
                if i == self.__row_position and j == self.__column_position:
                    print(8, end='')
                else:
                    print(self.__board[i][j], end='')
            print()


main()



