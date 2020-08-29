import pygame 
import random
pygame.init()

class zombie_enemy:
    def __init__(self,screen,x,y,w,h):
        self.screen=screen
        self.rect=pygame.Rect(x,y,w,h)
        self.hitbox=self.rect
        #self.img=pygame.image.load("/home/lars/Desktop/PyWeekTraining/shooter/images/FLEnemy1.png")
       
        self.dead=False
        self.movement_vel=pygame.Vector2(1,0)
        self.movement_acc=pygame.Vector2()
        self.angle=0
        self.speed=2

        self.sound_channel=pygame.mixer.find_channel(True)
        self.sound_channel.set_volume(0.8)
        self.die_sound=pygame.mixer.Sound("./sfx/zombie_enemy_die_sound.wav")

        
        try:
            self.MLImages=[pygame.image.load("./images/MLImage1.png"),pygame.image.load("./images/MLImage2.png")]
            self.MDImages=[pygame.image.load("./images/MDImage1.png"),pygame.image.load("./images/MDImage2.png")]
            self.MRImages=[pygame.image.load("./images/MRImage1.png"),pygame.image.load("./images/MRImage2.png")]
        except:
            print("Image loading error, you must be in the same directory as __main__.py for it to work you moron")
        self.MLImages=[pygame.transform.scale(i,(self.rect.w,self.rect.h)) for i in self.MLImages]
        self.MDImages=[pygame.transform.scale(i,(self.rect.w,self.rect.h)) for i in self.MDImages]
        self.MRImages=[pygame.transform.scale(i,(self.rect.w,self.rect.h)) for i in self.MRImages]

    def show(self,frame):
        #pygame.draw.rect(self.screen,(20,20,20),self.rect)
        if not self.dead:
            if self.movement_vel.x<0:
                if frame==0:
                    self.screen.blit(self.MLImages[0],(self.rect.x,self.rect.y))
                    
                elif frame==1:
                    self.screen.blit(self.MLImages[1],(self.rect.x,self.rect.y))
                else:
                    print("frame erro index out of range")
            elif self.movement_vel.y>0:
                if frame==0:
                    self.screen.blit(self.MDImages[0],(self.rect.x,self.rect.y))
                    
                elif frame==1:
                    self.screen.blit(self.MDImages[1],(self.rect.x,self.rect.y))
                else:
                    print("frame erro index out of range")
            elif self.movement_vel.x>0:
                if frame==0:
                    self.screen.blit(self.MRImages[0],(self.rect.x,self.rect.y))
                    
                elif frame==1:
                    self.screen.blit(self.MRImages[1],(self.rect.x,self.rect.y))
                else:
                    print("frame erro index out of range")
    def check_shot(self,player):
       #self is the zombie
        #print("len bullets {}".format(len(player.bullets)))
        try:
            for i in range(len(player.bullets)):#somehow only works if two bullets hit
                #print("cur bullet {}".format(i))
                if self.hitbox.colliderect(player.bullets[i].rect):
                    player.bullets.remove(player.bullets[i])

                    print("I dead")
                    self.dead=True
                    self.sound_channel.play(self.die_sound)
                    self.dead_animation()
                    
                    self.respawn()
                    
        except:
            print("list index out of range Error")
    def update_pos(self):
        self.rect.x+=self.movement_vel.x
        self.rect.y+=self.movement_vel.y

    def respawn(self):
        if self.dead==True:
            self.rect.x=random.randint(300,600)
            self.rect.y=random.randint(100,500)
            
            self.dead=False


    def rot_to_player(self,player):
        from pygame import Vector2
        import math
        import pygame
        player_pos=Vector2(player.rect.x+player.rect.w/2,player.rect.y+player.rect.h/2)
        own_pos=Vector2(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2)
        difference =Vector2(player_pos-own_pos)

        rotation_z=math.atan2(difference.y,difference.x)
       
        self.angle=360-(180 / math.pi) * -math.atan2(difference.y, difference.x)

    def move_to_player(self):
        import math
        from pygame import  Vector2
        angle=math.radians(self.angle)
        self.movement_vel=Vector2(math.cos(angle)*self.speed,math.sin(angle)*self.speed)

    def dead_animation(self):
        
        class Particle:
            def __init__(self,x,y,vx,vy,w,screen):
                self.x=x
                self.y=y
                self.vx=vx
                self.vy=vy
                self.w=w
                self.screen=screen
            def show(self):
                pygame.draw.rect(self.screen,self.get_color(),(self.x,self.y,self.w,self.w))
            def update_pos(self):
                self.x+=self.vx
                self.y+=self.vy
            def get_color(self):
                from random import randint
                return (randint(110,180),randint(10,30),randint(10,30))
        import time
        from random import randint
        start=time.time()
        particles=[]
        for i in range(randint(20,60)):
            particles.append(Particle(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,randint(-10,10),randint(-10,10),10,self.screen))
        print("seconds passed: ",time.time()-start)
        while (time.time()-start)<0.4:
            
            for i in particles:
                i.update_pos()
                
                i.show()
               
                pygame.display.flip()
        
        #particles=[]
        print("stopped dead animation")