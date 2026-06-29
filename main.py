#--------------------------Imports-------------------------------#
import asyncio
import pygame as pg
pg.init()
from constants_and_macros import *
from board_class import *
from game_class import *
import random as r
import math as m

#--------------------------Initialization-----------------------#
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True
dt = 0.1

game = Game(3, 6, 3)
#game.scramble_board()
"""for row in range(board.get_num_of_rows()):
    board.rotate_row(row, M_CLOCKWISE, row)"""
#board.alter_column_cross_column(1, M_OUTWARDS, 1)

#--------------------------------Game Loop---------------------------------------#

async def main():
    global running
    while running:
        #----------------Events-------------#
        for event in pg.event.get():
            #QUIT GAME
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    game.scramble_board()
                if event.key == pg.K_w:
                    pass#game.board.rotate_row(0, M_CLOCKWISE, 1)
                
                

        #--------------Mouse---------------#
        mouse_pos = pg.mouse.get_pos()
        mouse_down = pg.mouse.get_pressed()[0]


        #---------------Updating--------------#
        game.update(mouse_pos, mouse_down)

        #--------------Drawing--------------#
        screen.fill(BG_COLOR)
        game.draw(screen)
        pg.display.flip()
        
        #-------------Delta Time--------------#
        dt = clock.tick(60) / 1000
        dt = max(0.001, min(0.1, dt))

        #-----=------Async stuff--------------#
        await asyncio.sleep(0)


asyncio.run(main())