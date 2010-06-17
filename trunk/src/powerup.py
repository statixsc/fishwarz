# -*- coding: utf-8  -*-
import pygame #@UnresolvedImport
from vec2d import vec2d
import os

'''
Created on 2 jun 2010

@author: Ingemar
'''
class Powerup(pygame.sprite.Sprite):
    """Representerar en powerup."""
    
    def __init__(self, screen, init_position):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        # !TODO! Ladda med os.join.osv
        self.image_normal = pygame.image.load(os.path.join('images','pearl-normal.png')).convert_alpha()
        self.image = self.image_normal
        self.image_blink = pygame.image.load(os.path.join('images','pearl-blink.png')).convert_alpha()
        self.powerup_sound = pygame.mixer.Sound(os.path.join('sound','powerup.wav'))
        self.powerup_sound.set_volume(0.8)
        # Rect behövs för kolissionshanteringen
        self.rect = self.image.get_rect()
        # Startpositionen
        self.rect.x, self.rect.y = init_position
        self.blink_timer = 0
        # Start-position. En vektor
        self.pos = vec2d(init_position)
        # Start-riktning. En normaliserad vektor
        self.direction = vec2d((-1,-1)).normalized()
        self.speed = 0.15  
        
    def update(self, time_passed):
        self.blink_timer += time_passed
        # Beräkna förflyttningen. Riktningen, vilket är en normaliserad
        # vektor multiplicerat med sträckan dvs. hastighet x tiden
        displacement = vec2d(
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)
        # Sätt den nya positionen
        self.pos += displacement
        # Uppdatera dess rect för kolissioner
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y 
        # Studsa på väggar. Om utanför vänsterkanten
        bounds_rect = self.screen.get_rect()
        # Om utanför vänsterkanten
        if self.pos.x < bounds_rect.left-5:
            # Sätt pos inte längre än kanten
            self.pos.x = bounds_rect.left-5
            # Ändra riktningvektorn till andra hållet
            self.direction.x *= -1
        elif self.pos.x > bounds_rect.right-35:
            self.pos.x = bounds_rect.right-35
            self.direction.x *= -1
        elif self.pos.y < bounds_rect.top-5:
            self.pos.y = bounds_rect.top-5
            self.direction.y *= -1
        elif self.pos.y > bounds_rect.bottom-35:
            self.pos.y = bounds_rect.bottom-35
            self.direction.y *= -1             
        # Ändrar bilder efter varje x ms
        if self.blink_timer>200:
            self.blink_timer = 0
            if self.image == self.image_normal:
                self.image = self.image_blink
            else:
                self.image = self.image_normal
    
    