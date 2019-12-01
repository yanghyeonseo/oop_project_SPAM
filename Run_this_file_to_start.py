from init import *
from game_module import *
from screen_module import *


screen_start()
player1_num, player2_num = character_select()
background = map_select()
game_screen(player1_num, player2_num, background)