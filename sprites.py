import pygame
from settings import *
import random


# Generic Base Class for Player and Enemies
class Actor:
    def __init__(self, game, x, y):
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def attack(self, target):
        target.current_hit_points -= self.attack_power
        if target.current_hit_points <= 0:
            target.kill()


    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def collide_with_enemy(self, mob, dx=0, dy=0):
        if mob.x == self.x + dx and mob.y == self.y + dy:
            return True
        return False

    def move(self, dx=0, dy=0):
        mob_collide = False
        for mob in self.game.mobs:
            if self.collide_with_enemy(mob, dx, dy):
                mob_collide = True
        if not self.collide_with_walls(dx, dy) and not mob_collide:
            self.x += dx
            self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


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








class Enemy(Actor, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        Actor.__init__(self, game, x, y)
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = 'Red Slime'
        self.level = 1
        self.image = self.game.enemy_icon
        self.max_hit_points = 20
        self.current_hit_points = 20
        self.attack_power = 10

# Mob AI movement needs to be refined still
    def take_turn(self, game):
        if (abs(self.x - game.player.x) == 1 and abs(self.y - game.player.y) == 0) or \
                (abs(self.x - game.player.x) == 0 and abs(self.y - game.player.y) == 1):
            self.attack(game.player)
            print(game.player.current_hit_points)
        elif abs(self.x - game.player.x) > abs(self.y - game.player.y) and self.x - game.player.x > 0:
            self.move(dx=-1)
        elif abs(self.x - game.player.x) > abs(self.y - game.player.y) and self.x - game.player.x < 0:
            self.move(dx=1)
        elif abs(self.x - game.player.x) < abs(self.y - game.player.y) and self.y - game.player.y > 0:
            self.move(dy=-1)
        elif abs(self.x - game.player.x) < abs(self.y - game.player.y) and self.y - game.player.y < 0:
            self.move(dy=1)
        elif abs(self.x - game.player.x) == abs(self.y - game.player.y):
            if random.randint(0, 2) == 0:
                self.move(dy=1)
            else:
                self.move(dx=1)


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE