import random
import sys
import pygame

pygame.init()
screenWidth = 900
screenHeight = 600
largeText = pygame.font.Font('freesansbold.ttf', 115)
smallText = pygame.font.Font("freesansbold.ttf", 20)
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("2D Tank Game")
boxSize = 60
assert screenWidth % boxSize == 0
assert screenHeight % boxSize == 0
boxWidth = int(screenWidth / boxSize)
boxHeight = int(screenHeight / boxSize)
FPS = 12
tankWidth = 51
tankHeight = 53
player1_sprite = 'Tank_Turret.png'
player2_sprite = 'Red_Tank_Turret.png'
item_sprites = [pygame.image.load("item1.png"), pygame.image.load("item2.png"), pygame.image.load("item3.png"),
                pygame.image.load("item4.png"), pygame.image.load("item5.png")]

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
DARK_GREEN = (0, 155, 0)
BLUE = (0, 0, 255)

# tank positions
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


class Timer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def time_diff(self):
        seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        seconds = round(seconds)
        return seconds

    def reset_timer(self):
        self.start_time = pygame.time.get_ticks()


class Button:
    def __init__(self, message, x, y, width, height, func, color, select_color):
        pointer = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > pointer[0] > x and y + height > pointer[1] > y:
            pygame.draw.rect(win, color, (x, y, width, height))
            if click[0] == 1:
                func()
        else:
            pygame.draw.rect(win, select_color, (x, y, width, height))
        t_surface, t_rect = text_objects(message, smallText)
        t_rect.center = (x + width/2, y + height/2)
        win.blit(t_surface, t_rect)


def text_objects(text, font):
    t_surface = font.render(text, True, WHITE)
    return t_surface, t_surface.get_rect()


# reference: https://www.pygame.org/project-Rect+Collision+Response-1061-.html
class Tank:
    def __init__(self, image, num):
        self.player_number = num
        self.rect = pygame.Rect(tankWidth, tankWidth, tankHeight, tankHeight)
        self.char = pygame.image.load(image)
        self.vel = 10
        self.prev_char_pos = UP
        self.cur_char_pos = UP
        self.timers = [Timer(), Timer(), Timer(), Timer(), Timer()]
        self.speed_up = False

    def move(self, x, y):
        if x != 0:
            self.move_axis(x, 0)
        if y != 0:
            self.move_axis(0, y)

    def move_axis(self, x, y):
        self.rect.x += x
        self.rect.y += y
        # check for wall collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if x > 0:
                    self.rect.right = wall.rect.left
                if x < 0:
                    self.rect.left = wall.rect.right
                if y > 0:
                    self.rect.bottom = wall.rect.top
                if y < 0:
                    self.rect.top = wall.rect.bottom

        # check for wall collision
        for box in boxes:
            if self.rect.colliderect(box.rect):
                if x > 0:
                    self.rect.right = box.rect.left
                if x < 0:
                    self.rect.left = box.rect.right
                if y > 0:
                    self.rect.bottom = box.rect.top
                if y < 0:
                    self.rect.top = box.rect.bottom

        # check player collision
        check_player = player2
        if self.player_number == 2:
            check_player = player1
        if self.rect.colliderect(check_player.rect):
            if x > 0:
                self.rect.right = check_player.rect.left
            if x < 0:
                self.rect.left = check_player.rect.right
            if y > 0:
                self.rect.bottom = check_player.rect.top
            if y < 0:
                self.rect.top = check_player.rect.bottom

        # check item collision
        for item in items:
            if self.rect.colliderect(item.rect):
                if item.item_type == 0 and item.spawned is True:
                    self.speed_up = True
                    self.timers[0].reset_timer()
                    self.vel = 16
                item.reset_item()

        self.power_up_handler()

    # times out power up and reset tank to default value
    def power_up_handler(self):
        if self.speed_up is True:
            if self.timers[0].time_diff() == 5:
                self.vel = 10
                self.speed_up = False

    def rotate_left(self):
        self.char = pygame.transform.rotate(self.char, 90)
        if self.prev_char_pos == UP:
            self.cur_char_pos = LEFT
        elif self.prev_char_pos == RIGHT:
            self.cur_char_pos = UP
        if self.prev_char_pos == DOWN:
            self.cur_char_pos = RIGHT
        if self.prev_char_pos == LEFT:
            self.cur_char_pos = DOWN
        self.prev_char_pos = self.cur_char_pos
        pygame.time.delay(150)

    def rotate_right(self):
        self.char = pygame.transform.rotate(self.char, 270)
        if self.prev_char_pos == UP:
            self.cur_char_pos = RIGHT
        if self.prev_char_pos == RIGHT:
            self.cur_char_pos = DOWN
        if self.prev_char_pos == DOWN:
            self.cur_char_pos = LEFT
        if self.prev_char_pos == LEFT:
            self.cur_char_pos = UP
        self.prev_char_pos = self.cur_char_pos
        pygame.time.delay(150)

    def move_up(self):
        if self.cur_char_pos == 1:
            self.move(0, self.vel * -1)
        if self.cur_char_pos == 2:
            self.move(self.vel, 0)
        if self.cur_char_pos == 3:
            self.move(0, self.vel)
        if self.cur_char_pos == 4:
            self.move(self.vel * -1, 0)

    def move_down(self):
        if self.cur_char_pos == 1:
            self.move(0, self.vel)
        if self.cur_char_pos == 2:
            self.move(self.vel * -1, 0)
        if self.cur_char_pos == 3:
            self.move(0, self.vel * -1)
        if self.cur_char_pos == 4:
            self.move(self.vel, 0)

    def draw_tank(self):
        pygame.draw.rect(win, WHITE, self.rect)
        win.blit(self.char, (self.rect.centerx - 25, self.rect.centery - 25))


class Item:
    def __init__(self, pos):
        items.append(self)
        self.item_type = random.randint(0, 4)
        self.sprite = item_sprites[self.item_type]
        self.rect = pygame.Rect(boxSize, boxSize, boxSize, boxSize)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timer = Timer()
        self.spawned = False
        self.cool_down = 5

    def draw_item(self):
        # draw item if it is set to spawn or when certain time has past
        if self.timer.time_diff() == self.cool_down or self.spawned is True:
            pygame.draw.rect(win, WHITE, self.rect)
            win.blit(self.sprite, (self.rect.x + 4, self.rect.y + 1))
            self.spawned = True

    def reset_item(self):
        self.item_type = random.randint(0, 4)
        self.sprite = item_sprites[self.item_type]
        self.timer.reset_timer()
        self.spawned = False
        self.cool_down = random.randint(5, 15)


class Wall:
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], boxSize, boxSize)


class Box:
    def __init__(self, pos):
        boxes.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], boxSize, boxSize)
        self.hit_point = 2

    def draw_box(self):
        if self.hit_point == 0:
            boxes.remove(self)
        elif self.hit_point == 1:
            pygame.draw.rect(win, GREEN, self.rect)
        elif self.hit_point == 2:
            pygame.draw.rect(win, DARK_GREEN, self.rect)


# set background here
bg = pygame.image.load("background.jpg")

walls = []
boxes = []
items = []
player1 = Tank(player1_sprite, 1)
player2 = Tank(player2_sprite, 2)
fpsClock = pygame.time.Clock()

level = []

level1 = [
    "WWWWWWWWWWWW",
    "W          W",
    "W       W  W",
    "W       W 2W",
    "W1 W       W",
    "W  W       W",
    "W          W",
    "WWWWWWWWWWWW"
]

level2 = [
    "WWWWWWWWWWWWWWW",
    "W             W",
    "W             W",
    "W    W   W    W",
    "W1    I I     W",
    "W      I     2W",
    "W    W   W    W",
    "W             W",
    "W             W",
    "WWWWWWWWWWWWWWW"
]

level3 = [
    "WWWWWWWWWWWWWWW",
    "W    B   B    W",
    "W  B  B B  B  W",
    "W    B   B    W",
    "W1 B  B B  B  W",
    "W    B   B   2W",
    "W  B  B B  B  W",
    "W    B   B    W",
    "W  B  B B  B  W",
    "WWWWWWWWWWWWWWW"
]


def main():
    game_intro()
    terminate()


def start_game():
    setup_level()
    main_loop()
    terminate()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                intro = False
        win.fill(BLUE)
        t_surface, t_rect = text_objects("Tank Game", largeText)
        t_rect.center = ((screenWidth/2), (screenHeight/2))
        win.blit(t_surface, t_rect)
        # create buttons
        Button("START", 165, 400, 200, 100, select_level, RED, LIGHT_RED)
        Button("QUIT", 550, 400, 200, 100, terminate, GREEN, LIGHT_GREEN)

        pygame.display.update()
        fpsClock.tick(FPS)


def select_level():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        win.fill(BLUE)
        t_surface, t_rect = text_objects("Select A Level", largeText)
        t_rect.center = ((screenWidth/2), (screenHeight/2 - 100))
        win.blit(t_surface, t_rect)
        # create buttons
        Button("Level One", 165, 300, 200, 100, setup_level_one, GREEN, LIGHT_GREEN)
        Button("Level Two", 550, 300, 200, 100, setup_level_two, GREEN, LIGHT_GREEN)
        Button("Level Three", 356, 450, 200, 100, setup_level_three, GREEN, LIGHT_GREEN)

        pygame.display.update()
        fpsClock.tick(FPS)


def setup_level_one():
    global boxSize, level, level1
    boxSize = 75
    level = level1
    start_game()


def setup_level_two():
    global boxSize, level, level2
    boxSize = 60
    level = level2
    start_game()


def setup_level_three():
    global boxSize, level, level3
    boxSize = 60
    level = level3
    start_game()


def setup_level():
    x = y = 0
    for row in level:
        for col in row:
            # setup walls
            if col == "W":
                Wall((x, y))
            # setup player 1
            if col == "1":
                player1.rect.x = x
                player1.rect.y = y
            # setup player 2
            if col == "2":
                player2.rect.x = x
                player2.rect.y = y
            # setup items
            if col == "I":
                Item((x, y))
            if col == "B":
                Box((x, y))
            x += boxSize
        y += boxSize
        x = 0


def terminate():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def main_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()

        # First Player Programming
        if keys[pygame.K_a]:
            player1.rotate_left()
        if keys[pygame.K_d]:
            player1.rotate_right()
        # also need to change what forward and backwards modify when rotated
        if keys[pygame.K_w]:
            player1.move_up()
        if keys[pygame.K_s]:
            player1.move_down()

        # second player programming
        if keys[pygame.K_LEFT]:
            player2.rotate_left()
        if keys[pygame.K_RIGHT]:
            player2.rotate_right()
        # also need to change what forward and backwards modify when rotated
        if keys[pygame.K_UP]:
            player2.move_up()
        if keys[pygame.K_DOWN]:
            player2.move_down()
        # end second player programming

        # get rid of win.fill when background line is added
        win.fill(WHITE)
        # background needs to be updated here, after its set at the top
        win.blit(bg, (0, 0))

        # draw grid
        draw_grid()
        # draw walls
        for wall in walls:
            pygame.draw.rect(win, RED, wall.rect)
        for box in boxes:
            box.draw_box()
        # draw player
        player1.draw_tank()
        player2.draw_tank()
        # draw item
        for item in items:
            item.draw_item()

        pygame.display.update()
        fpsClock.tick(FPS)


def draw_grid():
    for i in range(0, screenWidth, boxSize):
        pygame.draw.line(win, BLUE, (i, 0), (i, screenHeight))
    for j in range(0, screenHeight, boxSize):
        pygame.draw.line(win, BLUE, (0, j), (screenWidth, j))


if __name__ == "__main__":
    main()
