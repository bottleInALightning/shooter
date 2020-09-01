import pygame

class Collectable:
    def __init__(self,x,y,w,h,screen,players,var):
        self.rect=pygame.Rect(x,y,w,h)
        
        self.screen=screen
        self.players=players
        self.var=var
        
        self.images=[pygame.image.load("./images/bullet_shooting_right.png"),pygame.image.load("./images/bullet_behind.png"),pygame.image.load("./images/bullet_shooting_left.png"),pygame.image.load("./images/bullet_front.png")]
        
        self.var.bullet_collectables.append(self)
        self.sound_channel=pygame.mixer.find_channel(True)
        self.sound_channel.set_volume(1)
        self.collect_sound=pygame.mixer.Sound("./sfx/collect_bullet_sound.wav")
        self.max_bullets_reached_sound=pygame.mixer.Sound("./sfx/max_bullets_reached_sound.wav")

        self.display_pos=[self.rect.x,self.rect.y]
    def show(self,index):
        self.display_pos[0]=self.rect.x+self.var.camera_scrolling[0]
        self.display_pos[1]=self.rect.y+self.var.camera_scrolling[1]

        self.screen.blit(self.images[index],(self.display_pos[0],self.display_pos[1]))
   
    def check_collected(self):
        
        for player in self.players:#have to pass not none value
            if player.rect.colliderect(self.rect):
                self.var.bullet_collectables.remove(self)
                if player.bullet_count<player.max_bullet_count:
                    player.bullet_count+=1
                    print("sound!")
                    self.sound_channel.play(self.collect_sound)
                else:
                    self.sound_channel.play(self.max_bullets_reached_sound)
                break
    def update_pos(self):
        #self.rect.x-=self.var.camera_scrolling[0]
        #self.rect.y-=self.var.camera_scrolling[1]
        pass
    def update(self):
        self.update_pos()
        self.show(0)
        self.check_collected()
