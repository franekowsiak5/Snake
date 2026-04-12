import pygame
import sys


pygame.init()
pygame.font.init()

width,height=500,500


font = pygame.font.SysFont('Arial', 32)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake")

class Level:
    def __init__(self,amount_w,amount_h):
        self.amount_w = amount_w
        self.amount_h = amount_h
    
    # rysowanie planszy,
    # jeżeli kwadrawty nie wyhodzą kwadratowe- rysuje biały margines po lewej i prawej
    def draw_map(self):
        size_h = int(height/self.amount_h)
        size_w = int(width/self.amount_w)
        self.margin_h, self.margin_w = 0,0
        
        # adding margins
        if size_h > size_w:
            size_h = size_w
            self.margin_h = (height - (size_h * self.amount_h)) / 2
            if size_w < width/self.amount_w:
                self.margin_w += (width - (size_w * self.amount_w)) / 2
        else:
            size_w = size_h
            self.margin_w = (width - (size_w * self.amount_w)) / 2
            if size_h < height/self.amount_h:
                self.margin_h += (height - (size_h * self.amount_h)) / 2
        
        for y in range(self.amount_h):
            for x in range(self.amount_w):
                if (x+y) % 2 == 0:
                    pygame.draw.rect(screen,(0,255,127),((size_w * x) + self.margin_w, (size_h * y) + self.margin_h ,size_w, size_h)) 
                else:
                    pygame.draw.rect(screen,(60,179,113),((size_w * x) + self.margin_w, (size_h * y) + self.margin_h, size_w, size_h))

Level1= Level(10,10)



while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("klik")
                

    screen.fill((128,128,128))
    
    Level1.draw_map()




    pygame.display.flip()
