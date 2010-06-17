# -*- coding: utf-8  -*-
import pygame #@UnresolvedImport
import random
from vec2d import vec2d
import os

#------------------------------------------------------------------------------
# BaseShot - Spelarens vanliga bubbelskott
#
#------------------------------------------------------------------------------
class BaseShot(pygame.sprite.Sprite):
    """Player basic shots."""
    
    def __init__(self, screen, init_x, init_y, dir_x=0, dir_y=0):
        """Konstruktorn.
        
        init_x är startposition
        dir_x är riktningen och hastighet i pxl
        
        """
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen 
        # TODO! Statisk bild för skott-klassen
        self.image = pygame.image.load(os.path.join('images','bubbla.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.dir_x = dir_x
        self.dir_y = dir_y
        
    def update(self):
        """Förflyttar skottet.
        
        dir_x är rikningen i x-led
        dir_y är riktningen i y-led
        
        """
        self.rect.move_ip(self.dir_x, self.dir_y)
        
    def show_boundary(self):
        """Vart går gränsen? Ritar en röd ruta vid player rect. 
        
        For testing purposes.
        
        """ 
        pygame.draw.rect(self.screen, pygame.Color('Red'), self.rect, 1)
        
#------------------------------------------------------------------------------
# BossShot
#
#
#------------------------------------------------------------------------------
class BossShot(BaseShot):
    
    def __init__(self, screen, init_x, init_y):
        # Anropa dess parents konstruktor
        BaseShot.__init__(self, screen, init_x, init_y)
        # Skapa en rect!
        self.rect = pygame.Rect(init_x, init_y, 16, 16)
        
    def update(self, time_passed):
        self.rect.move_ip(-5, 0)
        
    def rita(self):
        """For lazers! Ritar upp en blinkande boll.
        
        Byter färg varje update så den blinkar.
        
        """
        r = random.randint(0, 255) 
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # Ritar cirkeln med pos som center av cirkeln!
        # Vill att den ska använda mitten av hitboxen, dvs Rect som origo.
        pygame.draw.circle(self.screen, pygame.Color(r,b,g), (self.rect.x+8,self.rect.y+8), 8)
        # Testa hitbox
        # pygame.draw.rect(self.screen, pygame.Color('Red'), self.rect, 1)

#------------------------------------------------------------------------------
# VektorShot
#
#
#------------------------------------------------------------------------------        
class VektorShot(pygame.sprite.Sprite):
    
    def __init__(self, screen, init_position, init_direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        # Skapa en rect! för ritning och kollisionshantering
        init_x, init_y = init_position
        self.rect = pygame.Rect(init_x, init_y, 16, 16)
        # Start-position. En vektor
        self.pos = vec2d(init_position)
        # Start-riktning. En normaliserad vektor
        self.direction = vec2d(init_direction).normalized()
        self.speed = speed        
        
    def update(self, time_passed):
        # Beräkna förflyttningen. Riktningen, vilket är en normaliserad
        # vektor multiplicerat med sträckan dvs. hastighet x tiden
        displacement = vec2d(
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)
        # Sätt den nya positionen
        self.pos += displacement 
        # Uppdatera objektets rect - för kollisioner
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y 
        
    def rita(self):
        r = random.randint(0, 255) 
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # Ritar cirkeln med pos som center av cirkeln!
        # Vill att den ska använda mitten av hitboxen, dvs Rect som origo.
        pygame.draw.circle(self.screen, pygame.Color(r,b,g), (int(self.pos.x),int(self.pos.y)), 8)
        
        