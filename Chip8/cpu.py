from display import Display
from secrets import randbelow


class Cpu:
    keyboard = [False]*16
    memory = [0]*4096
    register = [0]*16
    stack = [0]*16
    index = 0
    delayTimer = 0
    soundTimer = 0
    programCounter = 512
    stackPointer = -1
    quit = False
    fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
           0x20, 0x60, 0x20, 0x20, 0x70, # 1
           0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
           0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
           0x90, 0x90, 0xF0, 0x10, 0x10, # 4
           0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
           0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
           0xF0, 0x10, 0x20, 0x40, 0x40, # 7
           0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
           0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
           0xF0, 0x90, 0xF0, 0x90, 0x90, # A
           0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
           0xF0, 0x80, 0x80, 0x80, 0xF0, # C
           0xE0, 0x90, 0x90, 0x90, 0xE0, # D
           0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
           0xF0, 0x80, 0xF0, 0x80, 0x80  # F
           ]
    def __init__(self):
        self.display = Display()
        pass 

    def clear_keyboard(self):
        for i in range(16):
            self.keyboard[i] = False
        pass

    def clock_cycle(self):
        self.decrement_timers()
        self.opcode = self.memory[self.programCounter]<< 8 | self.memory[self.programCounter+1]
        regStr = ""
        i=0
        self.performOpcode(self.opcode)
        for reg in self.register:
            regStr += "V"+str(i)+":"+str(reg)+" "
            i +=1
        print(str(hex(self.opcode))+" "+str(self.programCounter)+" "+regStr+" DT:"+str(self.delayTimer)+" ST:"+str(self.soundTimer)+" i:"+str(self.index)+" SP:"+str(self.stackPointer))
        print("")
        self.increment_program_counter()
        pass

    def decrement_timers(self):
        if(self.delayTimer >0):
            self.delayTimer -=1
        if(self.soundTimer>0):
            self.soundTimer -=1
        pass

    def performOpcode(self, opcode):
        x = (self.opcode &   0x0F00)>>8
        y = (self.opcode &   0x00F0)>>4
        kk = self.opcode &  0x00FF
        nnn = self.opcode & 0x0FFF
        n = self.opcode &   0x000F
        if(opcode & 0xF000 == 0x0000):
            # 00E0 Clear Screen
            if(self.opcode == 0x00E0):
                self.display.clear_screen()
                pass
            #Return from subroutine
            elif(self.opcode == 0x00EE):
                self.programCounter = self.stack[self.stackPointer]
                self.stackPointer -= 1
                pass
            #0NNN jump to location
            elif(self.opcode & 0x0F00 != 0x0000):
                self.programCounter = nnn - 2
                pass
            pass
        #1NNN jump to location
        elif(opcode & 0xF000 == 0x1000):
            self.programCounter = nnn - 2
            pass
        #2NNN Put program copunter into stack jump to location
        elif(opcode & 0xF000 == 0x2000):
            self.stackPointer += 1
            self.stack[self.stackPointer] = self.programCounter
            self.programCounter = nnn - 2
            pass
        #3xkk Skip next intrustion if register x == value kk
        elif(opcode & 0xF000 == 0x3000):
            if(self.register[x]==kk):
                self.programCounter += 2
                pass
            pass
        #4xkk Skip next instruction if register x != value kk
        elif(opcode & 0xF000 == 0x4000):
            if(self.register[x]!=kk):
                self.programCounter +=2
                pass
            pass
        #5xy0 Skip next instruction if register x ==  register y
        elif(opcode & 0xF000 == 0x5000):
            if(self.register[x]==self.register[y]):
                self.programCounter +=2
                pass
            pass
        #6xkk Put value kk into register x
        elif(opcode & 0xF000 == 0x6000):
            self.register[x] = kk
            pass
        #7xkk Set register x to register x + kk
        elif(opcode & 0xF000 == 0x7000):
            self.register[x] = (self.register[x] + kk)&0xFF
            pass
        #8xy0 Store value in register y in register x
        elif(opcode & 0xF00F == 0x8000):
            self.register[x] = self.register[y]
            pass
        #8xy1 set register x to (register x|register y)
        elif(opcode & 0xF00F == 0x8001):
            self.register[x] = self.register[x] | self.register[y]
            pass
        #8xy2 set register x to (register x&register y)
        elif(opcode & 0xF00F == 0x8002):
            self.register[x] = self.register[x] & self.register[y]
            pass
        #8xy3 set register x to (register x XOR register y)
        elif(opcode & 0xF00F == 0x8003):
            self.register[x] = self.register[x] ^ self.register[y]
            pass
        #8xy4 set register x to (register x + register y)
        elif(opcode & 0xF00F == 0x8004):
            self.register[x] = self.register[x] + self.register[y]
            if self.register[x] > 0xFF:
                self.register[0xF] = 1
            else:
                self.register[0xF] = 0
            self.register[x] &= 0xFF
            pass
        #8xy5 set register x to (register x - register y)
        elif(opcode & 0xF00F == 0x8005):
            if(self.register[x]<self.register[y]):
                self.register[0xF]=0
            else:
                self.register[0xF]=1
            self.register[x] -=self.register[y]
            self.register[x] &= 0xFF  
        #8xy6 If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
        elif(opcode & 0xF00F == 0x8006):
            #if(self.register[x]%2 ==1):
             #   self.register[0xF] = 1
            #else:
             #   self.register[0xF] = 0
            self.register[0xF] = self.register[x] & 0x01
            self.register[x] = self.register[x] >> 1
        #8xy7 If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
        elif(opcode & 0xF00F == 0x8007):
            if(self.register[x]>self.register[y]):
                self.register[0xF]=0
            else:
                self.register[0xF]=1
            self.register[x] = self.register[y] -self.register[x]
            self.register[x] = self.register[x] & 0xFF 
        #8xyE If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
        elif(opcode & 0xF00F == 0x800E):
            self.register[0xF] = self.register[x] >>7
            self.register[x] = self.register[x] << 1
        #9xy0  Skip next instruction if Vx != Vy.
        elif(opcode & 0xF000 == 0x9000):
            if(self.register[x]!=self.register[y]):
                self.programCounter +=2
        #Annn  set index to nnn
        elif(opcode & 0xF000 == 0xA000):
            self.index = nnn
        #Bnnn jump to location nnn + value in register 0
        elif(opcode & 0xF000 == 0xB000):
            self.programCounter = nnn + self.register[0] -2
        #Cxkk random byte & kk put into register x
        elif(opcode &0xF000 == 0xC000):
            self.register[x] = randbelow(255) & kk
        #Dxyn  Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
        elif(opcode & 0xF000 == 0xD000):
            xcord = self.register[x] 
            ycord = self.register[y]
            height = n

            pixel = 0
            self.register[0xF] = 0
            
            for q in range(height):
                pixel = self.memory[self.index + q]
                for i in range(8):
                    value = pixel & 0b000001
                    collision = self.display.set_pixel(xcord+8-i,ycord+q,value)
                    if(collision):
                        self.register[0xF] = 1
                    pixel = pixel >> 1
        #Ex9E  Skip next instruction if key with the value of Vx is pressed.
        elif(opcode & 0xF0FF == 0xE09E):
            for key in self.keyboard:
                print(str(key)+" ")
            if(self.keyboard[self.register[x]]):
                self.programCounter +=2
            pass
        #ExA1  Skip next instruction if key with the value of Vx is not pressed.
        elif(opcode & 0xF0FF== 0xE0A1):
            for key in self.keyboard:
                print(str(key)+" ")
            if( self.keyboard[self.register[x]]==False):
                self.programCounter +=2
            pass
        #Fx07 Set register x to the value of the delay timer
        elif(opcode & 0xF0FF == 0xF007):
            self.register[x] = self.delayTimer
            pass
        #Fx0A WAit for a key to be pressed
        elif(opcode & 0xF0FF == 0xF00A):
            pressed = False
            for i in range(16):
                if(self.keyboard[i]):
                    self.register[x] = i
                    pressed = True
                    break
            if(not pressed):
                self.programCounter -=2
            pass
        #Fx15 Set delay timer
        elif(opcode & 0xF0FF == 0xF015):
            self.delayTimer = self.register[x]
            pass
        #Fx18 Set sound timer
        elif(opcode & 0xF0FF == 0xF018):
            self.soundTimer = self.register[x]
            pass
        #Fx1E add register x + index put avlue in index
        elif(opcode & 0xF0FF == 0xF01E):
            self.index = self.register[x] + self.index
            pass
        #Fx29 Set I = location of sprite for digit Vx.
        elif (opcode & 0xF0FF == 0xF029):
            self.index = self.register[x]*5
            pass
        #Fx33 Store BCD representation of Vx in memory locations I, I+1, and I+2.
        elif(opcode & 0xF0FF == 0xF033):
            self.memory[self.index] = self.register[x]//100
            self.memory[self.index+1] = (self.register[x]%100) // 10
            self.memory[self.index+2] = ((self.register[x]%100) %10)
            pass
        #Fx55  store registers 0 through x in memory starting at index
        elif(opcode & 0xF0FF == 0xF055):
            for i in range(x+1):
                self.memory[self.index + i] = self.register[i]
            pass
        #Fx65 Read registers V0 through Vx from memory starting at location I.
        elif(opcode & 0xF0FF == 0xF065):
            for i in range(x+1):
                self.register[i] =self.memory[self.index + i] 
            pass
        else:
            pass
        pass


    def increment_program_counter(self):
        if(self.programCounter + 2 < 4096):
            self.programCounter += 2
            pass
        else:
            self.quit = True
            pass
        pass

    def load_rom(self, fileName):
        with open(fileName, "rb") as f:
            byte = f.read()
            for i in range(len(byte)):
                self.memory[self.programCounter + i] = byte[i]
        for i in range(80):
            self.memory[i] = self.fonts[i]
        pass


