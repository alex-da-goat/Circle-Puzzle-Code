#-------------------------------Imports--------------------------------#
from constants_and_macros import *
from board_class import *
from user_input_class import *
import random as r

#---------------------------------Classes--------------------------------------#

class Game:

    def __init__(self, _num_of_rows, _num_of_columns, _num_of_colors):
        self.board = Board(_num_of_rows, _num_of_columns, _num_of_colors)
        self.user_input = User_Input(SCREEN_HEIGHT/2, (CX, CY), _num_of_rows, _num_of_columns)
    
    def update(self, _mouse_pos, _mouse_down):
        self.board.update()
        user_input = self.user_input.update(_mouse_pos, _mouse_down)
        if user_input != False:
            if user_input["row_or_column_changing"] == M_ROW: #if only row changed 
                self.board.rotate_row(user_input["index_of_row_or_column"], user_input["direction"], user_input["spaces_to_move"])
            elif user_input["row_or_column_changing"] == M_COLUMN: #if only column changed 
                self.board.alter_column_cross_column(user_input["index_of_row_or_column"], user_input["direction"], user_input["spaces_to_move"])

    def draw(self, _surface):
        self.board.draw(_surface)

    def scramble_board(self, *_num_of_scrambles):
        rows = self.board.get_num_of_rows()
        columns = self.board.get_num_of_columns()

        if len(_num_of_scrambles) == 0:
            num_of_scrambles = m.ceil(rows * columns / 5)
        else:
            num_of_scrambles = _num_of_scrambles[0]

        
        for i in range(num_of_scrambles):
            self.board.alter_column_cross_column(r.randint(0, columns-1), M_OUTWARDS, r.randint(0, columns-1))
            self.board.rotate_row(r.randint(0, rows-1), M_CLOCKWISE, r.randint(0, rows-1))


