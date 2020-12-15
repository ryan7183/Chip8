import pygame
import random

def main():

    pygame.init()

    size = (640, 320)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Chip8")

    BLACK = ( 0, 0, 0)
    WHITE = ( 255, 255, 255)
    
    carryOn = True
    clock = pygame.time.Clock()
    while carryOn:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                  carryOn = False # Flag that we are done so we exit this loop

        screen.fill(WHITE)#Clear screen
        #Draw on screen
        
        for x in range(64):
            for y in range(32):
                if(bool(random.getrandbits(1))):
                    pygame.draw.rect(screen,WHITE,(x*10,y*10,10,10))
                else:
                    pygame.draw.rect(screen,BLACK,(x*10,y*10,10,10))

        pygame.display.flip()#Show screen

        clock.tick(60)
    pygame.quit()
    pass

main()
