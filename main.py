import pygame
import sqlite3
import datetime


START_TIME = datetime.datetime.now()
DATE = datetime.date.today()


class Screen:
    pass


class Menu(Screen):
    pass


class Scoreboard(Screen):
    def __init__(self):
        self.score = 0

    def add_score(self, score):
        self.score += score

    def add_to_db(self):
        duration = datetime.datetime.now() - START_TIME

        def parse(time):
            seconds = int(time.total_seconds())
            hours = seconds // 3600
            seconds -= hours * 3600
            minutes = seconds // 60
            seconds -= minutes * 60
            return [str(i) for i in [hours, minutes, seconds]]

        with sqlite3.connect('Scoreboard.db') as db:
            cursor = db.cursor()
            query = '''
            INSERT INTO Scoreboard
            VALUES(?, ?, ?)
            '''
            cursor.execute(query, [self.score, ':'.join(parse(duration)), DATE])


class Settings(Screen):
    pass


class Gameplay(Screen):
    pass


class Minimap:
    pass


class Player:
    def __init__(self):
        # main stats (always shown for player)
        self.hp = 200
        self.mana = 200
        self.stamina = 200

        # sub stats (shown in a special window)
        self.attack = 5
        self.attack_speed = 1

        self.move_speed = 5

        self.max_hp = 200
        self.max_mana = 200

        self.mana_regeneration = 0

        # weapon stats (increased with upgrades)
        self.swing_width = 60

        self.arrow_amount = 1

        self.mana_usage = 0
        self.spell_cast_speed = 5


class Inventory:
    pass


# items
class Item:
    pass


class Weapon(Item):
    pass


class Sword(Weapon):
    pass


class Bow(Weapon):
    pass


class Staff(Weapon):
    pass


class PickUp:
    pass


class Treasure(PickUp):
    pass


class Heal(PickUp):
    pass


class Key(PickUp):
    pass


class Upgrade(Item):
    pass


class CharacterUpgrade(Upgrade):
    pass


class WeaponUpgrade(Upgrade):
    pass


# world
class WorldGenerator:
    pass


class Floor:
    pass


class Room:
    pass


class Start(Room):
    pass


class Shop(Room):
    pass


class BattleRoom(Room):
    pass


class SimpleRoom(BattleRoom):
    pass


class DifficultRoom(BattleRoom):
    pass


class BoosRoom(BattleRoom):
    pass


def main():
    pass


if __name__ == '__main__':
    main()
    pygame.quit()
