import sys
sys.path.append("../")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *
from decisiontree import *

serverResponse = {
    'TurnNumber': 181, 
    'TurnResult': [], 
    'PlayerInfo': {
        'TeamId': 2, 
        'Characters': [
            {
                'ClassId': 'Paladin', 
                'CharacterName': 'Paladin'
            }, {
                'ClassId': 'Archer',
                'CharacterName': 'Archer'
            }, {
                'ClassId': 'Warrior',
                'CharacterName': 'Warrior'
            }],
        'TeamName': 'Test',
        'Id': 1
    },
    'Teams': [{
        'Id': 1,
        'Characters': [
            {
                'ClassId': 'Enchanter',
                'Debuffs': [],
                'Abilities': {
                    '0': 0,
                    '5': 0,
                    '7': 0,
                    '6': 0
                }, 'Casting': None,
                'Name': 'Enchanter',
                'Buffs': [], 'Position': [4, 2], 'Attributes': {'Rooted': 0, 'Stunned': 0, 'Silenced': 0, 'Armor': 25, 'MaxHealth': 1000, 'Damage': 45, 'AttackRange': 2, 'SpellPower': 0, 'Health': 1000, 'MovementSpeed': 1}, 'Id': 1}, {'ClassId': 'Enchanter', 'Debuffs': [], 'Abilities': {'0': 0, '5': 0, '7': 0, '6': 0}, 'Casting': None, 'Name': 'Enchanter', 'Buffs': [], 'Position': [4, 2], 'Attributes': {'Rooted': 0, 'Stunned': 0, 'Silenced': 0, 'Armor': 25, 'MaxHealth': 1000, 'Damage': 45, 'AttackRange': 2, 'SpellPower': 0, 'Health': 1000, 'MovementSpeed': 1}, 'Id': 2}, {'ClassId': 'Enchanter', 'Debuffs': [], 'Abilities': {'0': 0, '5': 0, '7': 0, '6': 0}, 'Casting': None, 'Name': 'Enchanter', 'Buffs': [], 'Position': [4, 2], 'Attributes': {'Rooted': 0, 'Stunned': 0, 'Silenced': 0, 'Armor': 25, 'MaxHealth': 1000, 'Damage': 45, 'AttackRange': 2, 'SpellPower': 0, 'Health': 1000, 'MovementSpeed': 1}, 'Id': 3}], 'Teamname': 'Test'}, {'Id': 2, 'Characters': [{'ClassId': 'Paladin', 'Debuffs': [], 'Abilities': {'0': 0, '3': 0, '14': 0}, 'Casting': None, 'Name': 'Paladin', 'Buffs': [], 'Position': [4, 4], 'Attributes': {'Rooted': 0, 'Stunned': 0, 'Silenced': 0, 'Armor': 45, 'MaxHealth': 1100, 'Damage': 50, 'AttackRange': 0, 'SpellPower': 0, 'Health': 1100, 'MovementSpeed': 1}, 'Id': 4}, {'ClassId': 'Archer', 'Debuffs': [], 'Abilities': {'0': 0, '12': 0, '2': 0}, 'Casting': None, 'Name': 'Archer', 'Buffs': [], 'Position': [4, 4], 'Attributes': {'Rooted': 0, 'Stunned': 0, 'Silenced': 0, 'Armor': 25, 'MaxHealth': 1000, 'Damage': 100, 'AttackRange': 2, 'SpellPower': 0, 'Health': 1000, 'MovementSpeed': 1}, 'Id': 5}, {'ClassId': 'Warrior', 'Debuffs': [], 'Abilities': {'1': 0, '0': 0, '15': 0}, 'Casting': None, 'Name': 'Warrior', 'Buffs': [], 'Position': [4, 4], 'Attributes': {'Rooted': 0, 'Stunned': 0, 'Silenced': 0, 'Armor': 50, 'MaxHealth': 1200, 'Damage': 75, 'AttackRange': 0, 'SpellPower': 0, 'Health': 1200, 'MovementSpeed': 1}, 'Id': 6}], 'Teamname': 'Test'}]}


myteam = []
enemyteam = []

for team in serverResponse["Teams"]:
    if team["Id"] == serverResponse["PlayerInfo"]["TeamId"]:
        for characterJson in team["Characters"]:
            character = Character()
            character.serialize(characterJson)
            myteam.append(character)
    else:
        for characterJson in team["Characters"]:
            character = Character()
            character.serialize(characterJson)
            enemyteam.append(character)

decision_tree = DecisionTree(enemyteam, myteam)
decision_tree.generate_to_level(decision_tree.initial_state, 0, 1, True)
print_decision_tree(decision_tree.initial_state, 0, sys.stdout)
best_move = initialize_ab(decision_tree.initial_state)
actions = best_move.deserialize()