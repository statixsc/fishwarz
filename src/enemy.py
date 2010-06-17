# -*- coding: utf-8  -*-
import pygame #@UnresolvedImport
from vec2d import vec2d
import random
from shots import BossShot
from shots import VektorShot
import os

#------------------------------------------------------------------------------------------------------
# Vanliga mobs.
#
#------------------------------------------------------------------------------------------------------ 
class Enemy(pygame.sprite.Sprite):
    """Representerar en fiende."""
    
    # De tillstånd fienden kan befinna sig i .. ie 0, 1 eller 2
    (ALIVE, EXPLODING, DEAD) = range(3)
    # Static
    explosion_sound = None
    
    def __init__(self, screen, img_filename, init_position):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        # Originalbilden
        self.image = pygame.image.load(img_filename).convert_alpha()
        self.explosion_image = pygame.image.load(os.path.join('images','boom.png')).convert_alpha()
        if Enemy.explosion_sound is None:
            # Ladda bara ljudet EN gång, en statisk variabel
            Enemy.explosion_sound = pygame.mixer.Sound(os.path.join('sound','bomb_explosion.wav'))
        self.explosion_sound = Enemy.explosion_sound
        self.explosion_sound.set_volume(0.2)
        # Rect behövs för kolissionshanteringen
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = init_position
        self.state = Enemy.ALIVE  
        self.speed = -3
        self.health = 3
        self.explosion_timer = 0        
    
    def set_speed(self, new_speed):
        self.speed = new_speed
    
    def decrease_health(self, amount):
        """Minskar health med angiven mängd.
        
        Om noll exploderar den.
        
        """
        self.health -= amount
        if(self.health<=0):
            self.state = Enemy.EXPLODING

    def update(self, time_passed):
        """Update metoden kallas varje gång vi itererar spel-loopen.
        
        Förflyttar fienden. Eller uppdatera explosionstimern.
        Exploderar 100 ms, sedan tas fienden bort ur!
        
        """        
        if self.state == Enemy.ALIVE:        
            # Sätt den nya positionen 
            self.rect.move_ip(self.speed, 0)
            if(self.rect.x < -55):
                # Döda den om den hamnar utanför skärmen.
                self.kill()
        elif self.state == Enemy.EXPLODING:
            self.explosion_timer += time_passed
            if self.explosion_timer > 100:
                self.state = Enemy.DEAD
                self.explosion_sound.play()
                self.kill()
        elif self.state == Enemy.DEAD:
            self.kill()
                 
    def show_boundary(self):
        """Vart går gränsen? Ritar en röd ruta vid player rect. 
        
        For testing purposes.
        
        """ 
        pygame.draw.rect(self.screen, pygame.Color('Red'), self.rect, 1)         

    def draw(self):
        """Ritar fienden på skärmen.
        
        Två olika uppritning beroende på state.
        ALIVE
        EXPLOSION
        
        """
        if self.state == Enemy.ALIVE:           
            self.screen.blit(self.image, self.rect)
        elif self.state == Enemy.EXPLODING:
            # Centrera explosionens position, 
            draw_pos = self.explosion_image.get_rect().move(
                # Sätt dess x-position till halva skillnaden
                self.rect.x - abs(((self.image.get_width()-self.explosion_image.get_width()) / 2)),
                # Sätt dess y-position till halva skillnaden            
                self.rect.y - abs(((self.image.get_height()-self.explosion_image.get_height()) / 2)))           
            self.screen.blit(self.explosion_image, draw_pos)
            
#------------------------------------------------------------------------------------------------------
# Taggfisk-boss.
#
#
#------------------------------------------------------------------------------------------------------ 
class BossTaggfiskEnemy(Enemy):
    """Klass för första bossen! Ärver från basklassen Enemy
    
    Har annorlunda hitbox. Bara träff vid munnen.
    Skjuter skott av typen BossShot ..
    Har 100 hp.
    
    """
    def __init__(self, screen, img_filename, init_position):
        Enemy.__init__(self, screen, img_filename, init_position)
        self.arriving = pygame.mixer.Sound(os.path.join('sound','boss_arrive.wav'))
        self.arriving.play()
        self.explosion_image_big = pygame.image.load(os.path.join('images','taggfisk-explosion.png')).convert_alpha()
        self.traffad_image = pygame.image.load(os.path.join('images','taggfisk-mindre_hit.png')).convert_alpha()
        self.stay = False
        self.health = 100
        # Vill ha en separat rect för ritandet
        # Och modifera rect och göra en mindre hitbox.
        self.draw_rect = self.rect
        self.rect = pygame.Rect(self.rect.x, self.rect.y+135, 20, 70)
        self.direction_y = 2
        self.ishurt = False
        self.ishurt_counter = 2
        self.hurtsound = pygame.mixer.Sound(os.path.join('sound','boss_hit.wav'))
        self.shoot_timer = 0
        self.vektor_shoot_timer = 0
        self.shot_grp = pygame.sprite.Group()
        self.vektorshot_grp = pygame.sprite.Group()
        
    def is_dead(self):
        """Kontrollerar bara om bossen är död."""
        return self.health==0
        
    def update(self, time_passed):
        """Kör in bossen och stannar 1/3 in ungefär.
        Då åker den upp och ner istället och skjuter.
        
        Olika update beroende på tillstånd.
        ALIVE
        EXPLODING
        DEAD
        
        """
        if self.state == BossTaggfiskEnemy.ALIVE:
            if self.stay:
                if(self.draw_rect.y > self.screen.get_height()-370):
                    self.direction_y *= -1
                elif(self.draw_rect.y < 10):
                    self.direction_y *= -1
                self.draw_rect.move_ip(0,self.direction_y)
                self.rect.move_ip(0,self.direction_y)
            elif (self.draw_rect.x > 320):
                self.draw_rect.move_ip(-3,0)
                self.rect.move_ip(-3,0)
            else:
                self.stay = True
            # Uppdatera skott-timern!
            self.shoot_timer += time_passed
            self.vektor_shoot_timer += time_passed
            # Varje 700 ms skjuter bossen en blinkande boll!
            if (self.shoot_timer > 700):
                self.shoot_timer = 0
                # Positionen utgår från bossens hitbox = Övre vänstra hörnet av munnen
                # Flyttar den ner 25 px för att skottet skall komma från mitten.
                self.shot_grp.add(BossShot(self.screen, self.rect.x, self.rect.y+25))
            # Ibland skjuter han snett också!
            if (self.vektor_shoot_timer > 400):
                self.vektor_shoot_timer = 0
                self.shot_grp.add(VektorShot(self.screen, 
                                            (self.rect.x, self.rect.y+25),
                                            (-1,
                                            random.uniform(-1,1)),
                                            0.2
                                            ))
                              
        elif self.state == BossTaggfiskEnemy.EXPLODING:
            self.explosion_timer += time_passed
            if self.explosion_timer > 145:
                self.state = Enemy.DEAD
                self.explosion_sound.play()
                self.kill()
        elif self.state == BossTaggfiskEnemy.DEAD:
            self.kill()
                        
    def decrease_health(self, amount):
        """Minskar health."""
        self.hurtsound.play()
        self.health -= amount
        self.ishurt = True
        if(self.health<=0):
            self.state = BossTaggfiskEnemy.EXPLODING
                        
    def draw(self):
        """Har en egen draw för att rita kraftmätare osv.
        
        Olika draw beroende på tillstånd.
        ALIVE
        EXPLODING
        """
        if self.state == BossTaggfiskEnemy.ALIVE:
            
            # Rita låda att den blir träffad
            if self.ishurt:
                self.ishurt_counter -= 1
                self.screen.blit(self.traffad_image, self.draw_rect)
                self.screen.fill(pygame.Color('Red'), self.rect)
                self.screen.blit(self.explosion_image, self.rect.move(0,random.randint(1,40)))
            else: 
                self.screen.blit(self.image, self.draw_rect)            
            if self.ishurt_counter == 0:
                self.ishurt_counter = 3
                self.ishurt = False
            # Rita health bar på 100x20 pixlar 
            health_bar_x = self.draw_rect.x -20
            health_bar_y = self.draw_rect.y 
            self.screen.fill(pygame.Color('red'), 
                               (health_bar_x, health_bar_y, 100, 20))
            self.screen.fill(pygame.Color('green'), 
                               (health_bar_x, health_bar_y, 
                                    self.health, 20))
        # Rita stor explosion!
        elif self.state == BossTaggfiskEnemy.EXPLODING:
            self.screen.blit(self.explosion_image_big, self.draw_rect)
            
#------------------------------------------------------------------------------------------------------
# Bläckfisk-boss.
#
#
#------------------------------------------------------------------------------------------------------        
class BossBlackfiskEnemy(BossTaggfiskEnemy):
    
    def __init__(self, screen, img_filename, init_position):
        BossTaggfiskEnemy.__init__(self, screen, img_filename, init_position)
        self.traffad_image = pygame.image.load(os.path.join('images','bigger_blackfisk_hit.png')).convert_alpha()
        self.rect = pygame.Rect(self.rect.x, self.rect.y-30, 20, 120)
    
    def update(self, time_passed):
        """Kör in bossen och stannar 1/3 in ungefär.
        Då åker den upp och ner istället och skjuter.
        
        Olika update beroende på tillstånd.
        ALIVE
        EXPLODING
        DEAD
        
        """
        if self.state == BossBlackfiskEnemy.ALIVE:
            if self.stay:
                if(self.draw_rect.y > self.screen.get_height()-370):
                    self.direction_y *= -1
                elif(self.draw_rect.y < 10):
                    self.direction_y *= -1
                self.draw_rect.move_ip(0,self.direction_y)
                self.rect.move_ip(0,self.direction_y)
            elif (self.draw_rect.x > 320):
                self.draw_rect.move_ip(-3,0)
                self.rect.move_ip(-3,0)
            else:
                self.stay = True
            # Uppdatera skott-timern!
            self.vektor_shoot_timer += time_passed
            # Skjut! om dags
            if (self.vektor_shoot_timer > 2000):
                self.vektor_shoot_timer = 0
                # Sprayar skott!
                for y in self.frange(-1, 1, 0.20):                    
                    self.shot_grp.add(VektorShot(self.screen, 
                                                (self.rect.x+200, self.rect.y+55),
                                                (-1, y),
                                                0.2
                                                ))
                              
        elif self.state == BossBlackfiskEnemy.EXPLODING:
            self.explosion_timer += time_passed
            if self.explosion_timer > 145:
                self.state = Enemy.DEAD
                self.explosion_sound.play()
                self.kill()
        elif self.state == BossBlackfiskEnemy.DEAD:
            self.kill()
        
    def draw(self):
        """Har en egen draw för att rita kraftmätare osv.
        
        Olika draw beroende på tillstånd.
        ALIVE
        EXPLODING
        """
        if self.state == BossTaggfiskEnemy.ALIVE:
            
            # Rita annan bild om den blir träffad
            if self.ishurt:
                self.ishurt_counter -= 1
                self.screen.blit(self.traffad_image, self.draw_rect)
                self.screen.blit(self.explosion_image, self.rect.move(0,random.randint(1,80)))
            else:
                self.screen.blit(self.image, self.draw_rect)
                            
            if self.ishurt_counter == 0:
                self.ishurt_counter = 3
                self.ishurt = False
            # Rita health bar på 100x20 pixlar 
            health_bar_x = self.draw_rect.x -20
            health_bar_y = self.draw_rect.y 
            self.screen.fill(pygame.Color('red'), 
                               (health_bar_x, health_bar_y, 100, 20))
            self.screen.fill(pygame.Color('green'), 
                               (health_bar_x, health_bar_y, 
                                    self.health, 20))
        # Rita stor explosion!
        elif self.state == BossTaggfiskEnemy.EXPLODING:
            self.screen.blit(self.explosion_image_big, self.draw_rect)
            
    def frange(self, start, end=None, inc=None):
        """Som range fast, decimala increments..."""
        
        if end == None:
            end = start + 0.0
            start = 0.0
        
        if inc == None:
            inc = 1.0
        
        L = []
        while 1:
            next = start + len(L) * inc
            if inc > 0 and next >= end:
                break
            elif inc < 0 and next <= end:
                break
            L.append(next)
           
        return L
   
   