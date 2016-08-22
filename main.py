import pygame
from pygame.locals import *
from os import path

from settings import *
from sprites import *

from transitions import Machine         # State Machine


class Game:

    # Define States for State Machine
    states = ['player turn', 'enemy turn']

    def __init__(self):
        # initialize game window, sound interaction, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()    # start the clock...
        self.running = True
        self.load_data()
        self.machine = Machine(model=self, states=self.states, initial='player turn')

        # Add Transitions to State Machine
        self.machine.add_transition(trigger='end_player_turn', source='player turn', dest='enemy turn')
        self.machine.add_transition('end_enemy_turn', 'enemy turn', 'player turn')

    def load_data(self):
        # load all image and sound files

        # Easy name to start file directory
        game_folder = path.dirname(__file__)

        # Load map from text file
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as file:
            for line in file:
                self.map_data.append(line)

    def new(self):
        # start a new game

        # Declare Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        # Iterate through the map.txt file to initialize the player and starting walls
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    self.enemy = Enemy(self, col, row)
                if tile == '1':
                    Wall(self, col, row)

    def run(self):
        self.playing = True

        # Game Loop
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # update everything that needs updating
        self.all_sprites.update()

    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():

            # quit event / close window
            if event.type == QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # ALL KEYDOWN EVENTS HERE
            if event.type == pygame.KEYDOWN:

                # quit event / press esc
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

            # Take Turns
            if self.state == 'player turn':
                self.player.take_turn(game, event)
            elif self.state == 'enemy turn':
                for mob in self.mobs:
                    mob.take_turn(game)
                self.player.start_turn()
                self.end_enemy_turn()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))

    # Double Check This Function / Make Better
    def draw_health_bar(self, self_screen, x, y, percentage):
        if percentage < 0:
            percentage = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        filled = (percentage / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pygame.Rect(x, y, filled, BAR_HEIGHT)
        pygame.draw.rect(self_screen, GREEN, filled_rect)
        pygame.draw.rect(self_screen, WHITE, outline_rect, 2)

    def draw(self):
        # SHOW FPS IN TITLE BAR WHILE TESTING
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # DRAW EVERYTHING FOR ONE FRAME
        self.screen.fill(BLACK)

        self.player.draw_move_area()

        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_health_bar(self.screen, 5, 5, self.player.hit_points)


        # DISPLAY FRAME = STOP DRAWING
        pygame.display.flip()

    def show_start_screen(self):
        # Start Screen / Menu
        pass

    def show_end_screen(self):
        # Game Over Screen
        pass




game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.run()

    game.show_end_screen()

pygame.quit()


