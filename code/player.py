import pygame
from pygame.math import Vector2
import math
from code.bullet import Bullet
from pygame import mixer

pygame.init()
class Player:

    def __init__(self,x,y,w,h,index,screen,):
        pygame.mixer.init(44100, -16,2,1024)
        self.rect=pygame.Rect(x,y,w,h)
        self.screen=screen
        self.image=pygame.image.load("./images/bluePlayer.png")
        self.rotatedImage=self.image
        self.angle=0
        
        self.velocity=pygame.Vector2(0,0)
        self.speed=2
        self.bullet_speed=10
        self.shoot_timer=0
        self.bullets=[]
        self.bul_counter=0
        self.shoot_sound=mixer.Sound("./sfx/shoot_sound.wav")
        self.sound_channel=pygame.mixer.find_channel(True)
        self.sound_channel.set_volume(0.0)
        self.alive=True
    def load(self):
        self.img=pygame.transform.scale(self.image,(self.rect.w,self.rect.h))
    def show(self):
        if self.alive:
            self.screen.blit(self.rotatedImage,(self.rect.x,self.rect.y))
       
    
    
    def check_move(self,event):
       
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                self.velocity.y+=-self.speed
            if event.key==pygame.K_s:
                self.velocity.y+=self.speed
            if event.key==pygame.K_a:
                self.velocity.x+=-self.speed
            if event.key==pygame.K_d:
                self.velocity.x+=self.speed
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                self.velocity.y=0
            if event.key==pygame.K_s:
                self.velocity.y=0
            if event.key==pygame.K_a:
                self.velocity.x=0
            if event.key==pygame.K_d:
                self.velocity.x=0
        else:
            if not( self.velocity.x==0 and self.velocity.y==0):
                self.velocity.x=0
                self.velocity.y=0#going to make this smooth down to zero, not just bam zero 
        
    def rot_center(self):
        """rotate an image while keeping its center and size"""
        orig_rect=self.rect
        image=self.image
        angle=360-self.angle-90
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        
        self.rotatedImage=rot_image
    def posToAngle(self):
        from pygame import Vector2
        import math
        import pygame
        mouse_pos=Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        playerPos=Vector2(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2)
        difference =Vector2(mouse_pos-playerPos)

        rotation_z=math.atan2(difference.y,difference.x)
       
        self.angle=360-(180 / math.pi) * -math.atan2(difference.y, difference.x)
   

    def update(self):
        self.rect.x+=self.velocity.x*self.speed
        self.rect.y+=self.velocity.y*self.speed
        self.posToAngle()
        self.rot_center()
        self.update_bullets()
        
        self.show()
        
    def shoot(self,event):
        
        if event.type==pygame.MOUSEBUTTONDOWN:
            angle=math.radians(self.angle)
            bulletVel=Vector2(math.cos(angle),math.sin(angle))

            self.bullets.append(Bullet(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,bulletVel,self.screen,self.bullet_speed,self,self.bul_counter))
            self.bul_counter+=1
            self.sound_channel.play(self.shoot_sound)
    def update_bullets(self):
        for i in self.bullets:
            i.update()
    def get_distance_to_closest_enemy(self,enemies):
        import math
        closest_dist=100000
        for i in enemies:
            #i=enemy
            dist_to_enemy=math.sqrt(((self.rect.x-i.rect.x)**2)+((self.rect.y-i.rect.y)**2))
            if abs(dist_to_enemy)<closest_dist:
                closest_dist=dist_to_enemy
        return closest_dist
    def check_dead(self,enemies):
        if self.get_distance_to_closest_enemy(enemies)<30:
            self.alive=False
            print("You are dead!!!!")
        