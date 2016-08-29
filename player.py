from sprites import *


class Player(Actor, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        Actor.__init__(self, game, x, y)
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.initial_x = x
        self.initial_y = y
        self.image = self.game.player_icon
        self.max_hit_points = 100
        self.current_hit_points = 100
        self.max_mana_points = 100
        self.current_mana_points = 100
        self.attack_power = 10
        self.move_range = 2
        self.attack_range = 1
        self.turn = 0

    def initialize_turn(self):
        self.initial_x = self.x
        self.initial_y = self.y

    def draw_filled_area(self, value):
        for i in range(0, value + 1):
            for j in range(0, value + 1):
                if i + j <= value:
                    pygame.draw.rect(self.game.screen, YELLOW,
                                     ((self.initial_x + i) * TILESIZE, (self.initial_y + j) * TILESIZE,
                                      TILESIZE, TILESIZE))
                    pygame.draw.rect(self.game.screen, YELLOW,
                                     ((self.initial_x + i) * TILESIZE, (self.initial_y - j) * TILESIZE,
                                      TILESIZE, TILESIZE))
                    pygame.draw.rect(self.game.screen, YELLOW,
                                     ((self.initial_x - i) * TILESIZE, (self.initial_y + j) * TILESIZE,
                                      TILESIZE, TILESIZE))
                    pygame.draw.rect(self.game.screen, YELLOW,
                                     ((self.initial_x - i) * TILESIZE, (self.initial_y - j) * TILESIZE,
                                      TILESIZE, TILESIZE))

    def draw_straight_area(self, value):
        for i in range(value + 1):
            pygame.draw.rect(self.game.screen, LIGHT_BLUE,
                             ((self.x + i) * TILESIZE, self.y * TILESIZE,
                              TILESIZE, TILESIZE))
            pygame.draw.rect(self.game.screen, LIGHT_BLUE,
                             ((self.x - i) * TILESIZE, self.y * TILESIZE,
                              TILESIZE, TILESIZE))
            pygame.draw.rect(self.game.screen, LIGHT_BLUE,
                             (self.x * TILESIZE, (self.y + i) * TILESIZE,
                              TILESIZE, TILESIZE))
            pygame.draw.rect(self.game.screen, LIGHT_BLUE,
                             (self.x * TILESIZE, (self.y - i) * TILESIZE,
                              TILESIZE, TILESIZE))

    def take_turn(self, event):
        if self.game.machine.state == 'player_turn_moving':
            if event.type == pygame.KEYDOWN:
                # player movement
                if event.key == pygame.K_LEFT and abs(self.initial_x - (self.x - 1)) + abs(self.initial_y - self.y) <= self.move_range:
                    self.move(dx=-1)
                if event.key == pygame.K_RIGHT and abs(self.initial_x - (self.x + 1)) + abs(self.initial_y - self.y) <= self.move_range:
                    self.move(dx=1)
                if event.key == pygame.K_UP and abs(self.initial_y - (self.y - 1)) + abs(self.initial_x - self.x) <= self.move_range:
                    self.move(dy=-1)
                if event.key == pygame.K_DOWN and abs(self.initial_y - (self.y + 1)) + abs(self.initial_x - self.x) <= self.move_range:
                    self.move(dy=1)

                if event.key == pygame.K_1:
                    self.targets = []
                    for mob in self.game.mobs:
                        if (abs(self.x - mob.x) <= self.attack_range and abs(self.y - mob.y) == 0) or \
                                (abs(self.x - mob.x) == 0 and abs(self.y - mob.y) <= self.attack_range):
                            self.targets.append(mob)
                    if self.targets:
                        self.selected_mob = self.targets[0]
                        self.game.machine.player_attack()

                if event.key == pygame.K_SPACE:
                    self.turn += 1
                    self.game.machine.end_player_turn()

        if self.game.machine.state == 'player_turn_attack':
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.selected_mob = self.targets[(self.targets.index(self.selected_mob) + 1) % len(self.targets)]

                if event.key == pygame.K_ESCAPE:
                    self.game.machine.cancel_attack()

                if event.key == pygame.K_RETURN:
                    self.attack(self.selected_mob)
                    self.game.machine.end_player_turn()