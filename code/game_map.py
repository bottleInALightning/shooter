import pygame 
pygame.init()
from code.walls import Wall
class Map:
    def __init__(self,var,player,screen):
        self.var=var
        self.player=player
        self.screen=screen
        self.tiles={1:pygame.image.load("./images/wooden_floor.png"),3:pygame.image.load("./images/wooden_floor_duck.png")}
        self.tile_size=32
        self.map_list=None
        self.load_map_data()
        
        self.map_size=(25,25)
        #self.tiles={1:pygame.image.load("./images/new_floor.png"),3:pygame.image.load("./images/floor_image_2_variation.png")}

        #self.cam_scroll_x=0
        #self.cam_scroll_y=0
        
        
    def load_map_data(self):
        import ast
        map_indices_list=None
        with open("./Maps/test_map2.txt","r") as map:
            map_s=map.read()
           
            #map_indicies_list=ast.literal_eval(map_s)
            map_indices_list=eval(map_s)
        
      
        self.map_list=map_indices_list

        y=0
        for layer in self.map_list:
            x=0
            for col in layer:
                
                if col==2:
                    self.var.walls.append(Wall(x*self.tile_size,y*self.tile_size,self.var,True,self.screen))
                
                x+=1
            
            y+=1
        
    
    def display_map(self):
        y=0
        for layer in self.map_list:
            x=0
            for col in layer:
                if col==1:
                    self.screen.blit(self.tiles[1],(x*self.tile_size-self.var.camera_scrolling[0],y*self.tile_size-self.var.camera_scrolling[1]))
                
                elif col==3:
                   
                    self.screen.blit(self.tiles[3],(x*self.tile_size-self.var.camera_scrolling[0],y*self.tile_size-self.var.camera_scrolling[1]))
                x+=1
            
            y+=1
        
        #print(self.cam_scroll_x,self.cam_scroll_y)