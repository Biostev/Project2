import pygame
import sqlite3
import datetime
import os
import sys
import random
import math


START_TIME = datetime.datetime.now()
DATE = datetime.date.today()

ALL_SPRITES = {
    'Player': [],
    'Arrow': [],
    'TestEnemy': [],
    'floor_light': [],
    'floor_dark': [],
    'wall': [],
    'door': []
    }

pygame.init()
size = WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode(size)
FPS = 30

player_group = pygame.sprite.Group()
arrows_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
map_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
doors_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

fight_room_group = pygame.sprite.Group()
simple_fight_room_group = pygame.sprite.Group()
elite_fight_room_group = pygame.sprite.Group()
boss_fight_room_group = pygame.sprite.Group()

to_draw_group = pygame.sprite.Group()


def load_image(filename):
    fullname = os.path.join('gameplay resources', 'Sprites', filename) + '.png'
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
        self.pos = [tile_width * (pos[0] + 0.5), tile_height * (pos[1] + 0.5)]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.inventory = []
        self.selected_item = None

        self.hp = 200
        self.dmg = 5
        self.speed = 20

        self.arrow_speed = 30
        self.attack_speed = 500
        self.last_shot_time = 0

        self.spawns = None
        self.spawn_counter = [0, 0, 0]

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def wall_check(self, old_rect, old_pos):
        if pygame.sprite.spritecollideany(self, wall_group) or \
                pygame.sprite.spritecollideany(self, doors_group):
            self.rect = old_rect
            self.pos = old_pos

    def fight_start(self):
        if pygame.sprite.spritecollideany(self, fight_room_group):
            if pygame.sprite.spritecollideany(self, simple_fight_room_group) and self.spawn_counter[0] < 1:
                enemy_spawn('simple', self.spawns[0])
                self.spawn_counter[0] += 1
            if pygame.sprite.spritecollideany(self, elite_fight_room_group) and self.spawn_counter[1] < 1:
                enemy_spawn('elite', self.spawns[1])
                self.spawn_counter[1] += 1
            if pygame.sprite.spritecollideany(self, boss_fight_room_group) and self.spawn_counter[2] < 1:
                enemy_spawn('boss', self.spawns[2])
                self.spawn_counter[2] += 1

    def shoot(self, pos):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.attack_speed:
            self.last_shot_time = now
            bullet = Projectile(arrows_group, self.arrow_speed, self.rect.center, pos)
            arrows.append(bullet)
            all_objects.append(bullet)

    def move(self, keys):
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
        self.wall_check(old_rect, old_pos)

    def update(self, keys):

        if any(keys):
            self.move(keys)

            if keys[pygame.K_y]:
                pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
                enemy = TestEnemy(enemies_group, pos)
                enemies[0].append(enemy)
                all_objects.append(enemy)

        self.fight_start()


class Inventory:
    pass


def start_fight():
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
                pygame.sprite.spritecollideany(self, wall_group):
            self.kill()


class TestEnemy(pygame.sprite.Sprite):
    images = ALL_SPRITES['TestEnemy']

    def __init__(self, group, cords):
        super().__init__(group)
        self.image = TestEnemy.images[0]
        self.rect = self.image.get_rect()
        self.orig_image = self.image

        self.pos = pygame.math.Vector2(cords[0], cords[1])
        self.rect.topleft = self.pos
        self.speed = 10

        self.hp = 20

        self.last_hit_time = 0
        self.immune_frames = 200

    def rotate(self, player_cords):
        pos_x, pos_y = self.pos - player_cords
        angle = math.degrees(math.atan2(pos_x, pos_y))
        self.image = pygame.transform.rotozoom(self.orig_image, angle, 1)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def move(self, player_cords):
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
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

    def get_hit(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > self.immune_frames:
            self.last_hit_time = now
            self.hp -= 5

    def update(self, player_cords):
        self.move(player_cords)
        self.rotate(player_cords)

        for arrow in arrows_group:
            if pygame.sprite.collide_mask(self, arrow):
                self.get_hit()
                if self.hp <= 0:
                    self.kill()
                    for i in range(len(enemies)):
                        if self in enemies[i]:
                            enemies[i].remove(self)
            # all_objects.remove(self)


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
        if tile_type == 'wall':
            super().__init__(wall_group)
            self.group = wall_group
        else:
            super().__init__(tiles_group)
            self.group = tiles_group

        self.room_type = None

        self.image = ALL_SPRITES[tile_type][0]
        self.tile_type = tile_type
        self.pos = [pos_x, pos_y]
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def change_room_type(self):
        if self.room_type in ('SimpleFight', 'EliteFight', 'BossFight'):
            super().__init__(fight_room_group)
            if self.room_type == 'SimpleFight':
                super().__init__(simple_fight_room_group)
                self.group = simple_fight_room_group
            elif self.room_type == 'EliteFight':
                super().__init__(elite_fight_room_group)
                self.group = elite_fight_room_group
            elif self.room_type == 'BossFight':
                super().__init__(boss_fight_room_group)
                self.group = boss_fight_room_group

    def update(self):
        delta = 100
        self.pos = list(self.rect.topleft)
        if -delta <= self.rect.x <= WIDTH + delta and \
                -delta <= self.rect.y <= HEIGHT + delta:
            to_draw_group.add(self)
        else:
            to_draw_group.remove(self)


class Door(Tile):
    images = ALL_SPRITES['door']

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_type, pos_x, pos_y)
        self.alive_enemies = 0
        self.image = Door.images[0]

    def update(self):
        if any(enemies):
            wall_group.add(self)
            to_draw_group.add(self)
        else:
            wall_group.remove(self)
            to_draw_group.remove(self)


def generate_level(level):
    new_player, x, y = None, None, None
    simple_rooms = []
    elite_rooms = []
    boss_rooms = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                tile = Tile('wall', x, y)
                all_objects.append(tile)
                tile.change_room_type()
            elif level[y][x] in ['.', '*', '\\', '^', '_', '@', '→']:
                tile = Tile('floor_light', x, y) if (x + y) % 2 else Tile('floor_dark', x, y)
                if level[y][x] == '.':
                    tile.room_type = 'floor'
                elif level[y][x] == '*':
                    tile.room_type = 'SimpleFight'
                    simple_rooms.append(tile)
                elif level[y][x] == '\\':
                    tile.room_type = 'EliteFight'
                    elite_rooms.append(tile)
                elif level[y][x] == '^':
                    tile.room_type = 'BossFight'
                    boss_rooms.append(tile)
                elif level[y][x] == '_':
                    door = Door('door', x, y)
                    all_objects.append(door)
                elif level[y][x] == '@':
                    new_player = Player([x, y], player_group)
                    all_objects.append(new_player)
                elif level[y][x] == '→':
                    tile.room_type = 'exit'
                tile.change_room_type()
                all_objects.append(tile)
    return new_player, x, y, simple_rooms, elite_rooms, boss_rooms


enemies = [[], [], []]


def enemy_spawn(enemy_type, spawns):
    cords = []
    ind = None
    if enemy_type == 'simple':
        ind = 0
        cords = random.sample(spawns, 5)
    if enemy_type == 'elite':
        ind = 1
        cords = random.sample(spawns, 5)
    if enemy_type == 'boss':
        ind = 2
        cords = random.sample(spawns, 1)
    for cord in cords:
        enemy = TestEnemy(enemies_group, (cord.pos[0], cord.pos[1]))
        enemies[ind].append(enemy)
        all_objects.append(enemy)


class Floor:
    pass


class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if isinstance(obj, Tile) or isinstance(obj, Player):
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        obj.pos[0] += self.dx
        obj.pos[1] += self.dy

    def update(self, target):
        self.dx = -(target.pos[0] - WIDTH // 2)
        self.dy = -(target.pos[1] - HEIGHT // 2)


def drawer(images):
    for image in images:
        image.draw(screen)


arrows = []


def main():
    text_map = load_level('Map2.txt')
    player, level_x, level_y, simple_spawns, elite_spawns, boss_spawns = generate_level(text_map)
    player.spawns = [simple_spawns, elite_spawns, boss_spawns]

    all_images = [to_draw_group, arrows_group,
                  enemies_group, player_group]

    clock = pygame.time.Clock()

    camera = Camera(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    player.shoot(pos)

        keys = pygame.key.get_pressed()
        player_group.update(keys)

        arrows_group.update()
        enemies_group.update(player.rect.topleft)

        camera.update(player)
        for obj in all_objects:
            camera.apply(obj)
        tiles_group.update()
        wall_group.update()
        doors_group.update()

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
