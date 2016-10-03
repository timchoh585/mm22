# Expected value calculations
import math
import sys

def calculate_distance(character, enemy):
    return math.sqrt(pow(character.position[0] - enemy.position[0], 2) + pow(character.position[1] - enemy.position[1], 2))


class ExpectedValue(object):
    evalue_none = 0
    evalue_dps = 0

    player_ehealth = 0
    enemy_ehealth = 0
    player_ehealth_dps = sys.maxint
    enemy_ehealth_dps = sys.maxint

    def __init__(self, characters, enemies):
        self.characters = characters
        self.enemies = enemies

    # calculates effective health of the time, flag = 0 for your characters 1 for enemy characters
    def calculate_ehealths(self, flag):
        if flag == 0:
            for character in self.characters:
                self.player_ehealth = self.player_ehealth + character.attributes.health * self.calculate_modifiers(character)

            for enemy in self.enemies:
                self.enemy_ehealth = self.enemy_ehealth + enemy.attributes.health * self.calculate_modifiers(enemy)
        else:
            for character in self.characters:
                if not character.is_dead():
                    self.player_ehealth_dps = min(self.player_ehealth_dps, (character.attributes.health + self.calculate_dps(character.classId)
                        + self.calculate_avg_distance(character, 0)))
            if self.player_ehealth_dps == 0:
                self.player_ehealth_dps = -sys.maxint - 1

            for enemy in self.enemies:
                if not enemy.is_dead():
                    self.enemy_ehealth_dps = min(self.enemy_ehealth_dps, (enemy.attributes.health
                        + self.calculate_dps(enemy.classId)))
            if self.enemy_ehealth_dps == 0:
                self.enemy_ehealth_dps = -sys.maxint - 1

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
            modifier = modifier * -1 #(character.attributes.maxHealth / character.attributes.health * -1)
        # dps flag
        return modifier

    # returns expected value of state
    def calculate_evalue(self):

        self.calculate_ehealths(0)
        self.calculate_ehealths(1)

        evalue = self.player_ehealth
        self.evalue_dps = self.player_ehealth_dps
        return (self.evalue_none, self.evalue_dps)

    def calculate_avg_distance(self, character, flag):
        avg_distance = 0
        if flag:
            for enemy in self.characters:
                avg_distance = avg_distance + calculate_distance(character, enemy)
            avg_distance = avg_distance / len(self.characters)
        else:
            for enemy in self.enemies:
                avg_distance = avg_distance + calculate_distance(character, enemy)
            avg_distance = avg_distance / len(self.enemies)
        return avg_distance
