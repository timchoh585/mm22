import src.game.gameConstants as gameConstants


class Character(object):

    def __init__(self, charId, name="AI", classId="warrior"):
        """ Init a character class based on class key defined in game consts

        :param charId: (int) id of the character, based off of team
        :param name: (string) name of the character
        :param classId: (int) class key
        """

        #Game related attributes
        self.posX = 0.0
        self.posY = 0.0
        self.id = charId
        self.name = name
        self.classId = classId

        #Crowd controls
        self.stunned = False
        self.silenced = False
        self.rooted = False

        # A json object if the character is casting an ability
        # {"abilityId": (int), "currentCastTime": (int)}
        self.casting = None

        classJson = gameConstants.classesJson[classId]

        self.attributes = Attributes( classJson['Health'],
                            classJson['Damage'],
                            classJson['AttackRange'],
                            classJson['AttackSpeed'],
                            classJson['Armor'],
                            classJson['MovementSpeed'],
                            self.stunned,
                            self.rooted,
                            self.silenced)

        # A Json that contains abilities by id and their cooldown by id
        self.abilities = {}
        for ability in classJson['Abilities']:
            self.abilities[ability] = 0.0

        self.buffs = []
        self.debuffs = []

    def update(self):
        if self.casting:
            self.casting["currentCastTime"] -= 1
            if self.casting["currentCastTime"] == 0:
                self.cast_ability(self.casting["abilityId"])

        # Update ability cooldowns
        for ability in self.abilities:
            if self.abilities[ability] > 0:
                self.abilities[ability] -= 0

        # Update buffs
        for buff in self.buffs:
            if buff['Time'] == 0:
                self.apply_stat_change(buff['StatChange']['Attribute'], -buff['ActualChange'])
                self.buffs.remove(buff)
            else:
                buff['Time'] -= 0

        # Update debuffs
        for debuff in self.debuffs:
            if debuff['Time'] == 0:
                self.apply_stat_change(debuff['StatChange']['Attribute'], -debuff['ActualChange'])
                self.debuffs.remove(debuff)
            else:
                debuff['Time'] -= 0

    def can_use_ability(self, ability_id):
        """ Checks if a character can use an ability (must have that ability)
        :param ability_id: id of the ability to check
        :return: True if yes, False if no
        """
        # Does this character actually have the ability?
        if ability_id not in self.abilities:
            return False
        return self.abilities[ability_id] == 0
        
        # Is the character stunned?
        if (self.stunned):
            return False
        return self.abilities[ability_id] == 0
        
        # Is the character silenced?
        if (self.silenced):
            return False
        return self.abilities[ability_id] == 0

    def use_ability(self, ability_id, character):
        # Does this ability even exist?
        if ability_id < len(gameConstants.abilitiesList):
            return False
        # Is the ability on cooldown?
        if not self.can_use_ability(self, ability_id):
            return False

        if gameConstants.abilitiesList[ability_id]['Casttime'] > 0:
            self.casting = {"abilityId": ability_id, "currentCastTime": 0}
        else:
            self.cast_ability(ability_id, character)

    def cast_ability(self, ability_id, character):
        self.casting = None

        # Apply Cooldown
        self.abilities[ability_id] = gameConstants.abilitiesList[ability_id]["Cooldown"]

        # Get ability json
        ability = gameConstants.abilitiesList[ability_id]

        # Iterate through stat changes
        for stat_change in ability['StatChanges']:
            if stat_change['Target'] == 0:
                self.apply_stat_change(stat_change)
            if stat_change['Target'] == 1:
                character.apply_stat_change(stat_change)

    def apply_stat_change(self, stat_change):

        # Will hold the value the change for reverting after the buff/debuff fades (if it is one)
        actual_change = 0

        # Apply stat change
        if stat_change['Health']:
            actual_change = self.attributes.change_attribute(self, stat_change['Attribute'], stat_change['change'])
        else:
            actual_change = self.attributes.change_attribute(self, stat_change['Attribute'], stat_change['change'])

        # If there a time on the buff/debuff, make note
        buff_json = {"StatChange": stat_change, "Time": stat_change['Time'], "ActualChange": actual_change}
        if actual_change < 0:
            self.debuffs.append(buff_json)
        else:
            self.buffs.append(buff_json)

    def toJson(self):
        """ Returns information about character as a json
        """

        #TODO finish

        json = {}
        json['charId'] = self.id
        json['x'] = self.posX
        json['y'] = self.posY
        json['name'] = self.name
        json['class'] = self.classId
        json['attributes'] = self.attributes.toJson()

        return json


class Attributes(object):

    def __init__(self, health, damage, abilityPower, attackRange, attackSpeed, armor, movementSpeed):
        """ Init attributes for a character
        :param health: (float) health
        :param damage: (float) damage per tick
        :param attackRange: (int) attackRange of auto attack
        :param attackSpeed: (int) attackSpeed of auto attacks
        :param armor: (float) damage removed from attacks
        :param movementSpeed: (int) movement per tick
        :param stunned: (bool) stun status
        :param rooted: (bool) root status
        :param silenced: (bool) silence status
        """

        self.maxHealth = health
        self.health = health
        self.damage = damage
        self.attackRange = attackRange
        self.attackSpeed = attackSpeed
        self.armor = armor
        self.movementSpeed = movementSpeed
        self.stunned = stunned
        self.rooted = rooted
        self.silenced = silenced

    def change_attribute(self, attribute_name, change):
        if attribute_name == 'Health':
            return self.change_health(change)
        if attribute_name == 'Damage':
            return self.change_damage(change)
        if attribute_name == 'AttackSpeed':
            return self.change_attack_speed(change)
        if attribute_name == 'AttackRange':
            return self.change_attack_range(change)
        if attribute_name == 'Armor':
            return self.change_armor(change)
        if attribute_name == 'MovementSpeed':
            return self.change_movement_speed(change)
        if attribute_name == 'Stunned':
            return self.change_stunned(change)
        if attribute_name == 'Rooted':
            return self.change_rooted(change)
        if attribute_name == 'Silenced':
            return self.change_silenced(change)

    def change_health(self, change):
        if change < 0:
            self.health = max(0, self.health + max(0, change + self.armor))
        if change > 0:
            self.health = min(self.maxHealth, self.health + change)

    def change_damage(self, change):
        self.damage = max(0, self.damage + change)

    def change_attack_speed(self, change):
        self.attackSpeed = max(1, self.attackSpeed + change)

    def change_attack_range(self, change):
        self.attackRange = max(0, self.attackRange + change)

    def change_armor(self, change):
        self.armor = max(0, self.armor + change)

    def change_movement_speed(self, change):
        new_change = change_in_Value()
        self.movementSpeed = max(0, self.movementSpeed + change)

    def change_stunned(self, change):
        if (change):
            self.stunned = (self.stunned || change)
        self.stunned = (self.stunned && change)

    def change_rooted(self, change):
        if (change):
            self.rooted = (self.rooted || change)
        self.rooted = (self.rooted && change)

    def change_silenced(self, change):
        if (change):
            self.silenced = (self.silenced || change)
        self.silenced = (self.silenced && change)

    def change_in_value(self, value, change, max=None, min=None):
        """ Given a initial value and change to that value along with a min or max, it will return the required change up to min/max if needed
        :param value: (int) Original value
        :param change: (int) change to value
        :param max: (int)
        :param min: (int)
        :return:
        """
        if not value and not change:
            return 0

        new_value = value + change

        if min:
            return change + (min - new_value)
        if max:
            return change + (max - new_value)
        return change

    def toJson(self):
        """ Return json of information containing all attribute information
        """

        json = {}
        json['MaxHealth'] = self.maxHealth
        json['Health'] = self.health
        json['Damage'] = self.damage
        json['AttackSpeed'] = self.attackSpeed
        json['AttackRange'] = self.attackRange
        json['Armor'] = self.armor
        json['MovementSpeed'] = self.movementSpeed

        return json