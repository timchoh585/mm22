import sys
sys.path.append("../..")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *

class Actor(object):
    gameMap = GameMap()
    character = {}
    actions = []
    enemies = []

    def __init__(self, character, enemies):
        self.character = character
        self.enemies = enemies

    # set movement of character
    def movement(self, x, y):
        json = None
        return json

    # set the enemy flag of what its evading
    #  -1 if not evading
    def evades(self):
        move_flag = -1
        return move_flag

    # set enemy to move towards
    # also checks for skill attack
    # -1 if not evading
    def advance(self):
        move_flag = -1
        return move_flag

    # -1 is base attack
    # everything else is index of array of moves
    def use_skill(self):
        attack_skill = -1
        return attack_skill

# appends attack json commands to action array
def attack_json(character, target):
    return {
        "Action": "Attack",
        "CharacterId": character.id,
        "TargetId": target.id
    }

# appends move json commands to specified location to action array
def move_position_json(character, location):
    return {
        "Action": "Move",
        "CharacterId": character.id,
        "Location": location
    }

def move_target_json(character, target):
    return {
        "Action": "Move",
        "CharacterId": character.id,
        "TargetId": target.id
    }

# appends ability json commands to action array
def ability_json(character, target, abilityId):
    if abilityId in character.abilities.items() and character.abilities.item()[abilityId] == 0:
        # If I can, then cast it
        ability = game_consts.abilitiesList[int(abilityId)]
        # Get ability
        return {
            "Action": "Cast",
            "CharacterId": character.id,
            # Am I buffing or debuffing? If buffing, target myself
            "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
            "AbilityId": int(abilityId)
        }
    return None