from pygame.locals import *
from os import path

from player import *

from transitions.extensions import HierarchicalMachine as Machine


class Game:
    def __init__(self):
        # initialize game window, sound interaction, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()    # start the clock...
        self.running = True
        self.load_data()

        # Define States for State Machine
        states = ['enemy_turn', {'name': 'player_turn', 'children': ['moving', 'attack', 'magic']}]

        # Add Transitions for State Machine
        transitions  = [
            # trigger, source, destination
            ['end_player_turn', 'player_turn', 'enemy_turn'],
            ['end_enemy_turn', 'enemy_turn', 'player_turn_moving'],
            ['player_move', 'player_turn', 'player_turn_moving'],
            ['player_attack', 'player_turn_moving', 'player_turn_attack'],
            ['cancel_attack', 'player_turn_attack', 'player_turn_moving'],
            ['player_magic', 'player_turn_moving' ,'player_turn_magic'],
            ['cancel_magic', 'player_turn_magic', 'player_turn_moving']
        ]

        # Initialize State Machine
        self.machine = Machine(states=states, transitions=transitions,
                               initial='player_turn_moving', ignore_invalid_triggers=True)

    def load_data(self):
        # Easy names to start file directories
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        # load all image and sound files
        self.attack_icon = pygame.image.load(path.join(img_folder, 'sword1.png')).convert_alpha()
        self.magic_icon = pygame.image.load(path.join(img_folder, 'fireball.png')).convert_alpha()
        self.enemy_icon = pygame.image.load(path.join(img_folder, 'slime_red.png')).convert_alpha()
        self.player_icon = pygame.image.load(path.join(img_folder, 'player_image.png')).convert_alpha()


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

        # Iterate through the map.txt file to initialize the player and starting enemies/walls
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    Enemy(self, col, row)
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
                pass

            # Take Turns
            if self.machine.state == 'player_turn' or self.machine.state == 'player_turn_moving'\
                or self.machine.state == 'player_turn_attack' or self.machine.state == 'player_turn_magic':
                self.player.take_turn(event)

            elif self.machine.state == 'enemy_turn':
                for mob in self.mobs:
                    mob.take_turn()
                self.player.initialize_turn()
                self.machine.end_enemy_turn()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))

    # Double Check These Functions / Make Better - Use x & y to draw text position as well
    def draw_bar(self, self_screen, x, y, percentage, type):
        if type == 'health':
            color = RED
        if type == 'mana':
            color = BLUE
        if percentage < 0:
            percentage = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        filled = percentage * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pygame.Rect(x, y, filled, BAR_HEIGHT)
        pygame.draw.rect(self_screen, color, filled_rect)
        pygame.draw.rect(self_screen, WHITE, outline_rect, 2)

        if type == 'health':
            self.draw_text(self.screen, "Health", 12, WHITE, WIDTH - 130, HEIGHT - 36, True)
        if type == 'mana':
            self.draw_text(self.screen, "Mana", 12, WHITE, WIDTH - 130, HEIGHT - 21, True)

    def draw_enemy_info(self):
        image = self.player.selected_mob.image
        image_rect = image.get_rect()
        image_rect.x = WIDTH / 2
        image_rect.y = HEIGHT - 36
        self.screen.blit(image, image_rect)
        self.draw_text(self.screen, (self.player.selected_mob.name + ": Level " + str(self.player.selected_mob.level)), 12, WHITE, WIDTH / 2 + 50, HEIGHT - 36, False)
        self.draw_bar(self.screen, WIDTH / 2 + 50, HEIGHT - 20,
                      self.player.selected_mob.current_hit_points / self.player.selected_mob.max_hit_points, 'health')

    def draw_ui(self):
        # Draw Empty Action Bar
        pygame.draw.rect(self.screen, GRAY, (0, HEIGHT - 40, WIDTH, 40))
        for i in range(10):
            pygame.draw.rect(self.screen, SILVER, (5 + ((5 + TILESIZE) * i), HEIGHT - 36, 32, 32))

        # Draw Icons in Action Bar
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

        # Draw Numbers in Action Bar
        for i in range(10):
            self.draw_text(self.screen, str((i + 1) % 10), 12, BLACK, 10 + ((5 + TILESIZE) * i), HEIGHT - 36, True)

        # Draw Health and Mana Bars
        self.draw_bar(self.screen, WIDTH - 105, HEIGHT - 35,
                      self.player.current_hit_points / self.player.max_hit_points, 'health')
        self.draw_bar(self.screen, WIDTH - 105, HEIGHT - 20,
                      self.player.current_mana_points / self.player.max_mana_points, 'mana')

        # Draw a box to highlight the selected enemy and show enemy info in action bar
        if self.machine.state == 'player_turn_attack' or self.machine.state == 'player_turn_magic':
            pygame.draw.rect(self.screen, ORANGE, self.player.selected_mob.rect, 3)
            self.draw_enemy_info()

    # function to handle drawing all types text
    def draw_text(self, surface, text, size, color, x, y, centered):
        font = pygame.font.Font(FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y
        if centered:
            text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        # SHOW FPS IN TITLE BAR WHILE TESTING
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # DRAW EVERYTHING FOR ONE FRAME
        self.screen.fill(BLACK)

        # Draw highlighted area depending on what action is happening
        if self.machine.state == 'player_turn_moving':
            self.player.draw_move_area()
        if self.machine.state == 'player_turn_attack':
            self.player.draw_range_area(self.player.attack_range, 'straight', RED)
        if self.machine.state == 'player_turn_magic':
            self.player.draw_range_area(self.player.spell_range, 'filled', LIGHT_BLUE)

        # Draw all sprites, the grid, and the UI
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.draw_ui()



        # DISPLAY FRAME = STOP DRAWING
        pygame.display.flip()

    def show_start_screen(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)

            # Draw All Text To Screen
            self.draw_text(self.screen, TITLE, 50, WHITE, WIDTH / 2, HEIGHT / 4, True)
            self.draw_text(self.screen, "Choose a Class", 30, WHITE, WIDTH / 2, HEIGHT / 2, True)
            self.draw_text(self.screen, "1. Warrior", 20, WHITE, 3 * WIDTH / 8, 3 * HEIGHT / 4, True)
            self.draw_text(self.screen, "2. Archer", 20, WHITE, WIDTH / 2, 3 * HEIGHT / 4, True)
            self.draw_text(self.screen, "3. Mage", 20, WHITE, 5 * WIDTH / 8, 3 * HEIGHT / 4, True)
            pygame.display.flip()

            # Get Events / Player Chooses Their Class
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        waiting = False
                    if event.key == K_2:
                        waiting = False
                    if event.key == K_3:
                        waiting = False
                    if event.key == K_ESCAPE:
                        waiting = False
                        self.running = False


    def show_end_screen(self):
        # Game Over Screen
        pass

game = Game()
game.new()

while game.running:
    game.show_start_screen()
    game.run()

    game.show_end_screen()

pygame.quit()


