import pygame
from settings import *
import random


# Generic Base Class for Player and Enemies
class Actor:
    def __init__(self, game, x, y):
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def attack(self, target):
        target.hit_points -= self.attack_power
        if target.hit_points == 0:
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
        self.image.fill(BLUE)
        self.hit_points = 100
        self.attack_power = 10
        self.move_range = 2
        self.turn = 0

    def start_turn(self):
        self.initial_x = self.x
        self.initial_y = self.y

    def draw_move_area(self):
        for i in range(0, self.move_range + 1):
            for j in range(0, self.move_range + 1):
                if i + j <= self.move_range:
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

    def take_turn(self, game, event):
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


            # player attack push '1'
            if event.key == pygame.K_1:
                for mob in game.mobs:
                    if (abs(self.x - mob.x) == 1 and abs(self.y - mob.y) == 0) or \
                            (abs(self.x - mob.x) == 0 and abs(self.y - mob.y) == 1):
                        self.attack(mob)
                        self.turn += 1
                        game.end_player_turn()

            if event.key == pygame.K_SPACE:
                self.turn += 1
                game.end_player_turn()


class Enemy(Actor, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        Actor.__init__(self, game, x, y)
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image.fill(RED)
        self.hit_points = 10
        self.attack_power = 10

# Mob AI movement needs to be refined still
    def take_turn(self, game):
        if (abs(self.x - game.player.x) == 1 and abs(self.y - game.player.y) == 0) or \
                (abs(self.x - game.player.x) == 0 and abs(self.y - game.player.y) == 1):
            self.attack(game.player)
            print(game.player.hit_points)
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