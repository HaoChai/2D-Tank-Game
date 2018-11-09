import pygame
pygame.init()

screenWidth = 900
screenHeight = 600
largeText = pygame.font.Font('freesansbold.ttf', 115)
smallText = pygame.font.Font("freesansbold.ttf", 20)
positions = [1, 2, 3, 4]
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("2D Tank Game")

# set background here
# bg = pygame.image.load(' [backgroundfile.png] ')

def text_objects(text, font):
        t_surface = font.render(text, True, (0,0,0))
        return t_surface, t_surface.get_rect()

def green_button(message, x, y, width, height):
        pointer = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > pointer[0] > x and y + height > pointer[1] > y:
                pygame.draw.rect(win, (0, 255, 0), (x, y, width, height))
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
                pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
                if click[0] == 1:
                        pygame.quit()
        else:
                pygame.draw.rect(win, (200, 0, 0), (x, y, width, height))
        t_surface, t_rect = text_objects(message, smallText)
        t_rect.center = (x + width/2, y + height/2)
        win.blit(t_surface, t_rect)

def game_intro():
        intro = True

        while intro:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                win.fill((255,255,255))



                
                t_surface , t_rect = text_objects("Tank Game", largeText)
                t_rect.center = ((screenWidth/2), (screenHeight/2))
                win.blit(t_surface, t_rect)

                green_button("START", 165, 400, 200, 100)
                red_button("QUIT", 550, 400, 200, 100)

                pygame.display.update()
                
                pygame.time.Clock().tick(15)
	
# Main Loop
def main_loop():
        # character traits
        # needs to be OOP-ed
        char = pygame.image.load('Tank_Turret.png')
        char_rect = char.get_rect()
        x = screenWidth/2
        y = screenHeight/2
        prev_char_pos = 1
        cur_char_pos = 1
        width = 51 
        height = 53
        vel = 10

        run = True
        while run:
                pygame.time.delay(100)

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                run = False

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
                # also need to change what forward and backwards modify when rotated
                if keys[pygame.K_w] and y > 0:
                        if cur_char_pos == 1:        
                                y -= vel
                        if cur_char_pos == 2:
                                x += vel
                        if cur_char_pos == 3:
                                y += vel
                        if cur_char_pos == 4:
                                x -= vel
                if keys[pygame.K_s] and y < screenHeight - height:
                        if cur_char_pos == 1:
                                y += vel
                        if cur_char_pos == 2:
                                x -= vel
                        if cur_char_pos == 3:
                                y -= vel
                        if cur_char_pos == 4:
                                x += vel
                #get rid of win.fill when background line is added
                win.fill((0,0,0))
                #background needs to be updated here, after its set at the top
                # win.blit(bg, (0,0))
                
                win.blit(char, (x, y))
                pygame.display.update()

game_intro()
main_loop()
pygame.quit()
