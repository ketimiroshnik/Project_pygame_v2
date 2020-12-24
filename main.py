import pygame
import pprint

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 700
BUTTON_PLACE = 50
FPS = 40
MAP_DIR = 'levels'
IMAGE_DIR = 'images'
TILE_SIZE = None

WALL_PER = 0.2

SIGNS = {'free': ' ', 'dynamic_stone': 'b', 'static_stone': 'B', 'fire_lake': 'f', 'water_lake': 'w',
         'fire': 'F', 'water': 'W', 'water_door': '$', 'fire_door': '#', 'wall': '-'}

COLORS = {'dynamic_stone': (90, 90, 90), 'static_stone': (101, 66, 10),
          'fire_lake': (210, 60, 0), 'water_lake': (0, 160, 210),
          'fire': (255, 20, 30), 'water': (30, 20, 255),
          'water_door': (60, 100, 200), 'fire_door': (255, 50, 100),
          'wall': (101, 66, 33)}

SIZES = {'dynamic_stone': None, 'static_stone': None,
         'fire_lake': None, 'water_lake': None,
         'fire': None, 'water': None,
         'water_door': None, 'fire_door': None,
         'g_wall': None, 'v_wall': None}

TYPE_BORD = {'left': 1, 'right': 2, 'up': 3, 'bottom': 4}


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, t):
        super().__init__(all_sprites)
        self.t = t
        if x1 == x2:  # вертикальная стенка
            self.add(v_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 5, y2 - y1)
        else:  # горизонтальная стенка
            self.add(g_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 5)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size, add_b=[]):
        super().__init__(all_sprites)
        self.add(walls)

        x, y = pos
        a, b = size
        if a > b:
            Border(x, y, x + a, y, TYPE_BORD['up'])
            Border(x, y + b, x + a, y + b, ['down'])
            for e in add_b:
                if e == TYPE_BORD['left']:
                    Border(x, y, x, y + b, TYPE_BORD['left'])
                elif e == TYPE_BORD['right']:
                    Border(x + a, y, x + a, y + b, TYPE_BORD['right'])
        else:
            Border(x, y, x, y + b, TYPE_BORD['left'])
            Border(x + a, y, x + a, y + b, TYPE_BORD['right'])

        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['wall'], (0, 0, *size))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)


class StaticStone(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.add(static_stones)

        x, y = pos
        a, b = size
        Border(x, y, x + a, y, TYPE_BORD['up'])
        Border(x, y + b, x + a, y + b, ['down'])
        Border(x, y, x, y + b, TYPE_BORD['left'])
        Border(x + a, y, x + a, y + b, TYPE_BORD['right'])

        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['static_stone'], (0, 0, *size))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)


class FireLake(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.add(fire_lakes)

        x, y = pos
        a, b = size
        Border(x, y, x + a, y, TYPE_BORD['up'])
        Border(x, y + b, x + a, y + b, ['down'])

        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['wall'], (0, 0, *size))
        pygame.draw.rect(self.image, (210, 60, 0), (0, 0, size[0], size[1] - TILE_SIZE * WALL_PER // 2))
        self.rect = pygame.Rect(*pos, *size)


class WaterLake(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.add(water_lakes)

        x, y = pos
        a, b = size
        Border(x, y, x + a, y, TYPE_BORD['up'])
        Border(x, y + b, x + a, y + b, ['down'])

        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['wall'], (0, 0, *size))
        pygame.draw.rect(self.image, COLORS['water_lake'], (0, 0, size[0], size[1] - TILE_SIZE * WALL_PER // 2))
        self.rect = pygame.Rect(*pos, *size)


class FireDoor(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.add(fire_doors)
        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['fire_door'], (0, 0, *size))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)

    def update(self):
        pass


class WaterDoor(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.add(water_doors)
        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['water_door'], (0, 0, *size))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)

    def update(self):
        pass


class DynamicStone(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.add(dynamic_stones)

        x, y = pos
        a, b = size
        Border(x, y, x + a, y, TYPE_BORD['up'])
        Border(x, y + b, x + a, y + b, ['down'])

        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, COLORS['dynamic_stone'], (0, 0, *size))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)

    def update(self):
        pass


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.ellipse(self.image, COLORS['fire'], (0, 0, *size))
        pygame.draw.ellipse(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)

    def update(self):
        pass


class Water(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.ellipse(self.image, COLORS['water'], (0, 0, *size))
        pygame.draw.ellipse(self.image, (0, 0, 0), (0, 0, *size), 1)
        self.rect = pygame.Rect(*pos, *size)
        self.on_fly = None

    def update(self):
        if pygame.key.get_pressed()[pygame.K_d] and not (
                pygame.sprite.spritecollideany(self, v_borders) and pygame.sprite.spritecollideany(self, v_borders).t ==
                TYPE_BORD['left']):
            self.rect = self.rect.move(TILE_SIZE / 25, 0)

        if pygame.key.get_pressed()[pygame.K_a] and not \
                (pygame.sprite.spritecollideany(self, v_borders) and
                 pygame.sprite.spritecollideany(self, v_borders).t == TYPE_BORD['right']):
            self.rect = self.rect.move(-TILE_SIZE / 25, 0)

        if not pygame.sprite.spritecollideany(self, g_borders):
            if self.on_fly is None:
                self.rect = self.rect.move(0, TILE_SIZE / 20)
        elif pygame.sprite.spritecollideany(self, g_borders).t != TYPE_BORD['up'] and self.on_fly is None:
            self.rect = self.rect.move(0, TILE_SIZE / 20)

        if self.on_fly is None and pygame.key.get_pressed()[pygame.K_w] and pygame.sprite.spritecollideany(self,
                                                                                                           g_borders) and \
                pygame.sprite.spritecollideany(self, g_borders).t == TYPE_BORD['up']:
            self.rect = self.rect.move(0, -TILE_SIZE / 20)
            self.on_fly = TILE_SIZE / 20
        elif self.on_fly is not None:
            if self.on_fly >= TILE_SIZE * (1 + WALL_PER + 0.05):
                self.on_fly = None
            else:
                if not pygame.sprite.spritecollideany(self, g_borders):
                    self.rect = self.rect.move(0, -TILE_SIZE / 20)
                    self.on_fly += TILE_SIZE / 20
                else:
                    self.on_fly = None


def load_level(filename):
    global TILE_SIZE, SIZES, water, fire
    level = []
    with open(f'{MAP_DIR}/{filename}') as input_file:
        for line in input_file:
            level.append(list(line.rstrip()))
    height = len(level)
    width = max((map(lambda x: len(x), level))) - 2
    for i in range(height):
        level[i] = list(''.join(level[i]).ljust(width + 2, SIGNS['free']))

    TILE_SIZE = int(min((2 * WINDOW_HEIGHT) / ((height / 2) + 2 * WALL_PER), WINDOW_WIDTH / (width + 2 * WALL_PER)))

    SIZES['fire'] = (TILE_SIZE / 2, 2 * TILE_SIZE / 3)
    SIZES['water'] = (TILE_SIZE / 2, 2 * TILE_SIZE / 3)
    SIZES['dynamic_stone'] = (TILE_SIZE / 2, TILE_SIZE / 2)
    SIZES['static_stone'] = (TILE_SIZE, TILE_SIZE)
    SIZES['fire_door'] = (TILE_SIZE * (1 - WALL_PER), TILE_SIZE)
    SIZES['water_door'] = (TILE_SIZE * (1 - WALL_PER), TILE_SIZE)
    SIZES['g_wall'] = (TILE_SIZE, int(WALL_PER * TILE_SIZE))
    SIZES['v_wall'] = (int(WALL_PER * TILE_SIZE), TILE_SIZE)
    SIZES['fire_lake'] = (TILE_SIZE, int(WALL_PER * TILE_SIZE))
    SIZES['water_lake'] = (TILE_SIZE, int(WALL_PER * TILE_SIZE))

    for i in range(width):
        Wall((i * TILE_SIZE + SIZES['v_wall'][0], 0), SIZES['g_wall'])

    for i in range(height // 2):
        Wall((0, i * TILE_SIZE + SIZES['g_wall'][1]), SIZES['v_wall'])
        Wall((width * TILE_SIZE + SIZES['v_wall'][0], i * TILE_SIZE + SIZES['g_wall'][1]), SIZES['v_wall'])

    for i in range(int(level[0][0])):
        for q in range(2):
            n = i * 4 + q * 2

            for j in range(2, width + 2):
                if level[n + 1][j] == SIGNS['wall']:
                    a = []
                    if j + 1 < width + 2 and level[n + 1][j + 1] == SIGNS['free']:
                        a.append(TYPE_BORD['right'])
                    if j - 1 > 1 and level[n + 1][j - 1] == SIGNS['free']:
                        a.append(TYPE_BORD['left'])
                    Wall((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE,
                          SIZES['g_wall'][1] + (i * 2 + q + 1) * TILE_SIZE), SIZES['g_wall'], a)
                elif level[n + 1][j] == SIGNS['fire_lake']:
                    FireLake((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE,
                              SIZES['g_wall'][1] + (i * 2 + q + 1) * TILE_SIZE), SIZES['fire_lake'])
                elif level[n + 1][j] == SIGNS['water_lake']:
                    WaterLake((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE,
                               SIZES['g_wall'][1] + (i * 2 + q + 1) * TILE_SIZE), SIZES['water_lake'])

            for j in range(2, width + 2):
                if level[n][j] == SIGNS['fire_door']:
                    FireDoor((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE + (TILE_SIZE - SIZES['fire_door'][0]) / 2,
                              SIZES['g_wall'][1] + (i * 2 + q) * TILE_SIZE + TILE_SIZE - SIZES['fire_door'][1]),
                             SIZES['fire_door'])
                elif level[n][j] == SIGNS['water_door']:
                    WaterDoor((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE + (TILE_SIZE - SIZES['water_door'][0]) / 2,
                               SIZES['g_wall'][1] + (i * 2 + q) * TILE_SIZE + TILE_SIZE - SIZES['water_door'][1]),
                              SIZES['water_door'])
                elif level[n][j] == SIGNS['static_stone']:
                    StaticStone((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE + (TILE_SIZE - SIZES['static_stone'][0]) / 2,
                                 SIZES['g_wall'][1] + (i * 2 + q) * TILE_SIZE + TILE_SIZE - SIZES['static_stone'][
                                     1] + 2),
                                SIZES['static_stone'])
                elif level[n][j] == SIGNS['dynamic_stone']:
                    DynamicStone(
                        (SIZES['v_wall'][0] + (j - 2) * TILE_SIZE + (TILE_SIZE - SIZES['dynamic_stone'][0]) / 2,
                         SIZES['g_wall'][1] + (i * 2 + q) * TILE_SIZE + TILE_SIZE - SIZES['dynamic_stone'][1] + 2),
                        SIZES['dynamic_stone'])
                elif level[n][j] == SIGNS['fire']:
                    fire = Fire((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE + (TILE_SIZE - SIZES['fire'][0]) / 2,
                                 SIZES['g_wall'][1] + (i * 2 + q) * TILE_SIZE + TILE_SIZE - SIZES['fire'][1] + 2),
                                SIZES['fire'])
                elif level[n][j] == SIGNS['water']:
                    water = Water((SIZES['v_wall'][0] + (j - 2) * TILE_SIZE + (TILE_SIZE - SIZES['water'][0]) / 2,
                                   SIZES['g_wall'][1] + (i * 2 + q) * TILE_SIZE + TILE_SIZE - SIZES['water'][1] - 100),
                                  SIZES['water'])


def main():
    global all_sprites, v_borders, g_borders, static_stones, dynamic_stones, fire_lakes, water_lakes, fire_doors, water_doors, walls
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1] + BUTTON_PLACE))
    clock = pygame.time.Clock()
    screen.fill((150, 150, 150))

    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    v_borders = pygame.sprite.Group()
    g_borders = pygame.sprite.Group()
    static_stones = pygame.sprite.Group()
    dynamic_stones = pygame.sprite.Group()
    fire_lakes = pygame.sprite.Group()
    water_lakes = pygame.sprite.Group()
    fire_doors = pygame.sprite.Group()
    water_doors = pygame.sprite.Group()

    water = None
    fire = None

    load_level('1.txt')

    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((150, 150, 150))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
