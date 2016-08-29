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


class Enemy(Actor, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        Actor.__init__(self, game, x, y)
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = 'Red Slime'
        self.level = 1
        self.image = self.game.enemy_icon
        self.max_hit_points = 15
        self.current_hit_points = 15
        self.attack_power = 10

# Mob AI movement needs to be refined still
    def take_turn(self):
        if (abs(self.x - self.game.player.x) == 1 and abs(self.y - self.game.player.y) == 0) or \
                (abs(self.x - self.game.player.x) == 0 and abs(self.y - self.game.player.y) == 1):
            self.attack(self.game.player)
            print(self.game.player.current_hit_points)
        elif abs(self.x - self.game.player.x) > abs(self.y - self.game.player.y) and self.x - self.game.player.x > 0:
            self.move(dx=-1)
        elif abs(self.x - self.game.player.x) > abs(self.y - self.game.player.y) and self.x - self.game.player.x < 0:
            self.move(dx=1)
        elif abs(self.x - self.game.player.x) < abs(self.y - self.game.player.y) and self.y - self.game.player.y > 0:
            self.move(dy=-1)
        elif abs(self.x - self.game.player.x) < abs(self.y - self.game.player.y) and self.y - self.game.player.y < 0:
            self.move(dy=1)
        elif abs(self.x - self.game.player.x) == abs(self.y - self.game.player.y):
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