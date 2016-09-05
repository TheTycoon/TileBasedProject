from sprites import *


class Player(Actor, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        Actor.__init__(self, game, x, y)
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.initial_x = x
        self.initial_y = y
        self.image = self.game.player_icon
        self.move_range = 1
        self.attack_range = 1
        self.spell_range = 2
        self.turn = 0

    def assign_class(self, event):
        if event.key == pygame.K_1:
            self.character_class = "Warrior"
            self.strength     = 4
            self.dexterity    = 2
            self.intelligence = 2
            self.agility      = 2
            self.endurance    = 4
            self.wisdom       = 1
        if event.key == pygame.K_2:
            self.character_class = "Archer"
            self.strength     = 2
            self.dexterity    = 4
            self.intelligence = 2
            self.agility      = 2
            self.endurance    = 3
            self.wisdom       = 2
        if event.key == pygame.K_3:
            self.character_class = "Mage"
            self.strength     = 2
            self.dexterity    = 2
            self.intelligence = 4
            self.agility      = 2
            self.endurance    = 2
            self.wisdom       = 3

        # All of the starting derived values based on stats
        self.max_hit_points = 5 + self.endurance * 3
        self.current_hit_points = self.max_hit_points
        self.max_mana_points = self.wisdom * 5
        self.current_mana_points = self.max_mana_points
        self.melee_attack_power = self.strength
        self.range_attack_power = self.dexterity
        self.magic_attack_power = self.intelligence
        self.melee_defense = self.strength + self.endurance
        self.range_defense = self.dexterity + self.agility
        self.magic_defense = self.intelligence + self.wisdom
        self.dodge_percent = self.agility
        self.level = 1

    def character_info(self):
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)

            # Start Drawing Frame
            self.game.screen.fill(BLACK)

            # Draw Info
            self.game.draw_text(self.game.screen, "Class: " + self.character_class, 32,
                                WHITE, 10, HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Level: " + str(self.level), 32,
                                WHITE, 10, 2 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "STR: " + str(self.strength), 32,
                                WHITE, 10, 4 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "DEX: " + str(self.dexterity), 32,
                                WHITE, 10, 5 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "INT: " + str(self.intelligence), 32,
                                WHITE, 10, 6 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "AGI: " + str(self.agility), 32,
                                WHITE, 10, 7 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "END: " + str(self.endurance), 32,
                                WHITE, 10, 8 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "WIS: " + str(self.wisdom), 32,
                                WHITE, 10, 9 * HEIGHT / 16, False)

            self.game.draw_text(self.game.screen, "Derived Statistics", 32, WHITE, WIDTH / 2, HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "HP  : " + str(self.current_hit_points) + "/" + str(self.max_hit_points),
                                32, WHITE, WIDTH / 2, 3 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "MP  : " + str(self.current_mana_points) + "/" + str(self.max_mana_points),
                                32, WHITE, WIDTH / 2, 4 * HEIGHT / 16, False)

            self.game.draw_text(self.game.screen, "Melee Attack  : " + str(self.melee_attack_power),
                                32, WHITE, WIDTH / 2, 5 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Melee Defense : " + str(self.melee_defense),
                                32, WHITE, WIDTH / 2, 6 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Ranged Attack : " + str(self.range_attack_power),
                                32, WHITE, WIDTH / 2, 7 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Ranged Defense: " + str(self.range_defense),
                                32, WHITE, WIDTH / 2, 8 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Magic Attack  : " + str(self.magic_attack_power),
                                32, WHITE, WIDTH / 2, 9 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Magic Defense : " + str(self.magic_defense),
                                32, WHITE, WIDTH / 2, 10 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Dodge Ability : " + str(self.agility) + "%",
                                32, WHITE, WIDTH / 2, 11 * HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Move Range    : " + str(self.move_range),
                                32, WHITE, WIDTH / 2, 12 * HEIGHT / 16, False)

            # End Drawing Frame
            pygame.display.flip()


            # Get Events
            for event in pygame.event.get():
                # Quit if player exits game
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False

                # All keydown events
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.game.machine.cancel_menu()

    def initialize_turn(self):
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

    def draw_range_area(self, value, type, color):

        if type == 'straight':
            for i in range(value + 1):
                pygame.draw.rect(self.game.screen, color,
                                 ((self.x + i) * TILESIZE, self.y * TILESIZE,
                                  TILESIZE, TILESIZE))
                pygame.draw.rect(self.game.screen, color,
                                 ((self.x - i) * TILESIZE, self.y * TILESIZE,
                                  TILESIZE, TILESIZE))
                pygame.draw.rect(self.game.screen, color,
                                 (self.x * TILESIZE, (self.y + i) * TILESIZE,
                                  TILESIZE, TILESIZE))
                pygame.draw.rect(self.game.screen, color,
                                 (self.x * TILESIZE, (self.y - i) * TILESIZE,
                                  TILESIZE, TILESIZE))
        if type == 'filled':
            for i in range(0, value + 1):
                for j in range(0, value + 1):
                    if i + j <= value:
                        pygame.draw.rect(self.game.screen, color,
                                         ((self.x + i) * TILESIZE, (self.y + j) * TILESIZE,
                                          TILESIZE, TILESIZE))
                        pygame.draw.rect(self.game.screen, color,
                                         ((self.x + i) * TILESIZE, (self.y - j) * TILESIZE,
                                          TILESIZE, TILESIZE))
                        pygame.draw.rect(self.game.screen, color,
                                         ((self.x - i) * TILESIZE, (self.y + j) * TILESIZE,
                                          TILESIZE, TILESIZE))
                        pygame.draw.rect(self.game.screen, color,
                                         ((self.x - i) * TILESIZE, (self.y - j) * TILESIZE,
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

                if event.key == pygame.K_2:
                    self.targets = []
                    for mob in self.game.mobs:
                        if (abs(self.x - mob.x)  + abs(self.y - mob.y) <= self.spell_range):
                            self.targets.append(mob)
                    if self.targets:
                        self.selected_mob = self.targets[0]
                        self.game.machine.player_magic()

                if event.key == pygame.K_SPACE:
                    self.turn += 1
                    self.game.machine.end_player_turn()

                if event.key == pygame.K_c:
                    self.game.machine.open_character_menu()

        if self.game.machine.state == 'player_turn_attack':
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.selected_mob = self.targets[(self.targets.index(self.selected_mob) + 1) % len(self.targets)]

                if event.key == pygame.K_ESCAPE:
                    self.game.machine.cancel_attack()

                if event.key == pygame.K_RETURN:
                    self.attack(self.selected_mob)
                    self.turn += 1
                    self.game.machine.end_player_turn()

        if self.game.machine.state == 'player_turn_magic':
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.selected_mob = self.targets[(self.targets.index(self.selected_mob) + 1) % len(self.targets)]

                if event.key == pygame.K_ESCAPE:
                    self.game.machine.cancel_magic()

                if event.key == pygame.K_RETURN:
                    self.magic_attack(self.selected_mob)
                    self.turn += 1
                    self.game.machine.end_player_turn()