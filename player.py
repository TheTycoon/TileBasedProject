import settings
import pygame
import sprites
import weapons
import armors
import skills


class Player(sprites.Actor, pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        sprites.Actor.__init__(self, game, x, y)
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.initial_x = x
        self.initial_y = y
        self.image = self.game.player_icon
        self.max_action_points = 4
        self.current_action_points = 4
        self.attack_range = 3
        self.spell_range = 2
        self.spell_cost = 5
        self.turn = 0

        # inventory stuff
        self.melee_weapon = weapons.MELEE['none']
        self.shield = armors.SHIELD['none']
        self.ranged_weapon = weapons.RANGED['none']
        self.ammo_type = weapons.AMMO['none']
        self.ammo_amount = 0
        self.helmet = armors.HELMET['none']
        self.gloves = armors.GLOVES['none']
        self.chest = armors.CHEST['none']
        self.legs = armors.LEGS['none']
        self.boots = armors.BOOTS['none']
        self.amulet = "-"
        self.ring = "-"

    def assign_class(self, event):
        if event.key == pygame.K_1:
            self.character_class = "Warrior"
            # starting stats
            self.strength     = 4
            self.dexterity    = 2
            self.intelligence = 2
            self.agility      = 2
            self.endurance    = 4
            self.wisdom       = 1
            # starting inventory
            self.melee_weapon = weapons.MELEE['rusty_sword']
            self.legs = armors.LEGS['cloth_pants']
            self.actions = [self.game.sword_icon, self.game.dash_skill_icon]

            # starting skills - WIP
            self.skills = [skills.SKILL['Melee Attack']]


        if event.key == pygame.K_2:
            self.character_class = "Archer"
            # starting stats
            self.strength     = 2
            self.dexterity    = 4
            self.intelligence = 2
            self.agility      = 2
            self.endurance    = 3
            self.wisdom       = 2
            # starting inventory
            self.ranged_weapon = weapons.RANGED['slingshot']
            self.ammo_type = weapons.AMMO['rocks']
            self.ammo_amount = 25
            self.legs = armors.LEGS['cloth_pants']
            # starting skills, spells, used for action bar
            self.actions = [self.game.bare_hands_icon, self.game.slingshot_icon]

        if event.key == pygame.K_3:
            self.character_class = "Mage"
            # starting stats
            self.strength     = 1
            self.dexterity    = 2
            self.intelligence = 4
            self.agility      = 2
            self.endurance    = 2
            self.wisdom       = 4
            # starting inventory
            self.helmet = armors.HELMET['cloth_hat']
            self.chest = armors.CHEST['cloth_robe']
            self.actions = [self.game.bare_hands_icon, self.game.magic_icon]

        # All of the starting derived values based on stats
        self.max_hit_points = 5 + self.endurance * 3
        self.current_hit_points = self.max_hit_points
        self.max_mana_points = self.wisdom * 5
        self.current_mana_points = self.max_mana_points
        self.melee_attack_power = self.strength + int(0.5 * (self.dexterity + self.agility))
        self.range_attack_power = self.dexterity + int(0.5 * (self.strength + self.agility))
        self.magic_attack_power = self.intelligence + int(0.5 * (self.wisdom + self.endurance))
        self.melee_defense = int(0.5 * (self.strength + self.endurance))
        self.range_defense = int(0.5 * (self.dexterity + self.agility))
        self.magic_defense = int(0.5 * (self.intelligence + self.wisdom))
        self.dodge_percent = self.agility
        self.level = 1
        self.experience = 0
        self.next_level = 100

    def draw_sprite(self):
        temp_rect = self.image.get_rect()
        temp_rect.x = self.x * settings.TILESIZE
        temp_rect.y = (self.y - 1) * settings.TILESIZE       # lowers by 1 to handle a 32x64 sprite
        self.game.screen.blit(self.image, temp_rect)

    def draw_character_info(self):
        waiting = True
        while waiting:
            self.game.clock.tick(settings.FPS)

            # Start Drawing Frame
            self.game.screen.fill(settings.BLACK)

            # Draw Info
            self.game.draw_text(self.game.screen, self.character_class, 32,
                                settings.LIGHT_BLUE, 10, settings.HEIGHT / 16, False)

            self.game.draw_text(self.game.screen, "Level: " + str(self.level), 32,
                                settings.WHITE, 10, 3 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Experience: " + str(self.experience), 32,
                                settings.WHITE, 10, 4 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Next Level: " + str(self.next_level), 32,
                                settings.WHITE, 10, 5 * settings.HEIGHT / 16, False)

            self.game.draw_text(self.game.screen, "Basic Attributes", 32,
                                settings.LIGHT_BLUE, 10, 7 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Strength    : " + str(self.strength), 32,
                                settings.WHITE, 10, 8 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Endurance   : " + str(self.endurance), 32,
                                settings.WHITE, 10, 9 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Dexterity   : " + str(self.dexterity), 32,
                                settings.WHITE, 10, 10 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Agility     : " + str(self.agility), 32,
                                settings.WHITE, 10, 11 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Intelligence: " + str(self.intelligence), 32,
                                settings.WHITE, 10, 12 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Wisdom      : " + str(self.wisdom), 32,
                                settings.WHITE, 10, 13 * settings.HEIGHT / 16, False)

            pygame.draw.line(self.game.screen, settings.WHITE, (settings.WIDTH / 2 - 5, 0), (settings.WIDTH / 2 - 5, settings.HEIGHT), 5)

            self.game.draw_text(self.game.screen, "Derived Attributes", 32, settings.LIGHT_BLUE, settings.WIDTH / 2 + 10, settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "HP  : " + str(self.current_hit_points) + "/" + str(self.max_hit_points),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 3 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "MP  : " + str(self.current_mana_points) + "/" + str(self.max_mana_points),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 4 * settings.HEIGHT / 16, False)

            self.game.draw_text(self.game.screen, "Melee Attack  : " + str(self.melee_attack_power) + "+"
                                + str(self.melee_weapon['Damage']) + "=" + str(self.melee_attack_power + self.melee_weapon['Damage']),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 6 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Ranged Attack : " + str(self.range_attack_power),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 7 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Magic Attack  : " + str(self.magic_attack_power),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 8 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Melee Defense : " + str(self.melee_defense),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 9 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Ranged Defense: " + str(self.range_defense),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 10 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Magic Defense : " + str(self.magic_defense),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 11 * settings.HEIGHT / 16, False)

            self.game.draw_text(self.game.screen, "Dodge Chance  : " + str(self.agility) + "%",
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 13 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Action Points : " + str(self.max_action_points),
                                32, settings.WHITE, settings.WIDTH / 2 + 10, 14 * settings.HEIGHT / 16, False)

            # End Drawing Frame
            pygame.display.flip()

            # Get Events
            for event in pygame.event.get():
                # Quit if player exits game
                if event.type == pygame.QUIT:
                    waiting = False
                    self.game.running = False

                # All keydown events
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.game.machine.cancel_menu()

    def draw_inventory(self):
        waiting = True
        while waiting:
            self.game.clock.tick(settings.FPS)

            # Start Drawing Frame
            self.game.screen.fill(settings.BLACK)

            self.game.draw_text(self.game.screen, "Inventory", 32,
                                settings.LIGHT_BLUE, 10, settings.HEIGHT / 16, False)
            # WEAPONS
            self.game.draw_text(self.game.screen, "Melee Weapon : " + self.melee_weapon['Name'], 32,
                                settings.WHITE, 10, 3 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Shield       : " + self.shield['Name'], 32,
                                settings.WHITE, 10, 4 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Ranged Weapon: " + self.ranged_weapon['Name'], 32,
                                settings.WHITE, 10, 5 * settings.HEIGHT / 16, False)
            if self.ammo_amount == 0:
                self.game.draw_text(self.game.screen, "Ammo         : -", 32,
                                    settings.WHITE, 10, 6 * settings.HEIGHT / 16, False)
            else:
                self.game.draw_text(self.game.screen, "Ammo         : " + str(self.ammo_amount) + " x " + self.ammo_type['Name'], 32,
                                settings.WHITE, 10, 6 * settings.HEIGHT / 16, False)

                ammo_icon = self.game.rock_icon
                ammo_rect = ammo_icon.get_rect()
                ammo_rect.x = settings.WIDTH / 2
                ammo_rect.y = 6 * settings.HEIGHT / 16
                self.game.screen.blit(ammo_icon, ammo_rect)





            # ARMOR
            self.game.draw_text(self.game.screen, "Helmet       : " + self.helmet['Name'], 32,
                                settings.WHITE, 10, 8 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Gloves       : " + self.gloves['Name'], 32,
                                settings.WHITE, 10, 9 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Chest        : " + self.chest['Name'], 32,
                                settings.WHITE, 10, 10 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Legs         : " + self.legs['Name'], 32,
                                settings.WHITE, 10, 11 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Boots        : " + self.boots['Name'], 32,
                                settings.WHITE, 10, 12 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Amulet       : " + self.amulet, 32,
                                settings.WHITE, 10, 14 * settings.HEIGHT / 16, False)
            self.game.draw_text(self.game.screen, "Ring         : " + self.ring, 32,
                                settings.WHITE, 10, 15 * settings.HEIGHT / 16, False)

            # End Drawing Frame
            pygame.display.flip()

            # Get Events
            for event in pygame.event.get():
                # Quit if player exits game
                if event.type == pygame.QUIT:
                    waiting = False
                    self.game.running = False

                # All keydown events
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.game.machine.cancel_menu()

    def initialize_turn(self):
        self.initial_x = self.x
        self.initial_y = self.y
        self.current_action_points = self.max_action_points

    def draw_range_area(self, value, type, color):
        if type == 'radius':
            for i in range(0, value + 1):
                for j in range(0, value + 1):
                    if i + j <= value:
                        temp_surface = pygame.Surface((settings.TILESIZE, settings.TILESIZE))
                        temp_rect = temp_surface.get_rect()
                        temp_surface.fill(color, temp_rect)
                        temp_surface.set_alpha(100)

                        '''
                        Consider adding a list of these temp_rects and then
                        checking that list versus the list of wall tiles
                        coordinates...
                        draw the list at the end?
                        '''

                        if i == 0 and j != 0:
                            temp_rect.x = self.x * settings.TILESIZE
                            temp_rect.y = (self.y + j) * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                            temp_rect.x = self.x * settings.TILESIZE
                            temp_rect.y = (self.y - j) * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                        elif i != 0 and j == 0:
                            temp_rect.x = (self.x + i) * settings.TILESIZE
                            temp_rect.y = self.y * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                            temp_rect.x = (self.x - i) * settings.TILESIZE
                            temp_rect.y = self.y * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                        else:
                            temp_rect.x = (self.x + i) * settings.TILESIZE
                            temp_rect.y = (self.y + j) * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                            temp_rect.x = (self.x + i) * settings.TILESIZE
                            temp_rect.y = (self.y - j) * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                            temp_rect.x = (self.x - i) * settings.TILESIZE
                            temp_rect.y = (self.y + j) * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

                            temp_rect.x = (self.x - i) * settings.TILESIZE
                            temp_rect.y = (self.y - j) * settings.TILESIZE
                            self.game.screen.blit(temp_surface, temp_rect)

        if type == 'straight':
            for i in range(value + 1):
                temp_surface = pygame.Surface((settings.TILESIZE, settings.TILESIZE))
                temp_rect = temp_surface.get_rect()
                temp_surface.fill(color, temp_rect)
                temp_surface.set_alpha(100)

                temp_rect.x = self.x * settings.TILESIZE
                temp_rect.y = (self.y + i) * settings.TILESIZE
                self.game.screen.blit(temp_surface, temp_rect)

                temp_rect.x = self.x * settings.TILESIZE
                temp_rect.y = (self.y - i) * settings.TILESIZE
                self.game.screen.blit(temp_surface, temp_rect)

                temp_rect.x = (self.x + i) * settings.TILESIZE
                temp_rect.y = self.y * settings.TILESIZE
                self.game.screen.blit(temp_surface, temp_rect)

                temp_rect.x = (self.x - i) * settings.TILESIZE
                temp_rect.y = self.y * settings.TILESIZE
                self.game.screen.blit(temp_surface, temp_rect)

    def take_turn(self, event):
        # All of the actions you can do while able to move around
        if self.game.machine.state == 'player_turn_moving':
            if event.type == pygame.KEYDOWN:
                # player movement
                if event.key == pygame.K_LEFT:
                    self.move(dx=-1)
                    self.current_action_points -= 1
                    if self.current_action_points <= 0:
                        self.game.machine.end_player_turn()
                if event.key == pygame.K_RIGHT:
                    self.move(dx=1)
                    self.current_action_points -= 1
                    if self.current_action_points <= 0:
                        self.game.machine.end_player_turn()
                if event.key == pygame.K_UP:
                    self.move(dy=-1)
                    self.current_action_points -= 1
                    if self.current_action_points <= 0:
                        self.game.machine.end_player_turn()
                if event.key == pygame.K_DOWN:
                    self.move(dy=1)
                    self.current_action_points -= 1
                    if self.current_action_points <= 0:
                        self.game.machine.end_player_turn()

                # Use Actions in Action Bar
                if event.key == pygame.K_1:
                    self.targets = []
                    for mob in self.game.mobs:
                        if (abs(self.x - mob.x) <= self.attack_range and abs(self.y - mob.y) == 0) or \
                                (abs(self.x - mob.x) == 0 and abs(self.y - mob.y) <= self.attack_range):
                            self.targets.append(mob)
                    if self.targets:
                        self.selected_mob = self.targets[0]
                        self.game.machine.player_attack()

                if event.key == pygame.K_2 and self.current_mana_points >= self.spell_cost:
                    self.targets = []
                    for mob in self.game.mobs:
                        if (abs(self.x - mob.x)  + abs(self.y - mob.y) <= self.spell_range):
                            self.targets.append(mob)
                    if self.targets:
                        self.selected_mob = self.targets[0]
                        self.game.machine.player_magic()

                # Other actions (wait, open menus, etc.)
                if event.key == pygame.K_SPACE:
                    self.turn += 1
                    self.game.machine.end_player_turn()

                if event.key == pygame.K_c:
                    self.game.machine.open_character_menu()

                if event.key == pygame.K_i:
                    self.game.machine.open_inventory_menu()

        # All of the actions you can do after selecting an attack
        if self.game.machine.state == 'player_turn_attack':
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.selected_mob = self.targets[(self.targets.index(self.selected_mob) + 1) % len(self.targets)]

                if event.key == pygame.K_ESCAPE:
                    self.game.machine.cancel_attack()

                if event.key == pygame.K_RETURN:
                    skills.melee_attack(self, self.selected_mob)
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