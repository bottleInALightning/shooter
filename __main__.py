
def mainFunction():
    from code.player import Player
    from code.zombie_enemy import zombie_enemy
    from code.collectable import Collectable
    from code.walls import Wall
    from code.game_map import Map
    from code.Updgrade_button import Upgrade_Button
    from code.ghost_enemy import ghost_enemy

    from random  import randint
    
    import pygame; pygame.init()
    
    WINDOWWIDTH=800
    WINDOWHEIGHT=600
    FPS=80
    clock=pygame.time.Clock()
    enemies=[]
    gameRunning=True

    

    class Var:
        def __init__(self):
            self.bullet_collectables=[]
            self.enemies=[]
            self.window_width=WINDOWWIDTH
            self.window_height=WINDOWHEIGHT
            self.camera_scrolling=[0,0]
            self.walls=[]
            self.background_image=pygame.image.load("./images/background_log_type.png")

            self.game_over=False
            self.tiles_rows_cols=[60,60]
            self.animation_duration=10
            self.animation_clock=0
            self.ui_font=pygame.font.SysFont('Cambria', 60)
            self.frame_counter=0
            self.player_points=0
            
            self.player=None
            self.score_board_image=pygame.image.load("./images/score_board.png")
            self.upgrade_buttons=[]
            self.paused=False

                
    var=Var()
    screen=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Shooting Circle")
    
    players=[]
    player1=Player(450,400,70,70,1,screen,var)
    var.player=player1
    #player2=Player(400,400,70,70,1,screen,"/home/lars/Desktop/PyWeekTraining/shooter/images/bluePlayer.png")
    players.append(player1)
    #players.append(player2)
    start_map=Map(var,players[0],screen)
    def play_BG_music():
        pygame.mixer.music.load("./sfx/BG_music.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    def spawn_rand_bullet(var):
        def get_col_pos():
            return [randint(0,var.tiles_rows_cols[1]*32),randint(20,var.tiles_rows_cols[0]*32)]

        ran_num=randint(0,150)
        if ran_num==5:
           
            while True:
                collided=False
                pos=get_col_pos()
                for i in var.walls:
                    if pygame.Rect(pos[0],pos[1],32,32).colliderect(i.rect):
                        collided=True
                if not collided:
                    Collectable(pos[0],pos[1],32,32,screen,players,var)
                    break
            #temp_col=Collectable(randint(40,WINDOWWIDTH),randint(40,WINDOWHEIGHT),32,32,screen,players,var)
            #var.bullet_collectables.append(temp_col)#this will prob throw an error
    def update_camera_scrolling(var,player):
        var.camera_scrolling[0]+=(player.rect.x - var.camera_scrolling[0] -400)
        var.camera_scrolling[1]+=(player.rect.y-var.camera_scrolling[1]-300)
       # var.camera_scrolling[0]=10
        #var.camera_scrolling[1]=50
        '''
        class Camera:
            def __init__(self):
                self.x = 0
                self.y = 0
                self.speed = 0.125
                self.offset = (0, 0)

            def follow(self, x, y):
                end_x, end_y = x + self.offset[0], y + self.offset[1]
                self.x = end_x*self.speed + self.x*(1-self.speed)
                self.y = end_y*self.speed + self.y*(1-self.speed)
        '''
        #pass
        
    def render_points(var):
        
        screen.blit(var.score_board_image,(680,30))
        score_surface = var.ui_font.render('{}'.format(var.player_points), False, (229, 148, 26))
        if var.player_points<10:
            screen.blit(score_surface,(720,50))
        elif var.player_points<100:
            screen.blit(score_surface,(705,50))
        else:
            screen.blit(score_surface,(693,50))
    def set_may_shoot(var):
        hovering=False
        for i in var.upgrade_buttons:
            if i.hovering==True:
                hovering=True
        if hovering==True:
            var.player.may_shoot=False
        else:
            var.player.may_shoot=True
    def spawn_random_zombies(var):
        var.max_zombies=2
        def get_col_pos():
            return [randint(0,var.tiles_rows_cols[1]*32),randint(20,var.tiles_rows_cols[0]*32)]
        import math
        ran_num=randint(0,90)
        if ran_num==5 and var.max_zombies>=0:
            var.max_zombies-=1
            while True:
                    collided=False
                    pos=get_col_pos()
                    for i in var.walls:
                        if pygame.Rect(pos[0],pos[1],32,32).colliderect(i.rect):
                            collided=True
                    dist_to_player=math.sqrt((pos[0]-var.player.rect.x)**2+(pos[1]-var.player.rect.y)**2)
                    if dist_to_player<400:
                        collided=True
                    if not collided:

                        zomb=zombie_enemy(screen,pos[0],pos[1],64,64,var)
                        var.enemies.append(zomb)
                        break
    def spawn_random_ghost(var):
        
        def get_col_pos():
            return [randint(0,var.tiles_rows_cols[1]*32),randint(20,var.tiles_rows_cols[0]*32)]
        import math
        ran_num=randint(0,100)
        if ran_num==5 :
            
            while True:
                    collided=False
                    pos=get_col_pos()
                    for i in var.walls:
                        if pygame.Rect(pos[0],pos[1],32,32).colliderect(i.rect):
                            collided=True
                    dist_to_player=math.sqrt((pos[0]-var.player.rect.x)**2+(pos[1]-var.player.rect.y)**2)
                    if dist_to_player<400:
                        collided=True
                    if not collided:

                        zomb=ghost_enemy(screen,pos[0],pos[1],75,100,var)
                        var.enemies.append(zomb)
                        break
    
   
    #zomb2=zombie_enemy(screen,300,40,100,100)
    #enemies.append(zomb)
    #enemies.append(zomb2)
    
    
    ghost=ghost_enemy(screen,20,20,64,64,var)
    var.enemies.append(ghost)

    button=Upgrade_Button(700,130,64,64,"heart",screen,var)
    button2=Upgrade_Button(700,200,64,64,"heart_container",screen,var)
    button3=Upgrade_Button(700,270,64,64,"double_bullet",screen,var)
    var.upgrade_buttons.append(button)
    var.upgrade_buttons.append(button2)
    var.upgrade_buttons.append(button3)

    

    play_BG_music()
    while gameRunning:
        update_camera_scrolling(var,players[0])
        set_may_shoot(var)
        clock.tick(FPS)
        #print("FPS:",clock.get_fps())
        #print("len of enemies:",len(var.enemies))
        var.animation_clock+=1
        var.frame_counter+=1
        for event in pygame.event.get():    
            if event.type==pygame.QUIT:
                gameRunning=False
                pygame.quit()
            else:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        zomb=zombie_enemy(screen,randint(100,WINDOWWIDTH-WINDOWWIDTH/2),randint(100,WINDOWHEIGHT-200),100,100,var)
                    player1.check_move(event)
                elif event.type==pygame.KEYUP:
                    player1.check_move(event)
                if event.type==pygame.MOUSEBUTTONDOWN:
                    player1.shoot(event)
        #----- Here all the drawing stuff starts -------
        screen.fill((50,50,50))
        #------- updating map --------------
        start_map.display_map()
        #--------- showing walls --------
        for i in var.walls:
            i.update()
        #-------- updating players ----------
        for i in players:
            i.update()
            i.check_dead(enemies)
        
        #--------- spawning random bullets ----------
        spawn_rand_bullet(var)
        ''''
        print("player x:",players[0].rect.x)
        print("player y:",players[0].rect.y)
        print("scroll x:",var.camera_scrolling[0])
        print("scroll y:",var.camera_scrolling[0])
        '''
        
        #----- spawning random zombies ---------
        spawn_random_zombies(var)
        spawn_random_ghost(var)
        #----------- updating objects based on animation_count for animations ---------
        #objects:   enemies, 
        if var.animation_clock==var.animation_duration*2:
            var.animation_clock=1
            for i in enemies:
                i.update(player1,1,var.frame_counter)     
        elif var.animation_clock>var.animation_duration:
            for i in var.enemies:
                i.update(player1,0,var.frame_counter)
        else:
            for i in var.enemies:
                i.update(player1,1,var.frame_counter)
        #updating,showing every collectable bullet and checking if picked up
        for i in var.bullet_collectables:
            i.update()

        #updating screen
        var.player.show_lose_life_animation(10)
        #---------- here belongs all showing on the screen (if possible) ----
        render_points(var)
        #button.update(var.frame_counter)
        for i in var.upgrade_buttons:
            i.update(var.frame_counter)
        if var.game_over:
            pygame.draw.rect(screen,(50,50,50),(0,0,var.window_width,var.window_height))
            go_font=pygame.font.SysFont("SerifBold",140)
            game_over_surf = go_font.render('Game Over!', False, (255,255,255))
            screen.blit(game_over_surf,(120,210))

        pygame.display.flip()
    
if __name__=="__main__":
    mainFunction()


