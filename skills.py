class Skill:
    def __init__(self, name):
        self.name = name


class activeSkill(Skill):
    def __init__(self, name):
        Skill.__init__(self, name)
        self.skillType = 'Active'

    def onUse(self):
        pass


class passiveSkill(Skill):
    def __init__(self, name):
        Skill.__init__(self, name)
        self.skillType = 'Passive'
        self.state = False

    def activate(self):
        if self.state == False:
            self.state = True
        if self.state == True:
            self.state = False


# Testing Skills Down Here
meleeAttack = activeSkill('Melee Attack', player.melee_weapon['Range'])
