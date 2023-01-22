import datetime
import math
import os
import random
import sys

import pygame

START_TIME = datetime.datetime.now()
DATE = datetime.date.today()

ALL_SPRITES = {
    'Player': [],
    'Arrow': [],
    'floor_light': [],
    'floor_dark': [],
    'wall': [],
    'door': [],
    'exit': [],
    'Cursor': [],
    'MeleeEnemy2': [],
    }

pygame.init()
pygame.mixer.music.load(os.path.join('gameplay resources', 'music', 'back_music') + '.wav')
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
FPS = 30


class GameManager:
    def __init__(self):
        self.score = 0
        self.player_group = pygame.sprite.Group()
        self.arrows_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()

        self.tiles_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.doors_group = pygame.sprite.Group()

        self.exit_group = pygame.sprite.Group()

        self.fight_room_group = pygame.sprite.Group()
        self.simple_fight_room_group = pygame.sprite.Group()
        self.elite_fight_room_group = pygame.sprite.Group()
        self.boss_fight_room_group = pygame.sprite.Group()

        self.to_draw_group = pygame.sprite.Group()
        self.cursor = pygame.sprite.Group()

        self.hp_bars = []
        self.floor = 0
        self.floor_passed = 0

        self.text_map = None
        self.tile_width = self.tile_height = 100
        self.player, self.level_x, self.level_y = [None] * 3

        self.all_images = [self.to_draw_group, self.arrows_group,
                           self.enemies_group, self.player_group]
        self.groups = [self.arrows_group, self.tiles_group,
                       self.wall_group, self.doors_group,
                       self.exit_group]

        self.all_objects = []
        self.arrows = []
        self.enemies = [[], [], []]

        self.clock = pygame.time.Clock()

        self.camera = Camera(WIDTH, HEIGHT)
        Cursor(self.cursor)

        pygame.mouse.set_visible(False)
        self.hp_save = 200

    def start_game(self, new):
        self.player_group = pygame.sprite.Group()
        self.arrows_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()

        self.tiles_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.doors_group = pygame.sprite.Group()

        self.exit_group = pygame.sprite.Group()

        self.fight_room_group = pygame.sprite.Group()
        self.simple_fight_room_group = pygame.sprite.Group()
        self.elite_fight_room_group = pygame.sprite.Group()
        self.boss_fight_room_group = pygame.sprite.Group()

        self.to_draw_group = pygame.sprite.Group()
        self.cursor = pygame.sprite.Group()

        self.hp_bars = []

        if new:
            self.score = 0
            self.floor = 0
            self.floor_passed = 0
            self.hp_save = 200

        self.text_map = None
        self.tile_width = self.tile_height = 100
        self.player, self.level_x, self.level_y = [None] * 3

        self.all_images = [self.to_draw_group, self.arrows_group,
                           self.enemies_group, self.player_group]
        self.groups = [self.arrows_group, self.tiles_group,
                       self.wall_group, self.doors_group,
                       self.exit_group]

        self.all_objects = []
        self.arrows = []
        self.enemies = [[], [], []]

        self.clock = pygame.time.Clock()

        self.camera = Camera(WIDTH, HEIGHT)
        Cursor(self.cursor)

        self.new_floor()
        self.player.cur_hp = self.hp_save

    def new_floor(self):
        self.floor += 1
        self.load_level('Map1.txt')
        self.generate_level(self.text_map)

    def load_level(self, filename):
        filename = "gameplay resources\\maps\\" + filename
        with open(filename, 'r') as file:
            self.text_map = [line for line in file]

    def generate_level(self, level):
        new_player, x, y = None, None, None
        simple_rooms = []
        elite_rooms = []
        boss_rooms = []
        for y in range(len(level)):
            possible_symbols = ['.', '*', '\\', '^', '_', '@', 'e', '1', '2', '3']
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    tile = Tile('wall', x, y)
                    game.all_objects.append(tile)
                    tile.change_room_type()
                elif level[y][x] in possible_symbols:
                    if level[y][x] == 'e':
                        end = Exit('exit', x, y)
                        game.all_objects.append(end)
                        continue
                    tile = Tile('floor_light', x, y) if (x + y) % 2 else Tile('floor_dark', x, y)
                    if level[y][x] == '.':
                        tile.room_type = 'floor'
                    elif level[y][x] == '*':
                        tile.room_type = 'SimpleFight'
                    elif level[y][x] == '1':
                        tile.room_type = 'SimpleFight'
                        simple_rooms.append(tile)
                    elif level[y][x] == '\\':
                        tile.room_type = 'EliteFight'
                    elif level[y][x] == '2':
                        tile.room_type = 'EliteFight'
                        elite_rooms.append(tile)
                    elif level[y][x] == '^':
                        tile.room_type = 'BossFight'
                    elif level[y][x] == '3':
                        tile.room_type = 'BossFight'
                        boss_rooms.append(tile)
                    elif level[y][x] == '_':
                        door = Door('door', x, y)
                        game.all_objects.append(door)
                    elif level[y][x] == '@':
                        new_player = Player([x, y], self.player_group)
                        game.all_objects.append(new_player)
                    tile.change_room_type()
                    game.all_objects.append(tile)
        self.player, self.level_x, self.level_y = new_player, x, y
        self.player.spawns = simple_rooms, elite_rooms, boss_rooms

    def update(self):
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
            self.cursor.update(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        self.updater()
        self.exit_group.update()

        self.enemies_group.update(self.player.rect.topleft)

        keys = pygame.key.get_pressed()
        self.player_group.update(keys)

        self.camera.update(self.player)
        for obj in self.all_objects:
            self.camera.apply(obj)

        self.drawer()

        if pygame.mouse.get_focused():
            self.cursor.draw(screen)

    def drawer(self):
        for image in self.all_images:
            image.draw(screen)
        for hp_bar in self.hp_bars:
            hp_bar.draw()

    def updater(self):
        for group in self.groups:
            group.update()


def load_image(filename):
    fullname = os.path.join('gameplay resources', 'Sprites', filename) + '.png'
    image = pygame.image.load(fullname)
    return image


for sprite in ALL_SPRITES.keys():
    if sprite[-1].isdigit():
        for i in range(int(sprite[-1])):
            ALL_SPRITES[sprite].append(load_image(f'{sprite[:-1]}{i}'))
        continue
    ALL_SPRITES[sprite].append(load_image(sprite))


# class Scoreboard:
#     def __init__(self):
#         self.score = 0
#
#     def add_score(self, score):
#         self.score += score
#
#     def add_to_db(self):
#         duration = datetime.datetime.now() - START_TIME
#
#         def parse(time):
#             seconds = int(time.total_seconds())
#             hours = seconds // 3600
#             seconds -= hours * 3600
#             minutes = seconds // 60
#             seconds -= minutes * 60
#             return [str(time) for time in [hours, minutes, seconds]]
#
#         with sqlite3.connect('Scoreboard.db') as db:
#             db_cursor = db.cursor()
#             query = '''
#             INSERT INTO Scoreboard
#             VALUES(?, ?, ?)
#             '''
#             db_cursor.execute(query, [self.score, ':'.join(parse(duration)), DATE])


class HpBar:
    def __init__(self, owner):
        self.owner = owner
        x, y = owner.rect.bottomleft
        self.width_const = owner.rect.width

        self.cur_hp = pygame.Rect((x, y + owner.rect.height + 10,
                                   self.width_const, 20))

        self.max_hp = pygame.Rect((x, y + owner.rect.height + 10,
                                   self.width_const, 20))

        game.hp_bars.append(self)
        game.all_objects.append(self)

    def update(self, max_hp, cur_hp):
        pos = self.owner.rect.bottomleft[0], self.owner.rect.bottomleft[1] + 10
        self.cur_hp.width = cur_hp / max_hp * self.width_const
        self.cur_hp.topleft = pos
        self.max_hp.topleft = pos

        if cur_hp <= 0:
            game.hp_bars.remove(self)

    def draw(self):
        pygame.draw.rect(screen, (200, 0, 0), self.max_hp)
        pygame.draw.rect(screen, (0, 200, 0), self.cur_hp)


class Player(pygame.sprite.Sprite):
    images = ALL_SPRITES['Player']

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Player.images[0]
        self.pos = [game.tile_width * (pos[0] + 0.5), game.tile_height * (pos[1] + 0.5)]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)

        self.score = 0

        self.max_hp = 200
        self.cur_hp = 200
        self.dmg = 10
        self.speed = 20
        self.main_speed = self.speed

        self.arrow_speed = 30
        self.attack_speed = 300
        self.last_shot_time = 0

        self.spawns = None
        self.spawn_counter = [0, 0, 0]

        self.hp_bar = HpBar(self)

        self.in_dash = False
        self.dash_cd = 700
        self.last_dash = 0
        self.dash_goal = None

        self.last_hit_time = 0
        self.immune_frames = 200

    def wall_check(self, old_rect, old_pos):
        if pygame.sprite.spritecollideany(self, game.exit_group):
            game.score += 100
            game.hp_save = self.cur_hp
            game.start_game(False)

        if pygame.sprite.spritecollideany(self, game.wall_group) or \
                pygame.sprite.spritecollideany(self, game.doors_group):
            self.rect = old_rect
            self.pos = old_pos[:]

    def enemy_spawn(self, enemy_type, spawns):
        cords = []
        ind = None
        modifier = 1
        if enemy_type == 'simple':
            ind = 0
            cords = random.sample(spawns, 5)
        if enemy_type == 'elite':
            ind = 1
            cords = random.sample(spawns, 5)
            modifier = 1.5
        if enemy_type == 'boss':
            ind = 2
            cords = random.sample(spawns, 1)
            modifier = 2
        for cord in cords:
            enemy = MeleeEnemy(game.enemies_group, (cord.pos[0], cord.pos[1]), modifier)
            game.enemies[ind].append(enemy)
            game.all_objects.append(enemy)

    def fight_start(self):
        if pygame.sprite.spritecollideany(self, game.simple_fight_room_group) and self.spawn_counter[0] < 1:
            self.enemy_spawn('simple', self.spawns[0])
            self.spawn_counter[0] += 1
        if pygame.sprite.spritecollideany(self, game.elite_fight_room_group) and self.spawn_counter[1] < 1:
            self.enemy_spawn('elite', self.spawns[1])
            self.spawn_counter[1] += 1
        if pygame.sprite.spritecollideany(self, game.boss_fight_room_group) and self.spawn_counter[2] < 1:
            self.enemy_spawn('boss', self.spawns[2])
            self.spawn_counter[2] += 1

    def shoot(self):
        pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.attack_speed:
            self.last_shot_time = now
            bullet = Projectile(game.arrows_group, self.dmg, self.arrow_speed, self.rect.center, pos)
            game.arrows.append(bullet)
            game.all_objects.append(bullet)

    def move(self, keys):
        old_rect = self.rect
        old_pos = self.pos[:]
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect = self.rect.move(0, self.speed)
            self.pos[1] += 10
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect = self.rect.move(0, -self.speed)
            self.pos[1] -= 10
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect = self.rect.move(self.speed, 0)
            self.pos[0] += 10
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect = self.rect.move(-self.speed, 0)
            self.pos[0] -= 10
        self.wall_check(old_rect, old_pos)

    def death(self):
        death_screen()

    def dash(self):
        old_rect = self.rect
        old_pos = self.pos[:]
        self.speed = 30
        now = pygame.time.get_ticks()
        if now - self.last_dash < self.dash_cd - 450:
            self.pos -= self.dash_goal * self.speed
        else:
            self.in_dash = False
            self.speed = self.main_speed
        shift = round(self.pos[0] - old_pos[0]), round(self.pos[1] - old_pos[1])
        self.rect = self.rect.move(shift)
        self.wall_check(old_rect, old_pos)

    def update(self, keys):
        if any(keys):
            if not self.in_dash:
                self.move(keys)

            if keys[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if (now - self.last_dash >= self.dash_cd) and not self.in_dash:
                    mouse = pygame.mouse.get_pos()
                    self.last_dash = now
                    self.dash_goal = pygame.math.Vector2(self.rect.center[0] - mouse[0],
                                                         self.rect.center[1] - mouse[1]).normalize()
                    self.in_dash = True

        if self.in_dash:
            self.dash()

        if pygame.sprite.spritecollideany(self, game.fight_room_group):
            self.fight_start()

        for enemy in game.enemies_group:
            now = pygame.time.get_ticks()
            if pygame.sprite.collide_mask(self, enemy) and \
                    now - self.last_hit_time >= self.immune_frames:
                self.last_hit_time = now
                self.cur_hp -= enemy.dmg

        self.hp_bar.update(self.max_hp, self.cur_hp)
        if self.cur_hp <= 0:
            self.death()
            self.kill()


class Projectile(pygame.sprite.Sprite):
    images = ALL_SPRITES['Arrow']

    def __init__(self, group, dmg, speed, start_pos, goal):
        super().__init__(group)
        self.image = Projectile.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(start_pos)
        self.goal = pygame.math.Vector2(goal[0] - self.pos[0], goal[1] - self.pos[1]).normalize()
        self.speed = speed
        self.dmg = dmg

    def update(self):
        self.pos += self.goal * self.speed
        self.rect.center = round(self.pos.x), round(self.pos.y)
        if (self.pos.x < -10 or self.pos.x > WIDTH + 10) or \
                (self.pos.y < -10 or self.pos.y > HEIGHT + 10) or \
                pygame.sprite.spritecollideany(self, game.wall_group):
            self.kill()


class MeleeEnemy(pygame.sprite.Sprite):
    images = ALL_SPRITES['MeleeEnemy2']

    def __init__(self, group, cords, modifier):
        super().__init__(group)
        self.frame_index = 0
        self.image = MeleeEnemy.images[self.frame_index]
        self.update_frames = 1000
        self.last_frame_update = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.orig_image = self.image

        self.pos = pygame.math.Vector2(cords[0], cords[1])
        self.rect.topleft = self.pos
        self.speed = 10
        self.main_speed = self.speed

        self.modifier = modifier

        self.max_hp = 20 * game.floor * self.modifier
        self.cur_hp = self.max_hp

        self.hp_bar = HpBar(self)

        self.dmg = round(20 * game.floor * self.modifier)

        self.in_attack = False
        self.last_attack = random.choice([j * 100 for j in range(20)])
        self.attack_cd = 2000
        self.goal = None

    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_update >= self.update_frames:
            self.last_frame_update = now
            self.frame_index += 1
            if self.frame_index > 1:
                self.frame_index = 0
        self.image = MeleeEnemy.images[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.orig_image = self.image

    def rotate(self, player_cords):
        pos_x, pos_y = self.pos - player_cords
        angle = math.degrees(math.atan2(pos_x, pos_y))
        self.image = pygame.transform.rotozoom(self.orig_image, angle, 1)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def move(self, player_cords):
        distance = round(pygame.math.Vector2(player_cords).distance_to(self.pos))
        goal = pygame.math.Vector2((self.pos - player_cords)).normalize()
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

    def attack(self, player_cords):
        self.speed = 20
        distance = round(pygame.math.Vector2(player_cords).distance_to(self.pos))
        if distance <= 400:
            self.pos -= self.goal * self.speed
        else:
            self.in_attack = False
            self.speed = self.main_speed
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

    def update(self, player_cords):
        self.animation()
        now = pygame.time.get_ticks()
        if not self.in_attack:
            self.move(player_cords)
        self.rotate(player_cords)

        if (now - self.last_attack >= self.attack_cd) and not self.in_attack:
            self.last_attack = now
            self.goal = pygame.math.Vector2((self.pos - player_cords)).normalize()
            self.in_attack = True

        if self.in_attack:
            self.attack(player_cords)

        for arrow in game.arrows_group:
            if pygame.sprite.collide_mask(self, arrow):
                self.cur_hp -= arrow.dmg
                arrow.kill()
                if self.cur_hp <= 0:
                    self.kill()
                    game.score += 5 * game.floor * self.modifier
                    if self.modifier == 2:
                        game.floor_passed += 1
                    for enemy in range(len(game.enemies)):
                        if self in game.enemies[enemy]:
                            game.enemies[enemy].remove(self)
        self.hp_bar.update(self.max_hp, self.cur_hp)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(game.wall_group)
            self.group = game.wall_group
        elif tile_type == 'exit':
            super().__init__(game.exit_group)
            self.group = game.exit_group
        else:
            super().__init__(game.tiles_group)
            self.group = game.tiles_group

        self.room_type = None

        self.image = ALL_SPRITES[tile_type][0]
        self.tile_type = tile_type
        self.pos = [pos_x, pos_y]
        self.rect = self.image.get_rect().move(
            game.tile_width * self.pos[0], game.tile_height * self.pos[1])

    def change_room_type(self):
        if self.room_type in ('SimpleFight', 'EliteFight', 'BossFight'):
            super().__init__(game.fight_room_group)
            if self.room_type == 'SimpleFight':
                super().__init__(game.simple_fight_room_group)
                self.group = game.simple_fight_room_group
            elif self.room_type == 'EliteFight':
                super().__init__(game.elite_fight_room_group)
                self.group = game.elite_fight_room_group
            elif self.room_type == 'BossFight':
                super().__init__(game.boss_fight_room_group)
                self.group = game.boss_fight_room_group

    def update(self):
        delta = 200
        self.pos = list(self.rect.topleft)
        if -delta <= self.rect.x <= WIDTH + delta and \
                -delta <= self.rect.y <= HEIGHT + delta:
            game.to_draw_group.add(self)
        else:
            game.to_draw_group.remove(self)


class Door(Tile):
    images = ALL_SPRITES['door']

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_type, pos_x, pos_y)
        self.image = Door.images[0]

    def update(self):
        if any(game.enemies):
            game.wall_group.add(self)
            game.to_draw_group.add(self)
        else:
            game.wall_group.remove(self)
            game.to_draw_group.remove(self)


class Exit(Tile):
    closed = ALL_SPRITES['wall']
    passed = ALL_SPRITES['exit']

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_type, pos_x, pos_y)
        self.image = Exit.closed[0]
        game.to_draw_group.add(self)

    def update(self):
        if game.floor_passed < game.floor:
            game.exit_group.remove(self)
            game.wall_group.add(self)
            self.image = Exit.closed[0]
        else:
            game.wall_group.remove(self)
            game.exit_group.add(self)
            self.image = Exit.passed[0]
        game.to_draw_group.add(self)


class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if isinstance(obj, HpBar):
            obj.cur_hp.x += self.dx
            obj.cur_hp.y += self.dy
            obj.max_hp.x += self.dx
            obj.max_hp.y += self.dy
            return
        if isinstance(obj, Player):
            obj.rect.x += self.dx
            obj.rect.y += self.dy
            return
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        obj.pos[0] += self.dx
        obj.pos[1] += self.dy

    def update(self, target):
        self.dx = -(target.rect.x - WIDTH // 2)
        self.dy = -(target.rect.y - HEIGHT // 2)


class Cursor(pygame.sprite.Sprite):
    image = ALL_SPRITES['Cursor'][0]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            self.rect.center = args[0].pos


def MainMenu():
    intro_text = [
        'Press any key',
        'to start the game',
        'or ESC to exit'
    ]

    fon = pygame.transform.scale(load_image('menu'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    text_size = 60
    font = pygame.font.SysFont('comicsansms', text_size)
    text_coord = HEIGHT // 2 - text_size * len(intro_text)
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += text_size + 10
        intro_rect.top = text_coord
        intro_rect.x = (WIDTH - intro_rect.width) // 2
        text_coord += 10
        screen.blit(string_rendered, intro_rect)

    time = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminate()
                game.start_game(True)
                return
        pygame.display.flip()
        time.tick(FPS)


def pause():
    intro_text = [
        'Press any key to continue',
        'or ESC to exit to main menu'
    ]

    fon = pygame.transform.scale(load_image('pause'), (WIDTH, HEIGHT))
    fon.set_colorkey((100, 100, 100, 50))
    screen.blit(fon, (0, 0))
    text_size = 60
    font = pygame.font.SysFont('comicsansms', text_size)
    text_coord = HEIGHT // 2 - text_size * len(intro_text)
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += text_size + 10
        intro_rect.top = text_coord
        intro_rect.x = (WIDTH - intro_rect.width) // 2
        text_coord += 10
        screen.blit(string_rendered, intro_rect)

    time = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        MainMenu()
                return
        pygame.display.flip()
        time.tick(FPS)


def death_screen():
    intro_text = [
        'Game Over',
        f'Your score is {game.score}.',
        'or ESC to exit to main menu'
    ]

    fon = pygame.transform.scale(load_image('pause'), (WIDTH, HEIGHT))
    fon.set_colorkey((100, 100, 100, 50))
    screen.blit(fon, (0, 0))
    text_size = 60
    font = pygame.font.SysFont('comicsansms', text_size)
    text_coord = HEIGHT // 2 - text_size * len(intro_text)
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += text_size + 10
        intro_rect.top = text_coord
        intro_rect.x = (WIDTH - intro_rect.width) // 2
        text_coord += 10
        screen.blit(string_rendered, intro_rect)

    time = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
                    return
        pygame.display.flip()
        time.tick(FPS)


game = GameManager()
running = True


def main():
    MainMenu()
    pygame.mouse.set_visible(False)

    while running:
        game.update()
        game.clock.tick(FPS)
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
    terminate()
