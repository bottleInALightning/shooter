import pygame 
import random
pygame.init()

class ghost_enemy:
    def __init__(self,screen,x,y,w,h,var):
        self.enemy_type="ghost"
        self.screen=screen
        self.rect=pygame.Rect(x,y,w,h)
        self.hitbox=self.rect
        #self.img=pygame.image.load("/home/lars/Desktop/PyWeekTraining/shooter/images/FLEnemy1.png")
        self.var=var
        self.dead=False
        self.movement_vel=pygame.Vector2(1,0)
        self.movement_acc=pygame.Vector2()
        self.angle=0
        self.speed=2

        self.sound_channel=pygame.mixer.find_channel(True)
        self.sound_channel.set_volume(0.8)
        self.die_sound=pygame.mixer.Sound("./sfx/zombie_enemy_die_sound.wav")
        
        self.death_animation_duration=60
        self.death_particle_range=[40,60]
        self.death_blood_particles=[]
        self.death_blood_particle_speed=2
        self.frame_start_death_animation=-1

        self.detection_range=400

        self.collided_top=False
        self.collided_right=False
        self.collided_bottom=False
        self.collided_left=False

        self.moving=False
        self.test_image=pygame.image.load("./images/ghost_enemy_test_version.png")
        self.test_image=pygame.transform.scale(self.test_image,(self.rect.w,self.rect.h))
    def show(self,frame):
      if not self.dead:
          self.screen.blit(self.test_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
          #showing enemyd
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
        self.moving=True
        if self.moving:
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

        #rotation_z=math.atan2(difference.y,difference.x)
       
        self.angle=360-(180 / math.pi) * -math.atan2(difference.y, difference.x)

    def move_to_player(self):
        import math
        import random
        from pygame import  Vector2
        dist=math.sqrt((self.var.player.rect.x-self.rect.x)**2+(self.var.player.rect.y-self.rect.y)**2)
        if dist <self.detection_range:
            angle=math.radians(self.angle)
            self.movement_vel=Vector2(math.cos(angle)*self.speed,math.sin(angle)*self.speed)

        #else:
            #self.angle=random.randint(0,360)
            
    def update(self,player,frame,animation_counter):
        
        self.update_pos()
       #self.move()
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
                    
                    for i in range(self.death_particle_range[0],self.death_particle_range[1]):#here they get intited
                        self.death_blood_particles.append(Particle(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,randint(-self.death_blood_particle_speed,self.death_blood_particle_speed),randint(-self.death_blood_particle_speed,self.death_blood_particle_speed),randint(4,10),self.screen,self.var))
                else:
                    for i in self.death_blood_particles:
                        i.update_pos()
                        i.show()
                       
            else:
                       
                self.death_blood_particles=[]
                #self.respawn()
                self.var.enemies.remove(self)

    def move(self):
        way_free=True
        if self.var.frame_counter%30==0:
            for i in self.var.walls:
                if self.check_straight_line_to_player(pygame.Vector2(i.rect.x,i.rect.y),pygame.Vector2(i.rect.x+i.rect.w,i.rect.y)):
                    way_free=False
                elif self.check_straight_line_to_player(pygame.Vector2(i.rect.x+i.rect.w , i.rect.y),pygame.Vector2(i.rect.x+i.rect.w , i.rect.y+i.rect.h)):
                    way_free=False
                elif self.check_straight_line_to_player(pygame.Vector2(i.rect.x+i.rect.w,i.rect.y+i.rect.h),pygame.Vector2(i.rect.x,i.rect.y+i.rect.h)):
                    way_free=False
                elif self.check_straight_line_to_player(pygame.Vector2(i.rect.x,i.rect.y),pygame.Vector2(i.rect.x,i.rect.y+i.rect.h)):
                    way_free=False

            if way_free==True:
                self.move_to_player()
    def check_wall_collision(self):
        collide_list=[]
        for tile in self.var.walls:
            if self.rect.colliderect(tile.rect):
                collide_list.append(tile)
        return collide_list

    def move_zombie(self):
        pass
    def check_straight_line_to_player(self,wall_line1,wall_line2):
        
        def ccw(A,B,C):
            return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    
        A=pygame.Vector2(self.rect.x,self.rect.y)
        B=pygame.Vector2(self.var.player.rect.x,self.var.player.rect.y)
        C=pygame.Vector2(wall_line1.x,wall_line1.y)
        D=pygame.Vector2(wall_line2.x,wall_line2.y)

        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
           
        
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
                if self.x-self.var.camera_scrolling[0] >-40 and self.x-self.var.camera_scrolling[0]<self.var.window_width+40:
                    if self.y-self.var.camera_scrolling[1] >-40 and self.y-self.var.camera_scrolling[1]<self.var.window_height+40:
 
                        pygame.draw.rect(self.screen,self.get_color(),(self.x-self.var.camera_scrolling[0],self.y-self.var.camera_scrolling[1],self.w,self.w))
            def update_pos(self):
                self.x+=self.vx#-self.var.camera_scrolling[0]
                self.y+=self.vy#-self.var.camera_scrolling[1]
            def get_color(self):
                from random import randint
                #base color (58, 248, 90)
                return (randint(20,70),randint(190,250),randint(50,100))
            