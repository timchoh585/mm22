#!/usr/bin/python2
import socket
import json
import os
import random
import sys
from socket import error as SocketError
import errno
sys.path.append("../..")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *

# Game map that you can use to query 
gameMap = GameMap()

class Actor(object):
    actions = []
    def __init__(self, character, enemy1, enemy2, enemy3):
        self.character = character
        self.enemy1 = enemy1         
        self.enemy2 = enemy2
        self.enemy3 = enemy3

    # set movement of character
    def movement(self, x, y):

        return json

    # set the enemy flag of what its evading
    #  0 if not evading
    def evades(self):
        return move_flag

    # set enemy to move towards
    # also checks for skill attack
    # 0 if not evading
    def advance(self):

        return move_flag

    # 0 is base attack
    # everything else is index of array of moves
    def use_skill(self):
        return attack_skill

# appends attack json commands to action array
def attack_json(actions, character, target):
    return actions.append({
                    "Action": "Attack",
                    "CharacterId": character.id,
                    "TargetId": target.id,
                })

# appends move json commands to specified location to action array
def move_json(actions, character, location):
    return actions.append({
                    "Action": "Move",
                    "CharacterId": character.id,
                    "TargetId": location,
                })

# appends ability json commands to action array
def ability_json(actions, character, target, abilityId, cooldown):
    if abilityId in character.abilities.items():
       #If I can, then cast it
       ability = game_consts.abilitiesList[int(abilityId)]
       # Get ability
        return actions.append({
                                            "Action": "Cast",
                                            "CharacterId": character.id,
                                            # Am I buffing or debuffing? If buffing, target myself
                                            "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
                                            "AbilityId": int(abilityId)
                                        })
# --------------------------- SET THIS IS UP -------------------------
teamName = "Test"
# ---------------------------------------------------------------------
character = "Druid"
# Set initial connection data
def initialResponse():
# ------------------------- CHANGE THESE VALUES -----------------------
    
    return {'TeamName': teamName,
            'Characters': [
                {"CharacterName": character,
                 "ClassId": character},
                {"CharacterName": character,
                 "ClassId": character},
                {"CharacterName": character,
                 "ClassId": character},
            ]}
# ---------------------------------------------------------------------

# Determine actions to take on a given turn, given the server response
def processTurn(serverResponse):
# --------------------------- CHANGE THIS SECTION -------------------------
    # Setup helper variables
    actions = []
    myteam = []
    enemyteam = []
    # Find each team and serialize the objects
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
# ------------------ You shouldn't change above but you can ---------------

    # Choose a target
    target = None
    for character in enemyteam:
        if not character.is_dead():
            target = character
            break

    # If we found a target
    if target:
        for character in myteam:
            # If I am in range, either move towards target
            if character.in_range_of(target, gameMap):
                # Am I already trying to cast something?
                if character.casting is None:
                    cast = False
                    # for abilityId, cooldown in character.abilities.items():
                    #     # Do I have an ability not on cooldown
                    #     if cooldown == 0:
                    #         # If I can, then cast it
                    #         ability = game_consts.abilitiesList[int(abilityId)]
                    #         # Get ability
                    #         actions.append({
                    #             "Action": "Cast",
                    #             "CharacterId": character.id,
                    #             # Am I buffing or debuffing? If buffing, target myself
                    #             "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
                    #             "AbilityId": int(abilityId)
                    #         })
                    #         cast = True
                    #         break
                    # Was I able to cast something? Either wise attack
                    if not cast:
                        actions.append({
                            "Action": "Attack",
                            "CharacterId": character.id,
                            "TargetId": target.id,
                        })
            else: # Not in range, move towards
                actions.append({
                    "Action": "Move",
                    "CharacterId": character.id,
                    "TargetId": target.id,
                })

    # Send actions to the server
    return {
        'TeamName': teamName,
        'Actions': actions
    }
# ---------------------------------------------------------------------

# Main method
# @competitors DO NOT MODIFY
if __name__ == "__main__":
    # Config
    conn = ('localhost', 1337)
    if len(sys.argv) > 2:
        conn = (sys.argv[1], int(sys.argv[2]))

    # Handshake
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(conn)

    # Initial connection
    s.sendall(json.dumps(initialResponse()) + '\n')

    # Initialize test client
    game_running = True
    members = None

    # Run game
    try:
        data = s.recv(1024)
        while len(data) > 0 and game_running:
            value = None
            if "\n" in data:
                data = data.split('\n')
                if len(data) > 1 and data[1] != "":
                    data = data[1]
                    data += s.recv(1024)
                else:
                    value = json.loads(data[0])

                    # Check game status
                    if 'winner' in value:
                        game_running = False

                    # Send next turn (if appropriate)
                    else:
                        msg = processTurn(value) if "PlayerInfo" in value else initialResponse()
                        s.sendall(json.dumps(msg) + '\n')
                        data = s.recv(1024)
            else:
                data += s.recv(1024)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    s.close()
