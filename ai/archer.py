from actor import *


class ArcherActor(Actor):
    def movement(self):
        json = None
        move_flag = self.evades()
        print move_flag
        if move_flag != -1:
            position = self.move_from_target(self.enemies[move_flag])
            json = move_position_json(self.character, position)
            return json
        move_flag = self.advance()
        if move_flag != -1:
            json = move_target_json(self.character, self.enemies[move_flag])
            return json
        move_flag = self.use_skill()
        target = self.choose_target()
        if move_flag != -1:
            ability_json(self.character, target, 12)
        else:
            json = attack_json(self.character, target)
            return json

    # set the enemy flag of what its evading
    #  -1 if not evading
    def evades(self):
        move_flag = -1
        for i, enemy in enumerate(self.enemies):
            if enemy.in_range_of(self.character, self.gameMap):
                move_flag = i
        return move_flag

    # set enemy to move towards
    # also checks for skill attack
    # -1 if not evading
    def advance(self):
        move_flag = -1
        for i, enemy in enumerate(self.enemies):
            if move_flag == -1 and not self.character.in_range_of(enemy, self.gameMap):
                move_flag = i
        return move_flag

    # -1 is base attack
    # everything else is index of array of moves
    def use_skill(self):
        attack_skill = -1
        return attack_skill

    def strafe_row(self, new_position):
        if self.gameMap.is_inbounds((new_position[0], new_position[1] + 1)):
            new_position[1] += 1
            return new_position
        else:
            new_position[1] -= 1
            return new_position

    def strafe_col(self, new_position):
        if self.gameMap.is_inbounds((new_position[0] + 1, new_position[1])):
            new_position[0] += 1
            return new_position
        else:
            new_position[0] -= 1
            return new_position

    def move_from_target(self, target):
        new_position = [self.character.position[0], self.character.position[1]]
        if self.gameMap.is_same_col(self.character.position, target.position):
            if self.character.position[0] > target.position[0]:
                while target.in_range_of(self.character, self.gameMap) and self.gameMap.is_inbounds(((new_position[0] + 1), new_position[1])):
                    new_position[0] += 1
                if target.in_range_of(self.character, self.gameMap):
                    new_position = self.strafe_row(new_position)
            else:
                while target.in_range_of(self.character, self.gameMap) and self.gameMap.is_inbounds(((new_position[0] - 1), new_position[1])):
                    new_position[0] -= 1
                if target.in_range_of(self.character, self.gameMap):
                    new_position = self.strafe_row(new_position)
        else:
            if self.character.position[1] > target.position[1]:
                while target.in_range_of(self.character, self.gameMap) and self.gameMap.is_inbounds((new_position[0], (new_position[1] + 1))):
                    new_position[1] += 1
                if target.in_range_of(self.character, self.gameMap):
                    new_position = self.strafe_col(new_position)
            else:
                while target.in_range_of(self.character, self.gameMap) and self.gameMap.is_inbounds((new_position[0], (new_position[1] - 1))):
                    new_position[1] -= 1
                if target.in_range_of(self.character, self.gameMap):
                    new_position = self.strafe_col(new_position)
        return tuple(new_position)

    def choose_target(self):
        target = None
        sorted(self.enemies, key=lambda enemy: enemy.attributes.get_attribute("Health"))
        for enemy in self.enemies:
            if not enemy.is_dead() and self.character.in_range_of(enemy, self.gameMap):
                target = enemy
        return target