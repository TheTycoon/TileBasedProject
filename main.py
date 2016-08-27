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
        # Easy names to start file directories
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        # load all image and sound files
        self.attack_icon = pygame.image.load(path.join(img_folder, 'sword1.png')).convert_alpha()
        self.magic_icon = pygame.image.load(path.join(img_folder, 'fireball.png')).convert_alpha()


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

    # Double Check These Functions / Make Better - Use x & y to draw text position as well
    def draw_health_bar(self, self_screen, x, y, percentage):
        if percentage < 0:
            percentage = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        filled = (percentage / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pygame.Rect(x, y, filled, BAR_HEIGHT)
        pygame.draw.rect(self_screen, RED, filled_rect)
        pygame.draw.rect(self_screen, WHITE, outline_rect, 2)
        self.draw_text(self.screen, "Health", 12, WHITE, WIDTH - 130, HEIGHT - 36)

    def draw_mana_bar(self, self_screen, x, y, percentage):
        if percentage < 0:
            percentage = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        filled = (percentage / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pygame.Rect(x, y, filled, BAR_HEIGHT)
        pygame.draw.rect(self_screen, BLUE, filled_rect)
        pygame.draw.rect(self_screen, WHITE, outline_rect, 2)
        self.draw_text(self.screen, "Mana", 12, WHITE, WIDTH - 130, HEIGHT - 21)

    def draw_ui(self):
        pygame.draw.rect(self.screen, GRAY, (0, HEIGHT - 40, WIDTH, 40))
        for i in range(10):
            pygame.draw.rect(self.screen, SILVER, (5 + ((5 + TILESIZE) * i), HEIGHT - 36, 32, 32))



        attack_icon = self.attack_icon
        attack_rect = attack_icon.get_rect()
        attack_rect.x = 5
        attack_rect.y = HEIGHT - 36
        self.screen.blit(attack_icon, attack_rect)

        magic_icon = self.magic_icon
        magic_rect = attack_icon.get_rect()
        magic_rect.x = 5 + (5 + TILESIZE)
        magic_rect.y = HEIGHT - 36
        self.screen.blit(magic_icon, magic_rect)

        for i in range(10):
            self.draw_text(self.screen, str((i + 1) % 10), 12, BLACK, 10 + ((5 + TILESIZE) * i), HEIGHT - 36)

    # function to handle drawing all types text
    def draw_text(self, surface, text, size, color, x, y):
        font = pygame.font.Font(FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)  # centers the text
        surface.blit(text_surface, text_rect)


    def draw(self):
        # SHOW FPS IN TITLE BAR WHILE TESTING
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # DRAW EVERYTHING FOR ONE FRAME
        self.screen.fill(BLACK)

        if self.state == 'player turn':
            self.player.draw_move_area()

        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_ui()
        self.draw_health_bar(self.screen, WIDTH - 105, HEIGHT - 35, self.player.hit_points)
        self.draw_mana_bar(self.screen, WIDTH - 105, HEIGHT - 20, self.player.mana_points)

        self.player.draw_spell_area()

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


