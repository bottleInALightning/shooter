
def mainFunction():
    from code.player import Player
    from code.zombie_enemy import zombie_enemy
    from random import randint
    import pygame; pygame.init()
    WINDOWWIDTH=800
    WINDOWHEIGHT=600
    FPS=30
    clock=pygame.time.Clock()
    enemies=[]
    gameRunning=True

    screen=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Shooting Circle")
    
    players=[]
    player1=Player(100,100,70,70,1,screen,)
    #player2=Player(400,400,70,70,1,screen,"/home/lars/Desktop/PyWeekTraining/shooter/images/bluePlayer.png")
    players.append(player1)
    #players.append(player2)
    def play_BG_music():
        pygame.mixer.music.load("./sfx/BG_music.wav")
        pygame.mixer.music.play(-1)
        
    zomb=zombie_enemy(screen,500,100,100,100)
    enemies.append(zomb)
    animation_duration=20
    animation_clock=0
    play_BG_music()
    while gameRunning:
        clock.tick(FPS)
        animation_clock+=1
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                gameRunning=False
                pygame.quit()
           
            else:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        zomb=zombie_enemy(screen,randint(100,WINDOWWIDTH-WINDOWWIDTH/2),randint(100,WINDOWHEIGHT-200),100,100)
                    player1.check_move(event)
                elif event.type==pygame.KEYUP:
                    player1.check_move(event)
                if event.type==pygame.MOUSEBUTTONDOWN:
                    player1.shoot(event)
        screen.fill((50,50,50))
        for i in players:
            i.update()
            i.check_dead(enemies)
        if animation_clock>=animation_duration*2:
            animation_clock=0
        elif animation_clock>animation_duration:
            zomb.show(1)
        else:
            zomb.show(0)
        zomb.rot_to_player(player1)
        zomb.check_shot(player1)
        zomb.move_to_player()
        zomb.update_pos()
        
        pygame.display.flip()
        
if __name__=="__main__":
    mainFunction()


