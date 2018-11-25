import sys
import pygame

pygame.init()
screenWidth = 900
screenHeight = 600
largeText = pygame.font.Font('freesansbold.ttf', 115)
smallText = pygame.font.Font("freesansbold.ttf", 20)
positions = [1, 2, 3, 4]
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("2D Tank Game")
boxSize = 75
assert screenWidth % boxSize == 0
assert screenHeight % boxSize == 0
boxWidth = int(screenWidth / boxSize)
boxHeight = int(screenHeight / boxSize)
FPS = 12
fpsClock = pygame.time.Clock()
width = 51
height = 53

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# reference: https://www.pygame.org/project-Rect+Collision+Response-1061-.html
class Player:

    def __init__(self):
        self.rect = pygame.Rect(width, width, height, height)
        self.rect.center = (screenWidth/2, screenHeight/2)

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


class Wall:
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], boxSize, boxSize)


# set background here
bg = pygame.image.load("background.jpg")

walls = []
player = Player()

level = [
    "WWWWWWWWWWWW",
    "W          W",
    "W          W",
    "W          W",
    "W          W",
    "W          W",
    "W          W",
    "WWWWWWWWWWWW"
]


def main():
    setup_wall()
    game_intro()
    main_loop()
    terminate()


def setup_wall():
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
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


# Main Loop
def main_loop():
    # character traits
    # needs to be OOP-ed
    char = pygame.image.load('Tank_Turret.png')
    x = screenWidth/2
    y = screenHeight/2
    prev_char_pos = 1
    cur_char_pos = 1
    vel = 10

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()

        # may have to write our own rotate functions. transform.rotate doesn't
        # work well with anything small than 90 degrees.
        if keys[pygame.K_a] and x > 0:
            char = pygame.transform.rotate(char, 90)
            if prev_char_pos == 1:
                cur_char_pos = 4
            if prev_char_pos == 2:
                cur_char_pos = 1
            if prev_char_pos == 3:
                cur_char_pos = 2
            if prev_char_pos == 4:
                cur_char_pos = 3
            prev_char_pos = cur_char_pos
            pygame.time.delay(150)
        if keys[pygame.K_d] and x < screenWidth - width:
            char = pygame.transform.rotate(char, 270)
            if prev_char_pos == 1:
                cur_char_pos = 2
            if prev_char_pos == 2:
                cur_char_pos = 3
            if prev_char_pos == 3:
                cur_char_pos = 4
            if prev_char_pos == 4:
                cur_char_pos = 1

            prev_char_pos = cur_char_pos
            pygame.time.delay(150)
        # also need to change what forward and backwards modify when rotated
        if keys[pygame.K_w]:
            if cur_char_pos == 1:
                y -= vel
                player.move(0, vel * -1)
            if cur_char_pos == 2:
                x += vel
                player.move(vel, 0)
            if cur_char_pos == 3:
                y += vel
                player.move(0, vel)
            if cur_char_pos == 4:
                x -= vel
                player.move(vel * -1, 0)
        if keys[pygame.K_s]:
            if cur_char_pos == 1:
                y += vel
                player.move(0, vel)
            if cur_char_pos == 2:
                x -= vel
                player.move(vel * -1, 0)
            if cur_char_pos == 3:
                y -= vel
                player.move(0, vel * -1)
            if cur_char_pos == 4:
                x += vel
                player.move(vel, 0)

        # check for screen bound in case wall collision doesn't work
        if x <= -10:
            x = 0
        if y <= -10:
            y = 0
        if x >= screenWidth - width:
            x = screenWidth - width
        if y >= screenHeight - height:
            y = screenHeight - height

        # get rid of win.fill when background line is added
        win.fill(WHITE)
        # background needs to be updated here, after its set at the top
        win.blit(bg, (0, 0))

        draw_grid()
        # draw walls
        for wall in walls:
            pygame.draw.rect(win, RED, wall.rect)
        # draw hit box
        pygame.draw.rect(win, WHITE, player.rect)
        # draw character sprite
        win.blit(char, (player.rect.centerx - 25, player.rect.centery - 25))
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
