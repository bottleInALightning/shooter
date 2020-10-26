import pygame
pygame.init()

class Wall:
    def __init__(self,x,y,var,collision,screen):
        self.rect=pygame.Rect(x,y,32,32)
        self.image=pygame.image.load("./images/temp_wall_image.png")
        self.var=var
        
        self.collision=collision#True or false

        
        self.screen=screen
    def show(self):
        

        
        #print(f"real-pos:{self.rect.x}, {self.rect.y} ")
        #print(f"display-pos:{self.display_pos.x},{self.display_pos.y} ")
        if self.rect.x-self.var.camera_scrolling[0] >-40 and self.rect.x-self.var.camera_scrolling[0]<self.var.window_width+40:
            if self.rect.y-self.var.camera_scrolling[1] >-40 and self.rect.y-self.var.camera_scrolling[1]<self.var.window_height+40:
 
                self.screen.blit(self.image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
   
    def update(self):
       
        self.show()