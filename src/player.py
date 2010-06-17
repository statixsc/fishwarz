# -*- coding: utf-8  -*-
import pygame #@UnresolvedImport
from vec2d import vec2d
from shots import BaseShot
import os


class PlayerShip(pygame.sprite.Sprite):
    """Player ship."""
    
    def __init__(self, screen):
        """Konstruktorn."""
        pygame.sprite.Sprite.__init__(self) 
        self.screen = screen
        # Originalbilden
        self.image = pygame.image.load(os.path.join('images','mort.png')).convert_alpha()
        # Rect behövs för kolissionshanteringen
        self.rect = self.image.get_rect()        
        self.rect.center = (100, 220)
        self.x = 0
        self.y = 0
        self.power = 1   # 1,3,5
        # Behövs för att samla skotten
        self.playershots_grp = pygame.sprite.Group()
        
    def update(self):
        """Update metoden kallas varje gång vi itererar spel-loopen.
        
        Förflyttar spelarens skepp och kontrollerar gränserna.
        
        """
        self.rect.move_ip(self.x,self.y)
        # Så att inte skeppet åker utanför kanterna
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()    
        
    def show_boundary(self):
        """Vart går gränsen? Ritar en röd ruta vid player rect. 
        
        For testing purposes.
        
        """ 
        pygame.draw.rect(self.screen, pygame.Color('Red'), self.rect, 1)

    def fire_weapon(self):
        """Skjuter vapnet.
        
        Börjar med en bubbla. Nästa nivå är tre bubblor.
        Och nästa fem bubblor.. Men sen?
        
        """
        ydir = [0, 1.5, -1.5, 3, -3]
        shot_xpos = self.rect.x + 35
        shot_ypos = self.rect.y + 7
        shot_xdir = 7
        for i in range(self.power):
            self.playershots_grp.add(BaseShot(self.screen,
                                              shot_xpos,
                                              shot_ypos,
                                              shot_xdir,
                                              ydir[i]))      
        