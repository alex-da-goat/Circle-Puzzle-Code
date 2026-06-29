from constants_and_macros import *
from generic import *
import math as m

class User_Input:
    def __init__(self, _radius, _center, _num_of_rows, _num_of_columns):
        self.radius = _radius
        self.center = _center
        self.num_of_rows = _num_of_rows
        self.num_of_columns = _num_of_columns

        #Cell-to-cell input method
        self.mouse_down_last_time_checked = False
        self.mouse_pos_last_time_checked = (-1, -1)

        #Lock-in input method
        self.cell_locked_into = None
        self.locked_into_rows_or_columns = None

    
    #Cell-to-cell input (it feels unresponsive and janky)
    """def update(self, _mouse_pos, _mouse_down): 
        if _mouse_down:
            if not self.mouse_down_last_time_checked:

                self.mouse_pos_last_time_checked = _mouse_pos
                self.mouse_down_last_time_checked = True
        else:
            if self.mouse_down_last_time_checked:
                self.mouse_down_last_time_checked = False    
                
                old_cell = self.get_cell(self.mouse_pos_last_time_checked)
                new_cell = self.get_cell(_mouse_pos)
                if (old_cell != new_cell) and (old_cell != False) and (new_cell != False):
                    if old_cell[0] == new_cell[0]: #row rotation
                        spaces_to_move = ( new_cell[1]-old_cell[1] + self.num_of_columns) % self.num_of_columns
                        return {
                            "row_or_column_changing" : M_ROW,
                            "index_of_row_or_column" : old_cell[0],
                            "spaces_to_move" : spaces_to_move
                        }
                    if old_cell[1] == new_cell[1]: #column alteration
                        spaces_to_move = ( new_cell[0]-old_cell[0] + 2*self.num_of_rows) % (2*self.num_of_rows)
                        return {
                            "row_or_column_changing" : M_COLUMN,
                            "index_of_row_or_column" : old_cell[1],
                            "spaces_to_move" : spaces_to_move
                        }
        
        return False"""


    #Live response input, feels more responsive but does not have smooth animation
    def update(self, _mouse_pos, _mouse_down): 
        if _mouse_down:

            #If not currently locked in
            if self.cell_locked_into == None:
                if self.get_cell(_mouse_pos) != False:
                    self.cell_locked_into = self.get_cell(_mouse_pos)

            #If locked into cell but direction not decided yet
            elif self.locked_into_rows_or_columns == None:
                old_cell =  self.cell_locked_into
                new_cell = self.get_cell(_mouse_pos)

                if (new_cell != old_cell) and (new_cell != False):
                     #if only rows rotated (ie rows remained the same)
                    if new_cell[0] == old_cell[0]:
                        self.locked_into_rows_or_columns = M_ROW
                    #if only column rotated (ie columns remained the same)
                    elif new_cell[1] == old_cell[1]: 
                        self.locked_into_rows_or_columns = M_COLUMN
                    #if both changed, more the direction with greater displacement is chosen
                    else:
                        delta_radius = CARTESIAN_COORDS_TO_POLAR(_mouse_pos, self.center)[0] 
                        delta_radius -= CARTESIAN_COORDS_TO_POLAR(self.mouse_pos_last_time_checked, self.center)[0]
                        delta_angle = CARTESIAN_COORDS_TO_POLAR(_mouse_pos, self.center)[1] 
                        delta_angle -= CARTESIAN_COORDS_TO_POLAR(self.mouse_pos_last_time_checked, self.center)[1]
                        delta_angle = (delta_angle + 2*m.pi) % (2*m.pi)

                        if delta_angle / (2*m.pi) > delta_radius / self.radius:
                            self.locked_into_rows_or_columns = M_ROW
                        else:
                            self.locked_into_rows_or_columns = M_COLUMN

            #If already locked in with direction decided
            else:

                moving_cross_column = False

                old_cell = self.cell_locked_into
                #If locked into rows:
                if self.locked_into_rows_or_columns == M_ROW: 
                    angle_to_new_cell = CARTESIAN_COORDS_TO_POLAR(_mouse_pos, self.center)[1]
                    new_cell = self.get_cell_polar( ( (self.radius/10), angle_to_new_cell ) ) #the first parameter is just any value, a placeholder
                    new_cell = (old_cell[0], new_cell[1])
                #If locked into columns
                else:

                    #to calculate radius to new cell i use some cool maths!
                    x = _mouse_pos[0] - self.center[0]
                    y = _mouse_pos[1] - self.center[1]
                    angle = (old_cell[1]+0.5) / self.num_of_columns * (2*m.pi)
                    tangent_m = m.tan(angle)
                    if tangent_m == 0:
                        normal_m = 67676767
                    else:
                        normal_m = -1/m.tan(angle) #gradient of normal line
                    signed_radius = (x * normal_m + y) / m.sqrt(normal_m**2 + 1) #radius but could be negative.
                    if (angle > 0) and (angle < m.pi):
                        signed_radius *= -1
                    radius_to_new_cell = min( abs(signed_radius) , (self.num_of_rows-0.5) / self.num_of_rows * self.radius ) #radius WITHOUT A SIGN and given an upper bound
                    
                    #if new cell is same exact column (not cross column)
                    if signed_radius > 0:
                        new_cell = self.get_cell_polar( (radius_to_new_cell, 0.67) ) #the second parameter is just any value, a placeholder
                        new_cell = (new_cell[0], old_cell[1])
                    #if new cell is cross column
                    else:
                        new_cell = self.get_cell_polar( (radius_to_new_cell, 0.67) ) #the second parameter is just any value, a placeholder
                        new_column = int( (old_cell[1] + self.num_of_columns/2) % self.num_of_columns )
                        new_cell = (new_cell[0], new_column)
                        
                        moving_cross_column = True


                if (old_cell != new_cell) and (new_cell != False):

                    self.cell_locked_into = new_cell

                    if moving_cross_column: #column alteration but it goes cross column
                        spaces_to_move =  (old_cell[0]+1 + new_cell[0]  +2*self.num_of_rows ) % (2*self.num_of_rows)
                        return {
                            "row_or_column_changing" : M_COLUMN,
                            "index_of_row_or_column" : old_cell[1],
                            "spaces_to_move" : spaces_to_move,
                            "direction" : M_INWARDS
                        }

                    if old_cell[1] == new_cell[1]: #normal column alteration
                        spaces_to_move = ( new_cell[0]-old_cell[0] + 2*self.num_of_rows) % (2*self.num_of_rows)
                        return {
                            "row_or_column_changing" : M_COLUMN,
                            "index_of_row_or_column" : old_cell[1],
                            "spaces_to_move" : spaces_to_move,
                            "direction" : M_OUTWARDS
                        }

                    if old_cell[0] == new_cell[0]: #row rotation
                        spaces_to_move = ( new_cell[1]-old_cell[1] + self.num_of_columns) % self.num_of_columns
                        return {
                            "row_or_column_changing" : M_ROW,
                            "index_of_row_or_column" : old_cell[0],
                            "spaces_to_move" : spaces_to_move,
                            "direction" : M_ANTICLOCKWISE
                        }
                    
                    

        #if mouse up
        else:
            self.locked_into_rows_or_columns = None
            self.cell_locked_into = None

        return False



    def get_cell(self, _coords): #get cell (row, col) as a tuple by inputting polar coordinates
        radius = CARTESIAN_COORDS_TO_POLAR(_coords, self.center)[0]
        angle = CARTESIAN_COORDS_TO_POLAR(_coords, self.center)[1]

        if radius < self.radius:
            row = m.floor( radius/self.radius * self.num_of_rows )
            col = m.floor( angle/(2*m.pi) * self.num_of_columns )
            return (row, col)
        return False
    
    def get_cell_polar(self, _coords): #get cell (row, col) as a tuple by inputting polar coordinates
        radius = _coords[0]
        angle = _coords[1]

        if radius < self.radius:
            row = m.floor( radius/self.radius * self.num_of_rows )
            col = m.floor( angle/(2*m.pi) * self.num_of_columns )
            return (row, col)
        return False
    

