import pygame
pygame.init()

screenWidth = 1600
screenHeight = 900

win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("2D Tank Game")

# set background here
# bg = pygame.image.load(' [backgroundfile.png] ')

# character traits
# needs to be OOP-ed
char = pygame.image.load('Tank_Turret.png')
char_rect = char.get_rect()
x = screenWidth/2
y = screenHeight/2
width = 128
height = 188
vel = 10

def reDrawWindow():
        #get rid of win.fill when background line is added
        win.fill((0,0,0))
        #background needs to be updated here
        # win.blit(bg, (0,0))
        
        win.blit(char, (x, y))
        pygame.display.update()
	
# Main Loop
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
        if keys[pygame.K_d] and x < screenWidth - width:
                char = pygame.transform.rotate(char, 270)
        # also need to change what forward and backwards modify when rotated
        if keys[pygame.K_w] and y > 0:
                y -= vel
        if keys[pygame.K_s] and y < screenHeight - height:
                y += vel

        reDrawWindow()
        
pygame.quit()
