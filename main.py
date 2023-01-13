import pygame
import sqlite3
import datetime
import os
import sys
import random


START_TIME = datetime.datetime.now()
DATE = datetime.date.today()

ALL_SPRITES = {
    'Player': [],
    'Arrow': [],
    'TestEnemy': [],
    'floor_light': [],
    'floor_dark': [],
    'wall': []
    }

pygame.init()
size = WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode(size)
FPS = 60

player_group = pygame.sprite.Group()
arrows_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
map_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
to_draw_group = pygame.sprite.Group()


def load_image(filename):
    fullname = os.path.join('gameplay resources\\Sprites', filename) + '.png'
    image = pygame.image.load(fullname)
    return image


for sprite in ALL_SPRITES.keys():
    ALL_SPRITES[sprite].append(load_image(sprite))


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
            return [str(time) for time in [hours, minutes, seconds]]

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


class Player(pygame.sprite.Sprite):
    images = ALL_SPRITES['Player']

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Player.images[0]
        self.pos = [tile_width * pos[0], tile_height * pos[1]]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        self.move = True

        self.inventory = []
        self.selected_item = None

        self.speed = 10

        self.arrow_speed = 10
        '''# main stats (always shown for player)
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
        self.spell_cast_speed = 5'''

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def update(self, keys):
        if keys:
            old_rect = self.rect
            old_pos = self.pos[:]
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect = self.rect.move(0, self.speed)
                self.pos[1] += self.speed
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect = self.rect.move(0, -self.speed)
                self.pos[1] -= self.speed
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect = self.rect.move(self.speed, 0)
                self.pos[0] += self.speed
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect = self.rect.move(-self.speed, 0)
                self.pos[0] -= self.speed

            if pygame.sprite.spritecollideany(self, boxes_group):
                self.rect = old_rect
                self.pos = old_pos


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


class Projectile(pygame.sprite.Sprite):
    images = ALL_SPRITES['Arrow']

    def __init__(self, group, speed, start_pos, goal):
        super().__init__(group)
        self.image = Projectile.images[0]
        self.rect = self.image.get_rect()

        self.pos = pygame.math.Vector2(start_pos)
        self.goal = pygame.math.Vector2(goal[0] - self.pos[0], goal[1] - self.pos[1]).normalize()
        self.speed = speed

    def update(self):
        self.pos += self.goal * self.speed
        self.rect.center = round(self.pos.x), round(self.pos.y)
        if (self.pos.x < -10 or self.pos.x > WIDTH + 10) or \
                (self.pos.y < -10 or self.pos.y > HEIGHT + 10) or \
                pygame.sprite.spritecollideany(self, boxes_group):
            self.kill()


class TestEnemy(pygame.sprite.Sprite):
    images = ALL_SPRITES['TestEnemy']

    def __init__(self, group):
        super().__init__(group)
        self.image = TestEnemy.images[0]
        self.rect = self.image.get_rect()

        self.pos = pygame.math.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.speed = 5

    def update(self, player_cords):
        distance = round(pygame.math.Vector2(player_cords).distance_to(self.pos))
        goal = pygame.math.Vector2(self.pos - player_cords).normalize()
        if distance > 200:
            self.pos -= goal * self.speed
            self.rect.center = round(self.pos.x), round(self.pos.y)
        else:
            if distance < 190:
                self.pos += goal * self.speed
                self.rect.center = round(self.pos.x), round(self.pos.y)
            new_goal = pygame.math.Vector2(goal.y, -goal.x)
            self.pos += new_goal * self.speed
            self.rect.center = round(self.pos.x), round(self.pos.y)
        if pygame.sprite.spritecollideany(self, arrows_group):
            self.kill()
            all_objects.remove(self)


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
tile_width = tile_height = 100
all_objects = []


def load_level(filename):
    filename = "gameplay resources\\maps\\" + filename
    with open(filename, 'r') as file:
        level_map = [line for line in file]
    return level_map


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type in ('floor_light', 'floor_dark'):
            super().__init__(tiles_group)
            self.group = tiles_group
        else:
            super().__init__(boxes_group)
            self.group = boxes_group
        self.image = ALL_SPRITES[tile_type][0]
        self.tile_type = tile_type
        self.pos = [pos_x, pos_y]
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def update(self):
        delta = 100
        if -delta <= self.rect.x <= WIDTH + delta and \
                -delta <= self.rect.y <= HEIGHT + delta:
            to_draw_group.add(self)
        else:
            self.remove(to_draw_group)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                tile = Tile('wall', x, y)
                all_objects.append(tile)
            elif level[y][x] in ['.', '@']:
                tile = Tile('floor_light', x, y) if (x + y) % 2 else Tile('floor_dark', x, y)
                if level[y][x] == '@':
                    new_player = Player([x, y], player_group)
                    all_objects.append(new_player)
                all_objects.append(tile)
    return new_player, x, y


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


class BossRoom(BattleRoom):
    pass


class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.pos[0] += self.dx
        obj.pos[1] += self.dy
        if isinstance(obj, Tile) or isinstance(obj, Player):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.pos[0] - WIDTH // 2)
        self.dy = -(target.pos[1] - HEIGHT // 2)


def drawer(images):
    for image in images:
        image.draw(screen)


arrows = []
enemies = []


def main():
    text_map = load_level('Map1.txt')
    player, level_x, level_y = generate_level(text_map)

    all_images = [to_draw_group, arrows_group,
                  enemies_group, player_group]

    clock = pygame.time.Clock()

    camera = Camera(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    bullet = Projectile(arrows_group, player.arrow_speed, player.rect.center, pos)
                    arrows.append(bullet)
                    all_objects.append(bullet)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    enemy = TestEnemy(enemies_group)
                    enemies.append(enemy)
                    all_objects.append(enemy)

        keys = pygame.key.get_pressed()
        player_group.update(keys)
        arrows_group.update()
        if enemies:
            enemies_group.update(player.rect.center)

        camera.update(player)
        for obj in all_objects:
            camera.apply(obj)
        tiles_group.update()
        boxes_group.update()

        screen.fill('black')
        drawer(all_images)
        clock.tick(FPS)
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
    terminate()
