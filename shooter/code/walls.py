import pygame
pygame.init()

class Wall:
    def __init__(self,x,y,var,collision,screen):
        self.rect=pygame.Rect(x,y,32,32)
        self.image=pygame.image.load("./images/temp_wall_image.png")
        self.var=var
        
        self.collision=collision#True or false

        self.display_pos=pygame.Vector2(self.rect.x,self.rect.y)
        self.screen=screen
    def show(self):
        

        temp_pos_x=self.display_pos.x+self.var.camera_scrolling[0]#-#self.var.camera_scrolling[0]
        temp_pos_y=self.display_pos.y+self.var.camera_scrolling[1]#-#self.var.camera_scrolling[1]

        #print(f"real-pos:{self.rect.x}, {self.rect.y} ")
        #print(f"display-pos:{self.display_pos.x},{self.display_pos.y} ")
        self.screen.blit(self.image,(temp_pos_x,temp_pos_y))
    '''def update_pos(self):
        self.rect.x-=self.var.camera_scrolling[0]
        self.rect.y-=self.var.camera_scrolling[1]
        pass'''
    def update(self):
        #self.update_pos()
        self.show()