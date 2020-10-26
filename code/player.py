import pygame
from pygame.math import Vector2
import math
from code.bullet import Bullet
from pygame import mixer


class Player:

    def __init__(self,x,y,w,h,index,screen,var):
        #pygame.mixer.init(44100, -16,2,2048) 
        pygame.init()
        pygame.mixer.init(44100, -16,2,512)
        
        #print("mixer get init:",pygame.mixer.get_init())
        self.rect=pygame.Rect(x,y,w,h)
        self.screen=screen
        self.image=pygame.image.load("./images/bluePlayer.png")
        self.rotatedImage=self.image
        self.angle=0
        
        self.velocity=pygame.Vector2(0,0)
        self.speed=7
        self.bullet_speed=9
        self.shoot_timer=0
        self.bullets=[]
        self.bul_counter=0
        self.shoot_sound=mixer.Sound("./sfx/shoot_sound.wav")
        self.sound_channel=pygame.mixer.find_channel(True)
        self.sound_channel.set_volume(0.0)
        self.alive=True
        self.var=var
        self.max_bullet_count=10

        self.bullet_count=10
        
        self.lifes=3
        self.max_lifes=3
        self.max_max_lifes=6
        
        self.full_bullet_ui_img=pygame.image.load("./images/bullet_count_indicator_full_bullet.png")
        self.empty_bullet_ui_img=pygame.image.load("./images/bullet_count_indicator_empty_bullet.png")
        self.bullet_w_h=[16,16]

        self.extra_per_shot_bullet=0
        self.max_extra_per_shot_bullets=4

        self.may_shoot=True
        self.weapon_sprites=self.sprite_sheet((32,32),"./images/player_wooden_crystal_wand.png")
        #self.weapon_sprites=[pygame.transform.scale(sprite,(32,32)) for sprite in self.weapon_sprites]
        self.animation_duration=6
        self.animation_sprites={"walking_left":self.sprite_sheet((32,32),"./images/shooter_game_main_character_walking_left.png"),"walking_right":self.sprite_sheet((32,32),"./images/shooter_game_main_character_walking_right.png"),"idle":self.sprite_sheet((32,32),"./images/shooter_game_main_character_idle.png"),"walking_up":self.sprite_sheet((32,32),"./images/shooter_game_main_character_walking_up.png"),"walking_down":self.sprite_sheet((32,32),"./images/shooter_game_main_character_walking_down.png")}

        self.heart_sprites=self.sprite_sheet((31,31),"./images/hearts.png")
        #self.heart_sprites=[pygame.transform.scale(i,(64,64))for i in self.heart_sprites]
        #print("len heart_sprites:",len(self.heart_sprites))
        self.start_lose_life_animation=None
        self.lose_life_animation_active=False
        self.lose_life_circle_radius=0
    def load(self):
        self.img=pygame.transform.scale(self.image,(self.rect.w,self.rect.h))
        self.full_bullet_ui_img=pygame.transform.scale(self.full_bullet_ui_img,(self.bullet_w_h[0],self.bullet_w_h[1]))
        self.empty_bullet_ui_img=pygame.transform.scale(self.empty_bullet_ui_img,(self.bullet_w_h[0],self.bullet_w_h[1]))
    def show(self):
        #print("frame count:",self.var.frame_counter)
        #print("walking_right calculated frame:",(((self.var.frame_counter)//self.animation_duration)-1)%len(self.animation_sprites["walking_right"]))
        #print("len of walking right sprites:",len(self.animation_sprites["walking_right"]))
        #if self.alive:
        #    self.screen.blit(se.lf.rotatedImage,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
        
        if self.velocity.x>0:
            #walk right
            current_image=self.animation_sprites["walking_right"][(((self.var.frame_counter)//self.animation_duration)-1)%len(self.animation_sprites["walking_right"])]
            self.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
        elif self.velocity.x<0:
            current_image=self.animation_sprites["walking_left"][(((self.var.frame_counter)//self.animation_duration)-1)%len(self.animation_sprites["walking_left"])]
            self.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
        
        elif self.velocity.y>0:
            current_image=self.animation_sprites["walking_down"][(((self.var.frame_counter)//self.animation_duration)-1)%len(self.animation_sprites["walking_down"])]
            self.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
        
        elif self.velocity.y<0:
            current_image=self.animation_sprites["walking_up"][(((self.var.frame_counter)//self.animation_duration)-1)%len(self.animation_sprites["walking_up"])]
            self.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
        
        else:
            current_image=self.animation_sprites["idle"][(((self.var.frame_counter)//self.animation_duration)-1)%len(self.animation_sprites["idle"])]
            self.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))
        
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
        #if self.velocity.length()>0 or self.velocity.length()<0:
            #self.velocity=self.velocity.normalize()
        
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
        mouse_pos=Vector2(pygame.mouse.get_pos()[0]+self.var.camera_scrolling[0],pygame.mouse.get_pos()[1]+self.var.camera_scrolling[1])
        playerPos=Vector2(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2)
        difference =Vector2(mouse_pos-playerPos)

        rotation_z=math.atan2(difference.y,difference.x)
       
        self.angle=360-(180 / math.pi) * -math.atan2(difference.y, difference.x)
   

    def update(self):
        #self.rect.x+=self.velocity.x#*self.speed
        #self.rect.y+=self.velocity.y#self.speed
        self.show()
        self.move()
        self.posToAngle()
        self.rot_center()
        self.check_dead(self.var.enemies)
        self.update_bullets()
        self.display_bullet_count()
        self.display_lifes()
        #self.display_weapon()
        #print("x: {}, y: {}".format(self.rect.x,self.rect.y))
        
        
    def shoot(self,event):
        from random import random#give bullets a bit of randomness
        import random
        if event.type==pygame.MOUSEBUTTONDOWN and self.bullet_count>0 and self.may_shoot:
            angle=math.radians(self.angle)
            bulletVel=Vector2(math.cos(angle),math.sin(angle))
            
            self.bullets.append(Bullet(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,bulletVel,self.screen,self.bullet_speed,self,self.bul_counter,self.var))
            for i in range(self.extra_per_shot_bullet):
                new_angle=math.radians(self.angle+random.randint(-5,5))
                new_bullet_Vel=Vector2(math.cos(new_angle),math.sin(new_angle))

                self.bullets.append(Bullet(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,new_bullet_Vel,self.screen,self.bullet_speed+random.randint(-2,2),self,self.bul_counter,self.var))
            
            
            self.bul_counter+=1
            self.sound_channel.play(self.shoot_sound)
            self.bullet_count-=1
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
        if self.lifes<1:
            self.var.game_over=True

        import math
        
        for i in self.var.enemies:
            #i=enemy
            if not i.dead:
                dist_to_enemy=math.sqrt(((self.rect.x-i.rect.x)**2)+((self.rect.y-i.rect.y)**2))
                if i.enemy_type=="zombie":
                    if dist_to_enemy<20:
                        self.lifes-=1
                        self.lose_life_animation_active=True
                        self.var.enemies.remove(i)
                elif i.enemy_type=="ghost":
                    if dist_to_enemy<40:
                        self.lifes-=1
                        self.lose_life_animation_active=True
                        self.var.enemies.remove(i)
    def display_bullet_count(self):
        #i got: bullet count, max-bullet-count
        bullet_spacing=10
        
        #gonna be bottom
        filled_bullets=0
        for i in range(self.max_bullet_count):
            if filled_bullets<self.bullet_count:
                filled_bullets+=1
                self.screen.blit(self.full_bullet_ui_img,((self.var.window_width-(self.bullet_w_h[0]+bullet_spacing)*(i+1)),(self.var.window_height-self.bullet_w_h[1]-50)))
            else:
                self.screen.blit(self.empty_bullet_ui_img,((self.var.window_width-(self.bullet_w_h[0]+bullet_spacing)*(i+1)),(self.var.window_height-self.bullet_w_h[1]-50)))
    def display_lifes(self):
        heart_spacing=50
        full_lifes_counter=0
        for i in range(self.max_lifes):
            if full_lifes_counter<self.lifes:#draw full heart
                self.screen.blit(self.heart_sprites[0],(40+i*heart_spacing,500))
                full_lifes_counter+=1
            else:
                self.screen.blit(self.heart_sprites[1],(40+i*heart_spacing,500))
            
    def check_wall_collision(self):
        collide_list=[]
        for tile in self.var.walls:
            if self.rect.colliderect(tile.rect):
                collide_list.append(tile)
        return collide_list

    def move(self):
        self.rect.x+=self.velocity.x
       

        collisions=self.check_wall_collision()

        for i in collisions:
            if self.velocity.x>0:#moving right
                self.rect.right=i.rect.left
            if self.velocity.x<0:#moving left
                self.rect.left=i.rect.right
        
        self.rect.y+=self.velocity.y
        collisions=self.check_wall_collision()
        for i in collisions:
           
            if self.velocity.y>0:
                self.rect.bottom=i.rect.top
            if self.velocity.y<0:
                self.rect.top=i.rect.bottom


       

    def show_lose_life_animation(self,duration):
        glow_color=(217, 94, 38)
        if self.lose_life_animation_active:
            if self.start_lose_life_animation==None:
                self.start_lose_life_animation=self.var.frame_counter
            elif self.var.frame_counter-self.start_lose_life_animation>duration:
                self.lose_life_animation_active=False
                self.start_lose_life_animation=None
                self.lose_life_circle_radius=0
            else:
                self.lose_life_circle_radius+=50
                glow_surf=pygame.Surface((self.var.window_width,self.var.window_height))
                pygame.draw.circle(glow_surf,glow_color,(int(self.var.window_width/2),int(self.var.window_height/2)),self.lose_life_circle_radius+20)
                glow_surf.set_colorkey((0,0,0))
                self.screen.blit(glow_surf,(glow_color),(0,0),special_flags=pygame.BLEND_RGB_ADD)
                pygame.draw.circle(self.screen,(240,240,240),(int(self.var.window_width/2),int(self.var.window_height/2)),self.lose_life_circle_radius)

    
    '''
    
        movement=[self.velocity.x*self.speed*-1,self.velocity.y*self.speed*-1]
        #print(f"x speed={movement[0]} y speed={movement[1]} ")

        print("old x:",self.rect.x)
        self.rect.x+=movement[0]#-self.var.camera_scrolling[0]#-self.var.camera_scrolling[0]#updating player x pos and later if collide setting it to collide site
        print("new x:",self.rect.x)


        collisons=self.check_wall_collision()
        for i in collisons:#with checkin the next step i cant just check for movement>0 but - camera_scrolling
            if movement[0]>0:#-self.var.camera_scrolling[0]>0:
                #self.rect.left=i.rect.right
               # self.rect.right=i.rect.left
               pass
            if movement[0]<0:#-self.var.camera_scrolling[0]:
                #self.rect.right=i.rect.left
                #self.rect.left=i.rect.right
                pass

        self.rect.y+=movement[1]#-self.var.camera_scrolling[1]
        for i in collisons:#with checkin the next step i cant just check for movement>0 but - camera_scrolling
            if movement[1]>0:#-self.var.camera_scrolling[1]>0:
                #self.rect.bottom=i.rect.top
                pass
            if movement[0]<0:#-self.var.camera_scrolling[0]<0:
               # self.rect.top=i.rect.bottom
                pass
            '''
    def sprite_sheet(self,size,file,pos=(0,0)):
        import pygame
        #Initial Values
        len_sprt_x,len_sprt_y = size #sprite size
        #print("size",size)
        sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
        sheet = pygame.image.load(file).convert_alpha() #Load the sheet
        sheet_rect = sheet.get_rect()
        #print(sheet_rect)
        sprites = []
        
        image_size=(64,64)
    
        #print("row")
        for i in range(0,sheet_rect.width-len_sprt_x,size[0]):#columns
            #print("column")    
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        return sprites

    def display_weapon(self):
        animation_duration=10
        new_sprites=[]
        for image in self.weapon_sprites:
            orig_rect=self.rect
            
            angle=360-self.angle-90
            orig_rect = image.get_rect()
            rot_image = pygame.transform.rotate(image, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            
            new_sprites.append(rot_image)
        
        current_image=new_sprites[(((self.var.frame_counter)//animation_duration)-1)%len(new_sprites)]
        self.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1]))

        new_sprites=[]