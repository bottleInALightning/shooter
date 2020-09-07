import pygame 
import random
pygame.init()

class zombie_enemy:
    def __init__(self,screen,x,y,w,h,var):
        self.screen=screen
        self.rect=pygame.Rect(x,y,w,h)
        self.hitbox=self.rect
        #self.img=pygame.image.load("/home/lars/Desktop/PyWeekTraining/shooter/images/FLEnemy1.png")
        self.var=var
        self.dead=False
        self.movement_vel=pygame.Vector2(1,0)
        self.movement_acc=pygame.Vector2()
        self.angle=0
        self.speed=4

        self.sound_channel=pygame.mixer.find_channel(True)
        self.sound_channel.set_volume(0.8)
        self.die_sound=pygame.mixer.Sound("./sfx/zombie_enemy_die_sound.wav")
        
        self.death_animation_duration=60
        self.death_particle_range=[40,60]
        self.death_blood_particles=[]
        self.death_blood_particle_speed=2
        self.frame_start_death_animation=-1

        self.detection_range=400
        
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
        #print("Dead: ",self.dead)
        if not self.dead:
            #xs=self.var.camera_scrolling[0]
            #ys=self.var.camera_scrolling[1]
            if self.movement_vel.x<0:
                if frame==0:
                    self.screen.blit(self.MLImages[0],(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
                    
                elif frame==1:
                    self.screen.blit(self.MLImages[1],(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
                else:
                    print("frame erro index out of range")
            elif self.movement_vel.y>0:
                if frame==0:
                    self.screen.blit(self.MDImages[0],(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
                    
                elif frame==1:
                    self.screen.blit(self.MDImages[1],(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
                else:
                    print("frame erro index out of range")
            elif self.movement_vel.x>0:
                if frame==0:
                    self.screen.blit(self.MRImages[0],(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
                    
                elif frame==1:
                    self.screen.blit(self.MRImages[1],(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
                else:
                    print("frame erro index out of range")
    def check_shot(self,player,animation_counter):
        
        try:
            for i in range(len(player.bullets)):#somehow only works if two bullets hit
                #print("cur bullet {}".format(i))
                if not self.dead:
                    if self.hitbox.colliderect(player.bullets[i].rect):
                        player.bullets.remove(player.bullets[i])

                        print("I dead")
                        self.dead=True
                        self.var.player_points+=1
                        self.sound_channel.play(self.die_sound)
                        self.frame_start_death_animation=animation_counter

            self.update_show_death_particles(animation_counter)
            
                    
                    #self.respawn()
                    
        except:
            print("list index out of range Error")
    def update_pos(self):
        self.rect.x+=self.movement_vel.x
        self.rect.y+=self.movement_vel.y
        pass
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
        import random
        from pygame import  Vector2
        dist=math.sqrt((self.var.player.rect.x-self.rect.x)**2+(self.var.player.rect.y-self.rect.y)**2)
        if dist <self.detection_range:
            angle=math.radians(self.angle)
            self.movement_vel=Vector2(math.cos(angle)*self.speed,math.sin(angle)*self.speed)

        else:
            self.movement_vel=Vector2(random.randint(-1,1)*self.speed,random.randint(-1,1)*self.speed)
    def update(self,player,frame,animation_counter):
        
        self.update_pos()
        self.move_to_player()
        self.rot_to_player(player)
        self.check_shot(player,animation_counter)
        self.show(frame)
    
    def update_show_death_particles(self,animation_counter):#have to remove enemy, 
        from random import randint
        #print("i got shot")
        #print("cur frame count:",animation_counter)
       # print("rel frame count: ",animation_counter-self.frame_start_death_animation)
        
        if self.dead==True:
            if not animation_counter-self.frame_start_death_animation>self.death_animation_duration:#if not time to die for particles
                if not len(self.death_blood_particles)>0:#if they arent already initalized
                    print("init new parts")
                    for i in range(self.death_particle_range[0],self.death_particle_range[1]):#here they get intited
                        self.death_blood_particles.append(Particle(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,randint(-self.death_blood_particle_speed,self.death_blood_particle_speed),randint(-self.death_blood_particle_speed,self.death_blood_particle_speed),randint(4,10),self.screen,self.var))
                else:
                    for i in self.death_blood_particles:
                        i.update_pos()
                        i.show()
                       
            else:
                print("end, i think i dont get here")       
                self.death_blood_particles=[]
                #self.respawn()
                self.var.enemies.remove(self)
        
#------ Particle Class ------------
class Particle:
            def __init__(self,x,y,vx,vy,w,screen,var):
                self.x=x
                self.y=y
                self.vx=vx
                self.vy=vy
                self.w=w
                self.screen=screen
                self.var=var
            def show(self):
                pygame.draw.rect(self.screen,self.get_color(),(self.x-self.var.camera_scrolling[0],self.y-self.var.camera_scrolling[1],self.w,self.w))
            def update_pos(self):
                self.x+=self.vx#-self.var.camera_scrolling[0]
                self.y+=self.vy#-self.var.camera_scrolling[1]
            def get_color(self):
                from random import randint
                return (randint(110,180),randint(10,30),randint(10,30))