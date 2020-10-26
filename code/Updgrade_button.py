import pygame
pygame.init()

class Upgrade_Button:
    def __init__(self,x,y,w,h,cage_input,screen,var):
        
        
        self.rect=pygame.Rect(x,y,w,h)
        self.cage_input=cage_input
        self.var=var
        self.screen=screen
        self.item_cage_sprites_animation=self.sprite_sheet((32,32),"./images/item_cage.png")
       
        self.idle_item_cage=self.sprite_sheet((32,32),"./images/item_cage.png")[0]

        self.animation_frame_counter=0
        self.hover_animation_duration=10
        self.last_clicked_frame=0
        self.icons={"heart":self.sprite_sheet((31,31),"./images/hearts.png")[0],"heart_container":pygame.image.load("./images/heart_container.png"),"bullet":pygame.image.load("./images/bullet_shooting_left.png"),"speed":2,"double_bullet":pygame.image.load("./images/icon_double_bullet.png")}
        self.hovering=False

        self.upgrade_sound=pygame.mixer.Sound("./sfx/upgrade_sound.wav")
    def show(self,frame_counter):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            
            self.hovering=True
            if self.animation_frame_counter != len(self.item_cage_sprites_animation)-1:
                current_image=self.item_cage_sprites_animation[(((self.var.frame_counter)//self.hover_animation_duration)-1)%len(self.item_cage_sprites_animation)-1]
                self.screen.blit(current_image,(self.rect.x,self.rect.y))
                self.animation_frame_counter+=1
            else:
                self.screen.blit(self.item_cage_sprites_animation[len(self.item_cage_sprites_animation)-1],self.rect)
                
        else:
            self.screen.blit(self.idle_item_cage,self.rect)
            self.hovering=False
            self.animation_frame_counter=0
            




    def update(self,frame_counter):

        self.show(frame_counter)
        self.check_clicked()
        self.show_icon()
        
        


    def check_clicked(self):
        cost_heart=5
        cost_heart_container=10
        cost_more_bullets=20
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()) and self.var.frame_counter-self.last_clicked_frame>=10:
            
            self.clicked=True
            self.last_clicked_frame=self.var.frame_counter

            
            if self.cage_input=="heart":
                if self.var.player_points>=cost_heart and self.var.player.lifes < self.var.player.max_lifes:
                    self.var.player_points-=cost_heart
                    self.var.player.lifes+=1
                    #show success buy animation
                    self.var.player.sound_channel.play(self.upgrade_sound)
            elif self.cage_input=="heart_container":
                if self.var.player_points>=cost_heart_container and self.var.player.max_lifes< self.var.player.max_max_lifes:
                    self.var.player_points-=cost_heart_container
                    self.var.player.max_lifes+=1
                    self.var.player.sound_channel.play(self.upgrade_sound)
            elif self.cage_input=="double_bullet":
                if self.var.player_points>=cost_more_bullets and self.var.player.max_extra_per_shot_bullets>self.var.player.extra_per_shot_bullet:
                    self.var.player_points-=cost_more_bullets
                    self.var.player.extra_per_shot_bullet+=1
                    self.var.player.sound_channel.play(self.upgrade_sound)
            
    
    def sprite_sheet(self,size,file,pos=(0,0)):
        import pygame
        #Initial Values
        len_sprt_x,len_sprt_y = size #sprite size
        
        sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
        sheet = pygame.image.load(file).convert_alpha() #Load the sheet
        sheet_rect = sheet.get_rect()
       # print(sheet_rect)
        sprites = []
        
        image_size=(64,64)
    
        
        for i in range(0,sheet_rect.width-len_sprt_x,size[0]):#columns
             
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        return sprites
    def show_icon(self):
        #print("type:",type(self.icons[self.cage_input]))
        #print("cage input:",self.cage_input)
        current_icon=pygame.transform.scale(self.icons[self.cage_input],(40,40))
        self.screen.blit(current_icon,(self.rect.x+12,self.rect.y+12))
