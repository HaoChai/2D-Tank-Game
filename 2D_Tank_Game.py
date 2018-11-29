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
width = 51
height = 53
player1_sprite = 'Tank_Turret.png'
player2_sprite = 'Red_Tank_Turret.png'

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# positions
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


# reference: https://www.pygame.org/project-Rect+Collision+Response-1061-.html
class Tank:
    def __init__(self, image):
        self.rect = pygame.Rect(width, width, height, height)
        self.char = pygame.image.load(image)
        self.vel = 10
        self.prev_char_pos = UP
        self.cur_char_pos = UP

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


class Wall:
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], boxSize, boxSize)


# set background here
bg = pygame.image.load("background.jpg")

walls = []
player1 = Tank(player1_sprite)
player2 = Tank(player2_sprite)
fpsClock = pygame.time.Clock()

level = [
    "WWWWWWWWWWWWWWW",
    "W             W",
    "W             W",
    "W             W",
    "W1           2W",
    "W             W",
    "W             W",
    "W             W",
    "W             W",
    "WWWWWWWWWWWWWWW"
]


def main():
    setup_level()
    game_intro()
    main_loop()
    terminate()


def setup_level():
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "1":
                player1.rect.x = x
                player1.rect.y = y
            if col == "2":
                player2.rect.x = x
                player2.rect.y = y
            x += boxSize
        y += boxSize
        x = 0


def terminate():
    pygame.quit()
    sys.exit()


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        win.fill(BLUE)
        t_surface, t_rect = text_objects("Tank Game", largeText)
        t_rect.center = ((screenWidth/2), (screenHeight/2))
        win.blit(t_surface, t_rect)

        green_button("START", 165, 400, 200, 100)
        red_button("QUIT", 550, 400, 200, 100)

        pygame.display.update()
        fpsClock.tick(FPS)


def main_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

        draw_grid()
        # draw walls
        for wall in walls:
            pygame.draw.rect(win, RED, wall.rect)
        # draw player
        player1.draw_tank()
        player2.draw_tank()
        pygame.display.update()
        fpsClock.tick(FPS)


def text_objects(text, font):
    t_surface = font.render(text, True, WHITE)
    return t_surface, t_surface.get_rect()


def green_button(message, x, y, width, height):
    pointer = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > pointer[0] > x and y + height > pointer[1] > y:
        pygame.draw.rect(win, GREEN, (x, y, width, height))
        if click[0] == 1:
            main_loop()
            pygame.quit()
    else:
        pygame.draw.rect(win, (0, 200, 0), (x, y, width, height))
    t_surface, t_rect = text_objects(message, smallText)
    t_rect.center = (x + width/2, y + height/2)
    win.blit(t_surface, t_rect)


def red_button(message, x, y, width, height):
    pointer = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > pointer[0] > x and y + height > pointer[1] > y:
        pygame.draw.rect(win, RED, (x, y, width, height))
        if click[0] == 1:
            pygame.quit()
    else:
        pygame.draw.rect(win, (200, 0, 0), (x, y, width, height))
    t_surface, t_rect = text_objects(message, smallText)
    t_rect.center = (x + width/2, y + height/2)
    win.blit(t_surface, t_rect)


def draw_grid():
    for i in range(0, screenWidth, boxSize):
        pygame.draw.line(win, BLUE, (i, 0), (i, screenHeight))
    for j in range(0, screenHeight, boxSize):
        pygame.draw.line(win, BLUE, (0, j), (screenWidth, j))


if __name__ == "__main__":
    main()
