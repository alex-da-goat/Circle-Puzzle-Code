#import numpy
from constants_and_macros import *
import pygame as pg
pg.init()
import math as m

#------------------Classes------------------#
class Board:
    def __init__(self, _num_of_rows, _num_of_columns, _num_of_colors):

        self.num_of_columns = _num_of_columns
        self.num_of_rows = _num_of_rows
        self.num_of_colors = _num_of_colors
        
        if self.num_of_columns % self.num_of_colors != 0:
            print("error! number of columns not divisible by number of colors!")
            return False
        if self.num_of_columns % 2 != 0:
            print("error! number of rows must be even!")
            return False

        #Initialize array
        list = [ [None]*self.num_of_columns for i in range(self.num_of_rows)]
        columns_per_color = self.num_of_columns // self.num_of_colors
        for color_index in range(self.num_of_colors):
            for column in range(columns_per_color):
                for row in range(self.num_of_rows):
                    final_column = color_index*columns_per_color + column
                    list[row][final_column] = BOARD_COLORS[color_index]
        #self.array = numpy.array(list)
        self.array = list

    
    def draw(self, _surface):
        radius = min(_surface.get_width(), _surface.get_height())/2
        cell_radius_length = radius/self.num_of_rows
        cx = _surface.get_width()/2 #center x
        cy = _surface.get_height()/2 #center y

        #Drawing filled in spaces
        for row in range(self.num_of_rows):
            for column in range(self.num_of_columns):
                angle_start = (column/self.num_of_columns) * (2*m.pi)
                angle_stop = angle_start + ( 2*m.pi / self.num_of_columns )
                color = MACRO_TO_COLOR(self.array[row][column])
                circle_rect = pg.Rect(-1, -1, 2*cell_radius_length*(row+1), 2*cell_radius_length*(row+1))
                circle_rect.center = (cx, cy)
                pg.draw.arc(_surface, color, circle_rect, angle_start, angle_stop, m.floor(cell_radius_length))

        #Drawing radius line
        for row in range(self.num_of_rows):
            for column in range(self.num_of_columns):
                angle_start = (column/self.num_of_columns) * (2*m.pi)
                full_circle_rect = pg.Rect(-1, -1, radius, radius)
                full_circle_rect.center = (cx, cy)
                end_pos = (cx + radius*m.cos(angle_start), cy + radius*m.sin(angle_start))
                pg.draw.line(_surface, BOARD_GRID_COLOR, (cx, cy), end_pos, GRID_THICKNESS)

        #Drawing concentric circles
        for i in range(1, self.num_of_rows+1):
            pg.draw.circle(_surface, BOARD_GRID_COLOR, (cx, cy), i*cell_radius_length, GRID_THICKNESS)

    
    def rotate_row(self, _row, _clockwise_or_anticlockwise, _num_of_rotations):
        if _num_of_rotations < 0 or _num_of_rotations > self.num_of_columns:
            return False

        if _clockwise_or_anticlockwise == M_ANTICLOCKWISE:
            _num_of_rotations = self.num_of_columns - _num_of_rotations

        #Actually rotating
        temps = []
        for col in range(self.num_of_columns):
            if col < _num_of_rotations: #storing certain cells in temp variables to make the swap work
                temps.append(self.array[_row][col])

            col_to_copy_from = (col + _num_of_rotations) % self.num_of_columns
            if col + _num_of_rotations >= self.num_of_columns:
                self.array[_row][col] = temps[col_to_copy_from]
            else:
                self.array[_row][col] = self.array[_row][col_to_copy_from]
        del temps

    def alter_column(self, _col, _outwards_or_inwards, _num_of_alterations):
        if _num_of_alterations < 0 or _num_of_alterations > self.num_of_rows:
            return False

        if _outwards_or_inwards == M_OUTWARDS:
            _num_of_alterations = self.num_of_rows - _num_of_alterations

        #Actually altering
        temps = []
        for row in range(self.num_of_rows):
            if row < _num_of_alterations:
                temps.append(self.array[row][_col])

            row_to_copy_from = (row + _num_of_alterations) % self.num_of_rows
            if row + _num_of_alterations >= self.num_of_rows:
                self.array[row][_col] = temps[row_to_copy_from]
            else:
                self.array[row][_col] = self.array[row_to_copy_from][_col]
        del temps

    def alter_column_cross_column(self, _col, _outwards_or_inwards, _num_of_alterations):
        
        if _num_of_alterations < 0 or _num_of_alterations > 2*self.num_of_rows:
            return False

        if _outwards_or_inwards == M_OUTWARDS:
            _num_of_alterations = 2*self.num_of_rows - _num_of_alterations

        #setting tempory array to perform operation with
        both_columns_as_one = []
        for row in range(self.num_of_rows):
            both_columns_as_one.append(self.array[row][_col])
        opposite_col = int( (_col + self.num_of_columns/2) % self.get_num_of_columns() )
        for row in range(self.num_of_rows):
            inverted_row = self.get_num_of_rows()-1 - row #has to be inverted cus way stuff is oriented, just trust me bro 
            both_columns_as_one.append(self.array[inverted_row][opposite_col])
        #both_columns_as_one = numpy.array(both_columns_as_one)

        #altering both_columns_as_one
        temps = []
        for cell in range(len(both_columns_as_one)):
            if cell < _num_of_alterations:
                temps.append(both_columns_as_one[cell])

            cell_to_copy_from = (cell + _num_of_alterations) % len(both_columns_as_one)
            if cell + _num_of_alterations >= len(both_columns_as_one):
                both_columns_as_one[cell] = temps[cell_to_copy_from]
            else:
                both_columns_as_one[cell] = both_columns_as_one[cell_to_copy_from]

        #actually changing self.array to values from both_columns_as_one
        #changing original column
        for row in range(self.num_of_rows): 
            self.array[row][_col] = both_columns_as_one[row]
        #changing opposite column
        opposite_col = int( (_col + self.num_of_columns/2) % self.get_num_of_columns() )
        for row in range(self.num_of_rows):
            inverted_row = self.get_num_of_rows()-1 - row #has to be inverted cus way stuff is oriented, just trust me bro 
            self.array[inverted_row][opposite_col] = both_columns_as_one[self.num_of_rows + row]


        del temps
        del both_columns_as_one


    def update(self):
        pass


    def get_num_of_rows(self):
        return self.num_of_rows
    
    def get_num_of_columns(self):
        return self.num_of_columns
    
    def get_num_of_colors(self):
        return self.num_of_color