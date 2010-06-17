# -*- coding: utf-8  -*-
import pygame #@UnresolvedImport
from vec2d import vec2d
import os



class Creep(pygame.sprite.Sprite):
    """Representerar ett fiende-kryp."""
    
    # Static
    explosion_sound = None
    
    def __init__(self, screen, img_filename, init_position,
                 init_direction, speed):
        """Skapar ett nytt kryp.
        
        @param screen: Ytan där krypet ska målas. 
        @param image_filname: Image file för krypet.
        @param init_position: Startposition.
        @param init_direction: Startriktning.
        @param speed: Hastighet i pixels/ms
        
        """
        pygame.sprite.Sprite.__init__(self)
        if Creep.explosion_sound is None:
            # Ladda bara ljudet EN gång, en statisk variabel
            Creep.explosion_sound = pygame.mixer.Sound(os.path.join('sound','bomb_explosion.wav'))
        self.explosion_sound = Creep.explosion_sound
        self.explosion_sound.set_volume(0.2)
        self.health = 5
        self.state = Creep.ALIVE
        self.screen = screen
        self.speed = speed
        self.explosion_image = pygame.image.load(os.path.join('images','boom.png')).convert_alpha()
        self.explosion_timer = 0        
        # Originalbilden
        self.base_image = pygame.image.load(img_filename).convert_alpha()
        # Bilden som skall roteras osv
        self.image = self.base_image
        # Rect behövs för den kolissionshanteringen
        self.rect = self.image.get_rect()
        # Start-position. En vektor
        self.pos = vec2d(init_position)
        # Start-riktning. En normaliserad vektor
        self.direction = vec2d(init_direction).normalized()
        
    
    def is_alive(self):
        return self.state in (Creep.ALIVE, Creep.EXPLODING)
        
    def update(self, time_passed):
        """Updatera creep.
        
        @param time_passed: Den tid i ms som passerat sedan senaste uppdateringen.
        
        """
        if self.state == Creep.ALIVE:
            # Sätt rätt riktning på krypet. Rotate tar ett surface-objekt
            # och riktningen det skall rotera! Mot-urs rotation, så negativa
            # vinklar innebär rotation med-urs. Vi använder en negativ
            # vinkel eftersom xy-planet är inverterat i pygame.
            self.image = pygame.transform.rotate(
                self.base_image, -self.direction.angle)        
            # Beräkna förflyttningen. Riktningen, vilket är en normaliserad
            # vektor multiplicerat med sträckan dvs. hastighet x tiden
            displacement = vec2d(
                self.direction.x * self.speed * time_passed,
                self.direction.y * self.speed * time_passed)
            # Sätt den nya positionen
            self.pos += displacement 
            # Uppdatera dess rect för kollisioner
            self.rect = self.image.get_rect()
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y        
            # Studsa på väggar.
            self.image_w, self.image_h = self.image.get_size()
            # Minska skärmens gränser med krypets höjd och bredd,
            # vilket gör att krypets centrerade position kommer att
            # studsa lite före skärmens gräns. Snyggare
            bounds_rect = self.screen.get_rect().inflate(
                            -self.image_w, -self.image_h)
            # Om utanför vänsterkanten
            if self.pos.x < bounds_rect.left:
                # Sätt pos inte längre än kanten
                self.pos.x = bounds_rect.left
                # Ändra riktningvektorn till andra hållet
                self.direction.x *= -1
            elif self.pos.x > bounds_rect.right:
                self.pos.x = bounds_rect.right
                self.direction.x *= -1
            elif self.pos.y < bounds_rect.top:
                self.pos.y = bounds_rect.top
                self.direction.y *= -1
            elif self.pos.y > bounds_rect.bottom:
                self.pos.y = bounds_rect.bottom
                self.direction.y *= -1
                
        elif self.state == Creep.EXPLODING:
            self.explosion_timer += time_passed
            if self.explosion_timer > 100:
                self.explosion_sound.play()    
                self.state = Creep.DEAD
                self.kill()
        
        elif self.state == Creep.DEAD:
            pass
 
    def draw(self):
        """Ritar krypet på den Surface som angavs vid skapandet."""
        if self.state == Creep.ALIVE:
            # Centrera kryp-bildens position, 
            # eftersom bilden ändrar storlek när den roterar
            draw_pos = self.image.get_rect().move(
                # Sätt dess x-position till halva bildens bredd
                self.pos.x - self.image_w / 2,
                # Sätt dess y-position till halva bildens höjd            
                self.pos.y - self.image_h / 2)
            # Rita kryp-image på screen-image, centrerat 
            self.screen.blit(self.image, draw_pos)
        
        elif self.state == Creep.EXPLODING:
            # Centrera explosionens position, 
            draw_pos = self.explosion_image.get_rect().move(
                # Sätt dess x-position till halva skillnaden
                self.rect.x - abs(((self.image.get_width()-self.explosion_image.get_width()) / 2)),
                # Sätt dess y-position till halva skillnaden            
                self.rect.y - abs(((self.image.get_height()-self.explosion_image.get_height()) / 2)))           
            self.screen.blit(self.explosion_image, draw_pos) 
                   
        
        elif self.state == Creep.DEAD:
            pass
        
    def decrease_health(self, n):
        self.health -= n
        if self.health == 0:
            self.explode()


            
    def explode(self):
        self.state = Creep.EXPLODING
    
    #----------- PRIVATA VARIABLER --------------------------------#
    
    # De tillstånd krypet kan befinna sig i.
    # ALIVE: Krypet åker levand och glad omkring.
    # EXPLODING: En stund bara, före det dör.
    # DEAD: Dött och inaktivt.
    (ALIVE, EXPLODING, DEAD) = range(3)
    
    
    
    
    