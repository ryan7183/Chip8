import random

class Display:
    height = 32
    width = 64
    draw = False
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
        self.pixels = []
        for x in range(self.height):
            row = []
            for y in range(self.width):
                row.append(False)
            self.pixels.append(row)

    def clear_screen(self):
        for y in range(0,self.height):
            for x in range(0,self.width):
                self.pixels[y][x] = False
                pass
        pass

    def set_pixel(self,x,y,value):
        x=x-1
        
        if(x>=self.width):
            x= x%self.width
            pass
        if(y>=self.height):
            y = y%self.height
            pass
        ogPixel = self.pixels[y][x]
        self.pixels[y][x] ^= value
        if((ogPixel==True) and (self.pixels[y][x]==False)):
             collision = 1
        else:
             collision = 0
        self.draw=True
        return collision


