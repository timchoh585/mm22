#from __future__ import print_function
import sys
sys.path.append("../")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *
from expectedvalue import ExpectedValue


class DecisionTree(object):
    initial_state = None
    gameMap = GameMap()

    def __init__(self, team, enemy_team):
        self.initial_state = State(team, enemy_team)
        self.initial_state.us = True
        self.initial_state.expected_value = ExpectedValue(team, enemy_team)
        self.initial_state.expected_value.calculate_evalue()

    def generate_to_level(self, prev_state, currentlevel, targetlevel, team_1):
        if (currentlevel == targetlevel):
            return
        else:
            prev_state.children = []
            team_actions = []
            for i, character in enumerate(prev_state.team):
                actions = generate_actions(i, prev_state, self.gameMap, team_1)
                team_actions.append(actions)

            for action_1 in team_actions[0]:
                for action_2 in team_actions[1]:
                    for action_3 in team_actions[2]:
                        next_state = copy_chars_off_actions([action_1, action_2, action_3], prev_state, team_1)
                        next_state = eval_next_state(0, action_1, next_state, self.gameMap, team_1)
                        next_state = eval_next_state(1, action_2, next_state, self.gameMap, team_1)
                        next_state = eval_next_state(2, action_3, next_state, self.gameMap, team_1)

                        next_state.expected_value = ExpectedValue(next_state.team, next_state.enemy_team)
                        next_state.expected_value.calculate_evalue()

                        next_state.us = team_1
                        prev_state.children.append(next_state)
                        self.generate_to_level(next_state, currentlevel + 1, targetlevel, not team_1)
            '''
            for action_1 in team_actions[0]:
                next_state = copy_chars_off_actions([action_1], prev_state, team_1)
                next_state = eval_next_state(0, action_1, next_state, self.gameMap, team_1)
                #next_state = eval_next_state(1, action_2, next_state, self.gameMap, team_1)
                #next_state = eval_next_state(2, action_3, next_state, self.gameMap, team_1)

                next_state.expected_value = ExpectedValue(next_state.team, next_state.enemy_team)
                next_state.expected_value.calculate_evalue()

                next_state.us = team_1
                prev_state.children.append(next_state)
                self.generate_to_level(next_state, currentlevel + 1, targetlevel, not team_1)
            '''


def alphabeta(tree, alpha, alpha_node, beta, beta_node):
    best_value = 0
    best_node = None
    if len(tree.children) == 0:
        best_node = tree
    elif tree.us:
        best_value = alpha
        best_node = alpha_node

        for i in tree.children:
            grandchild = alphabeta(i, best_value, best_node, beta, beta_node)
            if calc_expected_value(grandchild) >= best_value:
                best_value = calc_expected_value(grandchild)
                best_node = grandchild
            if beta < best_value:
                break
    else:
        best_value = beta
        best_node = beta_node

        for i in tree.children:
            grandchild = alphabeta(i, alpha, alpha_node, best_value, best_node)
            if calc_expected_value(grandchild) <= best_value:
                best_value = calc_expected_value(grandchild)
                best_node = grandchild
            if best_value < alpha:
                break
    return best_node

def calc_expected_value(node):
    return (node.expected_value.player_ehealth_dps - node.expected_value.enemy_ehealth_dps)

def initialize_ab(tree):
    best_node = alphabeta(tree, -999999, None, 999999, None)
    return best_node


def indentation(level):
    result = ""
    while(level > 0):
        result = result + '\t'
        level = level - 1
    return result


def print_decision_tree(node, level, file):
    if len(node.children) == 0:
        print >>file, indentation(level) + 'No move moves...'
        return

    #print tree.expected_value.evalue_dps
    print >>file, indentation(level) + "Number of possible moves: " + str(len(node.children))
    for child in node.children:
        for i, action in enumerate(child.actions_acted):
            actor = None
            if child.us:
                actor = child.team[i]
            else:
                actor = child.enemy_team[i]
            result = ""
            if action.is_movement():
                if action.m == 0:
                    result = "moves north to location: (" + str(actor.position[0]) + ", " + str(actor.position[1]) + ")"
                elif action.m == 1:
                    result =  "moves south to location: (" + str(actor.position[0]) + ", " + str(actor.position[1]) + ")"
                elif action.m == 2:
                    result = "moves east to location: (" + str(actor.position[0]) + ", " + str(actor.position[1]) + ")"
                else:
                    result = "moves west to location: (" + str(actor.position[0]) + ", " + str(actor.position[1]) + ")"
            elif action.is_attack():
                if action.target[0]:
                    result = "attacks " + child.team[action.target[1]].classId
                else:
                    result = "attacks " + child.enemy_team[action.target[1]].classId
            print >>file, indentation(level) + actor.classId + " " + result + " with expected_value: " + str(calc_expected_value(child))
        print >>file, indentation(level) + 'Next Move: '
        print_decision_tree(child, level + 1, file)


class State(object):
    actions_acted = []
    team = []
    enemy_team = []
    children = []
    expected_value = None
    us = None

    def __init__(self, team, enemy_team):
        self.team = copy.copy(team)
        self.enemy_team = copy.copy(enemy_team)

    def deserialize(self):
        ret = []
        for i, action in enumerate(self.actions_acted):
            character = None
            if(self.us):
                character = self.team[i]
            else:
                character = self.enemy_team[i]
            if(not action.is_movement()):
                if action.target[0]:
                    target = self.team[action.target[1]]
                else:
                    target = self.enemy_team[action.target[1]]
            if(action.is_movement()):
                ret.append({
                    "Action": "Move",
                    "CharacterId": character.id,
                    "Location": character.position
                })
            elif(action.is_attack):
                ret.append({
                    "Action": "Attack",
                    "CharacterId": character.id,
                    "TargetId": target.id,
                })
            else:
                ret.append({
                    "Action": "Cast",
                    "CharacterId": character.id,
                    "TargetId": target.id,
                    "AbilityId": (action.m - 5)
                })
        return ret

def copy_chars_off_actions(actions, state, team_1):
    ret = copy.copy(State(state.team, state.enemy_team))
    ret.children = []
    ret.actions_acted = []
    for i, action in enumerate(actions):
        if action.is_movement():
            if team_1:
                ret.team[i] = copy.copy(ret.team[i])
            else:
                ret.enemy_team[i] = copy.copy(ret.enemy_team[i])
        else:
            if action.target[0]:
                ret.team[action.target[1]] = copy.copy(ret.team[action.target[1]])
            else:
                ret.enemy_team[action.target[1]] = copy.copy(ret.enemy_team[action.target[1]])
    return ret

def eval_next_state(character_index, action, current_state, gameMap, team_1=True):
    actor = None
    ret = current_state
    ret.actions_acted.append(copy.copy(action))
    if team_1:
        actor = ret.team[character_index]
    else:
        actor = ret.enemy_team[character_index]
    if action.is_movement():
        new_position = [actor.position[0], actor.position[1]]
        if action.m == 0:
            new_position[1] = new_position[1] - 1
        elif action.m == 1:
            new_position[1] = new_position[1] + 1
        elif action.m == 2:
            new_position[0] = new_position[0] + 1
        else:
            new_position[0] = new_position[0] - 1
        actor.position = tuple(new_position)
    else:
        if action.target[0]:
            target = ret.team[action.target[1]]
        else:
            target = ret.enemy_team[action.target[1]]
        actor.attributes = copy.copy(actor.attributes)
        target.attributes = copy.copy(target.attributes)
        if action.is_attack():
            target.add_stat_change({
                "Target": 1,
                "Attribute": "Health",
                "Change": -1 * actor.attributes.get_attribute("Damage"),
                "Time": 0
            })
            target.apply_pending_stat_changes()
        else:
            actor.use_ability(action.m - 5, target, gameMap)
            target.apply_pending_stat_changes()
    return ret


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


def generate_actions(character_index, current_state, gameMap, team_1):
    ret = []  # append
    if team_1:
        main = current_state.team[character_index]
        enemies = current_state.enemy_team
    else:
        main = current_state.enemy_team[character_index]
        enemies = current_state.team

    position = [main.position[0], main.position[1]]
    target = "";

    # checks for possible positions
    if not main.attributes.get_attribute("Stunned") and not main.attributes.get_attribute("Rooted"):
        if gameMap.is_inbounds((position[0] + 1, position[1])):
            ret.append(Action(2))
        if gameMap.is_inbounds((position[0] - 1, position[1])):
            ret.append(Action(3))
        if gameMap.is_inbounds((position[0], position[1] - 1)):
            ret.append(Action(0))
        if gameMap.is_inbounds((position[0], position[1] + 1)):
            ret.append(Action(1))

    for i, enemy in enumerate(enemies):
        if main.in_range_of(enemy, gameMap) and not enemy.is_dead():
            ret.append(Action(4, (not team_1, i)))
        for abilityId, cooldown in main.abilities.items():
            if main.can_use_ability(abilityId):
                if main.in_ability_range_of(enemy, gameMap, abilityId):
                    ret.append(Action(abilityId + 5), (team_1, i))

    return ret