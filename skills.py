'''
Current Idea For Implementation:
Make skill components as functions (so melee attack, ranged attack, spells, etc)
Make advanced skills by calling multiple functions
'''
from random import randint

# Skills Dictionary
SKILL = {
    'Melee Attack': {
        'Name': 'Melee Attack',
        'Image': 'bare_hands.png',
        'Function': 'melee_attack'
    },
    'Magic Attack': {
        'Name': 'Magic Attack',
        'Image': 'magic_icon.png',
        'Function': 'magic_attack'
    },
}


def melee_attack(self, target):
    if randint(0, 99) <= target.dodge_percent:
        damage = 0
        print("Dodged!")
    else:
        damage = self.melee_attack_power - target.melee_defense
        if damage <= 0:
            damage = 1
    target.current_hit_points -= damage

    if target.current_hit_points <= 0:
        target.kill()
        self.experience += target.experience_worth