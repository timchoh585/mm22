import sys
sys.path.append("../")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *


class Action(object):
    m = -1
    target = None

    # enum m = -1 -> no action, 0-3 -> movement, 4 -> regular attack, 5-8 maps to index of skill in abilities array
    # target is tuple ( [boolean] 0 -> our team; 1 -> opponent, index in team array)
    def __init__(self, action_type, target=None):
        self.m = action_type
        self.target = target

    def is_movement(self):
        if self.m >= 0 and self.m < 4:
            return True
        else:
            return False

    def is_attack(self):
        return self.m == 4

    def is_ability(self):
        if self.m > 4:
            return True
        else:
            return False

            ### room for more helper functions


def generate_action(character_index, current_state, gameMap, team_1):
    ret = []  # append
    if team_1:
        main = current_state.team[character_index]
        enemy = current_state.enemy_team
    else:
        main = current_state.enemy_team[character_index]
        enemy = current_state.team

    position = [current_state[character_index].position[0], current_state[character_index].position[1]]
    target = "";

    # checks for possible positions
    if main.can_move():
        if gameMap.is_inbounds((position[0] + 1, position[1])):
            ret.append(Action(2))
        if gameMap.is_inbounds((position[0] - 1, position[1])):
            ret.append(Action(3))
        if gameMap.is_inbounds((position[0], position[1] - 1)):
            ret.append(Action(0))
        if gameMap.is_inbounds((position[0], position[1] + 1)):
            ret.append(Action(1))

    for i in enemy:
        if main.in_range_of(main, enemy[i], gameMap):
            ret.append(Action((4, (team_1, i))))
        for abilityId, cooldown in main.abilities.items():
            if main.can_use_ability(main, abilityId):
                if main.in_ability_range_of(main, enemy[i], gameMap, abilityId):
                    ret.append(Action(abilityId + 5), (team_1, i))

    return ret