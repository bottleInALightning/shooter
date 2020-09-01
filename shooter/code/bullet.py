import pygame
from pygame.math import Vector2
import math
pygame.init()

class Bullet:
    def __init__(self,x,y,vel,screen,bul_speed,player,bul_index,var):#have to make it so bullets die after time or if they hit player or maybe object or out of bounds
        
        self.vel=vel
        self.time_limit=1
        self.w=5
        self.rect=pygame.Rect(x,y,self.w,self.w)
        self.screen=screen
        self.color=(150,70,200)
        self.speed=bul_speed
        self.player=player
        self.bul_index=bul_index
        self.var=var
    def show(self):
        pygame.draw.rect(self.screen,self.color,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1],self.w,self.w))
    
    def update_pos(self):
        self.rect.x+=self.vel.x*self.speed
        self.rect.y+=self.vel.y*self.speed

        

    def update(self):
        self.update_pos()
        self.show()
'''
        for i, item in enumerate(self.player.bullets):
            if item.bul_index == self.bul_index:
                self.player.bullets[i]=self
                print("update")
'''