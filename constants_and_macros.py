#-------------Macros------------#
M_RED = 0
M_BLUE = 1
M_GREEN = 2
M_YELLOW = 3
M_PURPLE = 4
M_ORANGE = 5
M_BROWN = 6
M_PINK = 7

M_ANTICLOCKWISE = 0
M_CLOCKWISE = 1

M_OUTWARDS = 0
M_INWARDS = 1

M_ROW = 0
M_COLUMN = 1

def MACRO_TO_COLOR(_macro):
    match _macro:
        case 0:
            return RED
        case 1:
            return BLUE
        case 2:
            return GREEN
        case 3:
            return YELLOW
        case 4:
            return PURPLE
        case 5:
            return ORANGE
        case 6:
            return BROWN
        case 7:
            return PINK
        
    return False

#-----------Constants--------#
#Basic and Essential
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#SCREEN_WIDTH = round(SCREEN_WIDTH/4)
#SCREEN_HEIGHT = round(SCREEN_HEIGHT/4)
CX = SCREEN_WIDTH/2
CY = SCREEN_HEIGHT/2


#Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 225, 53)
PURPLE = (191, 0, 255)
ORANGE = (255, 130, 0)
WHITE = (255, 255, 255)
BROWN = (89, 45, 0)
PINK = (241, 156, 187)
BLACK = (0, 0, 0)

BG_COLOR = WHITE
BOARD_COLORS = [M_RED, M_BLUE, M_GREEN, M_YELLOW, M_PURPLE, M_ORANGE, M_BROWN, M_PINK]
BOARD_GRID_COLOR = BLACK
GRID_THICKNESS = 2

INPUT_DIST_REGISTER = 0.6 #fraction of a cell a mouse has to move before movement locks in