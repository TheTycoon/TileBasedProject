import pygame

# Game Options and Settings

# define colors
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
GRAY       = (128, 128, 128)
RED        = (255,   0,   0)
ORANGE     = (255, 165,   0)
YELLOW     = (255, 255,   0)
GREEN      = (  0, 128,   0)
BLUE       = (  0,   0, 255)
PURPLE     = (128,   0, 128)
BROWN      = (165,  42,  42)
LIGHT_BLUE = (135, 206, 250)
SILVER     = (192, 192, 192)



# game settings
WIDTH = 1024
HEIGHT = 704
TILESIZE = 32
FPS = 60
TITLE = 'Tile-based Project'

# loads a font from the computer that most closely matches the name given
FONT = pygame.font.match_font('courier')
