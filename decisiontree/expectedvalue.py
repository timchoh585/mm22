# Expected value calculations
class ExpectedValue(object):
    evalue_none = 0
    evalue_dps = 0

    player_ehealth = 0
    enemy_ehealth = 0
    player_ehealth_dps = 0
    enemy_ehealth_dps = 0

    def __init__(self, characters, enemies):
        self.characters = characters
        self.enemies = enemies

    # calculates effective health of the time, flag = 0 for your characters 1 for enemy characters
    def calculate_ehealths(self, flag):
        if flag == 0:
            for character in self.characters:
                self.player_ehealth = self.player_ehealth + character.attributes.health * self.calculate_modifiers(character)

            for enemy in self.enemies:
                self.enemy_ehealth = self.enemy_ehealth + enemy.attributes.health * self.calculate_modifiers(character)
        else:
            for character in self.characters:
                self.player_ehealth_dps = self.player_ehealth + character.attributes.health * self.calculate_modifiers(
                    character) + self.calculate_dps(character.classId)

            for enemy in self.enemies:
                self.enemy_ehealth_dps = self.enemy_ehealth + enemy.attributes.health * self.calculate_modifiers(
                    character) + self.calculate_dps(character.classId)

    # returns dps from dps array
    def calculate_dps(self, character):
        characters = ['Archer', 'Assassin', 'Druid', 'Enchanter', 'Paladin', 'Sorcerer', 'Warrior', 'Wizard']
        dps = [100, 125, 60, 45, 50, 80, 96.25, 75, 100]
        return dps[characters.index(character)]

    # calculate modifiers to the expected value
    def calculate_modifiers(self, character):
        modifier = 1
        # if character is dead, make the modifier the negative of the character's effective health
        if character.is_dead() == True:
            modifier = modifier * (character.attributes.maxHealth / character.attributes.health * -1)
        # dps flag
        return modifier

    # returns expected value of state
    def calculate_evalue(self):

        self.calculate_ehealths(0)
        self.calculate_ehealths(1)

        evalue = self.player_ehealth
        self.evalue_dps = self.player_ehealth_dps
        return (self.evalue_none, self.evalue_dps)

