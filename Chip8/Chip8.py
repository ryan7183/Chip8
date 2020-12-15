import pygame
from cpu import Cpu
import os

def main(fileName):
    
    cpu = Cpu()
    cpu.load_rom(fileName)
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
            #cpu.clear_keyboard()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cpu.keyboard[0] = True
                if event.key == pygame.K_2:
                    cpu.keyboard[1] = True
                if event.key == pygame.K_3:
                    cpu.keyboard[2] = True
                if event.key == pygame.K_4:
                    cpu.keyboard[3] = True
                if event.key == pygame.K_q:
                    cpu.keyboard[4] = True
                if event.key == pygame.K_w:
                    cpu.keyboard[5] = True
                if event.key == pygame.K_e:
                    cpu.keyboard[6] = True
                if event.key == pygame.K_r:
                    cpu.keyboard[7] = True
                if event.key == pygame.K_a:
                    cpu.keyboard[8] = True
                if event.key == pygame.K_s:
                    cpu.keyboard[9] = True
                if event.key == pygame.K_d:
                    cpu.keyboard[10] = True
                if event.key == pygame.K_f:
                    cpu.keyboard[11] = True
                if event.key == pygame.K_z:
                    cpu.keyboard[12] = True
                if event.key == pygame.K_x:
                    cpu.keyboard[13] = True
                if event.key == pygame.K_c:
                    cpu.keyboard[14] = True
                if event.key == pygame.K_v:
                    cpu.keyboard[15] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    cpu.keyboard[0] = False
                if event.key == pygame.K_2:
                    cpu.keyboard[1] = False
                if event.key == pygame.K_3:
                    cpu.keyboard[2] = False
                if event.key == pygame.K_4:
                    cpu.keyboard[3] = False
                if event.key == pygame.K_q:
                    cpu.keyboard[4] = False
                if event.key == pygame.K_w:
                    cpu.keyboard[5] = False
                if event.key == pygame.K_e:
                    cpu.keyboard[6] = False
                if event.key == pygame.K_r:
                    cpu.keyboard[7] = False
                if event.key == pygame.K_a:
                    cpu.keyboard[8] = False
                if event.key == pygame.K_s:
                    cpu.keyboard[9] = False
                if event.key == pygame.K_d:
                    cpu.keyboard[10] = False
                if event.key == pygame.K_f:
                    cpu.keyboard[11] = False
                if event.key == pygame.K_z:
                    cpu.keyboard[12] = False
                if event.key == pygame.K_x:
                    cpu.keyboard[13] = False
                if event.key == pygame.K_c:
                    cpu.keyboard[14] = False
                if event.key == pygame.K_v:
                    cpu.keyboard[15] = False
                pass
        # Do clock cycle
        cpu.clock_cycle()    
        if(cpu.quit):
            pygame.quit()
            return
        screen.fill(WHITE)#Clear screen
        #Draw on screen
        if cpu.display.draw:
            cpu.display.draw=False
            pixels = cpu.display.pixels
            for x in range(64):
                for y in range(32):
                    if(pixels[y][x]):
                        pygame.draw.rect(screen,WHITE,(x*10,y*10,10,10))
                    else:
                        pygame.draw.rect(screen,BLACK,(x*10,y*10,10,10))
            pygame.display.flip()#Show screen

        clock.tick(60)
    pygame.quit()
    pass

fileName = input("ROM file name: ")
#fileName = "c8_test.c8"#"Brick (Brix hack, 1990).ch8"#"test_opcode.ch8"
main(fileName)