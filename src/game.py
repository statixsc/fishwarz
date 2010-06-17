# -*- coding: utf-8  -*-
import pygame #@UnresolvedImport
from pygame.locals import *
from vec2d import vec2d
from enemy import Enemy
from enemy import BossBlackfiskEnemy
from enemy import BossTaggfiskEnemy
from player import PlayerShip
from shots import BaseShot
from powerup import Powerup
import random
import sys
import time
from powerup import Powerup
from creep import Creep
import os


class Game(object):
    
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    SCORE_RECT = pygame.Rect(10, 10, 150, 60)
    
    def __init__(self):
        """Startar spelet.
        
        Laddar ljud och grafik.
        
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption('Fishwars > Intro') 
        # Ladda ljud
        pygame.mixer.music.load(os.path.join('sound','soundtrack.mp3'))
        # Volym anges mellan 0 och 1              
        pygame.mixer.music.set_volume(0.5)  
        pygame.mixer.music.play(-1)
        self.coin = pygame.mixer.Sound(os.path.join('sound','102_coin.wav'))
        self.coin.set_volume(0.3)
        self.bubble = pygame.mixer.Sound(os.path.join('sound','bubbla_liten.wav'))
        # Ladda grafik
        self.clock = pygame.time.Clock()
        self.my_font = pygame.font.SysFont('arial', 20)
        self.intropic = pygame.image.load(os.path.join('images','intro.png'))
        self.background_image = pygame.image.load(os.path.join('images','sea-background.jpg'))
        self.foreground_image = pygame.image.load(os.path.join('images','foreground.png'))
        self.fore_foreground_image = pygame.image.load(os.path.join('images','fore_foreground.png'))           
        
    def quit(self):
        """Avslutar spelet."""
        pygame.quit()
        sys.exit()

    def initialize(self):
        """Skapar alla objekt och nollställer bakgrunder osv."""
        pygame.display.set_caption('Fishwars > Gogo! ^^')        
        # Spel inställningar
        self.paused = False
        self.player_score = 0
        # Skapa grupper för fiender
        self.enemy_grp = pygame.sprite.Group()
        self.bonus_enemy_grp = pygame.sprite.Group()
        self.spawn_bonus_monsterfiskar()
        self.creeps = pygame.sprite.Group()
        # Skapa spelaren
        self.player = PlayerShip(self.screen)
        self.player_grp = pygame.sprite.Group()
        # För att hantera kollisioner
        self.player_grp.add(self.player)
        # Powerups!
        self.powerup_grp = pygame.sprite.Group()
        font = pygame.font.SysFont('Arial Black', 80)
        self.gameOverImage = font.render("GAME OVER", True, (255,0,0))
        self.woo = font.render("YOU WIN! :)", True, (0,255,0))
        self.wooo = font.render("WELL DONE!", True, (0,255,0))
        mindre_font = pygame.font.SysFont('Arial Black', 25)
        self.gameOverRetry = mindre_font.render("Back to main menu? [y/n]", True, (255,0,0))
        # Nollställ alla bakgrunder
        self.bg_x = 0
        self.fg_x = 0
        self.ffg_x = 0
        
    def spawn_bonus_monsterfiskar(self):
        """Spawnar fem stycken fiskar man kan få powerups av!
        De kommer i rad med 50 px mellan varje.
        
        """
        random_y = random.randint(0,self.SCREEN_HEIGHT-100)
        x = self.SCREEN_WIDTH
        for i in range(5):
            self.bonus_enemy_grp.add(Enemy(screen=self.screen,
                               img_filename=os.path.join('images','monsterfisk.png'),
                               init_position=(x, random_y) 
                               ))
            # Nästa fiende lite åt sidan
            x += 50

    def spawn_monster(self, antal, pref=None, lila=None):
        """Spawnar vanliga mobs.
        
        @param antal: Hur många mobs
        @param pref: Vilken typ 
        
        """
        x = self.SCREEN_WIDTH
        all_monsters = [os.path.join('images','dygaddaa.png'),
                        os.path.join('images','taggfisk.png'),
                        os.path.join('images','monsterfisk.png'),
                        os.path.join('images','taggfisk-blue.png'),
                        os.path.join('images','taggfisk-green.png')]
        if pref:
            img = all_monsters[pref]
        elif lila:
            img = os.path.join('images','taggfisk-lila.png')
        else:
            img = random.choice(all_monsters)
        for i in range(antal):
            random_y = random.randint(0,self.SCREEN_HEIGHT-100)
            temp = Enemy(screen=self.screen,
                                   img_filename=img,
                                   init_position=(x, random_y) 
                                   )
            temp.set_speed(random.randint(-7, -3))
            self.enemy_grp.add(temp)
            # Nästa fiende lite åt sidan
            x += 60         
                
    def spawn_creeps(self):
        """Spawnar ett studsande kryp.
        Random riktning vid initialisering.
        
        """
        random_y = random.randint(0,self.SCREEN_HEIGHT-100)
        self.creeps.add(Creep(self.screen,
                    os.path.join('images','new_creep.png'),
                    # Position
                    (   self.SCREEN_WIDTH, random_y),
                    # Riktning
                    (   random.choice([-1, -0.7]),
                        random.choice([-0.7, 0, 0.7])),
                    # Hastighet
                    0.1))        

    def draw_instructions(self):
        """Ritar upp spelets instruktioner.
        Aktiveras mha space-tangenten vid startskärmen.        
        
        """
        INSTR_RECT = pygame.Rect(20, 240, 200, 205)
        # Rita den vit-transparenta lådan
        transparent_box = pygame.Surface((INSTR_RECT.w, INSTR_RECT.h))
        transparent_box.fill(pygame.Color(255, 255, 255))
        transparent_box.set_alpha(50)
        self.screen.blit(transparent_box, INSTR_RECT)
        # Rita instruktionerna
        my_font = pygame.font.SysFont('arial', 20)        
        INSTR_RECT = INSTR_RECT.move(10, 5)
        instructions = ['Instructions:',
                        '[w] up',
                        '[a] left',
                        '[s] right',
                        '[d] down',
                        '[Enter] shoot',
                        '[Space] pause',
                        '[Escape] exit']
        for instruction in instructions:
            msg = my_font.render(instruction, True, pygame.Color('white'))
            self.screen.blit(msg, INSTR_RECT)
            # Flytta positionen nedåt för nästa instruktion
            INSTR_RECT = INSTR_RECT.move(0, msg.get_height())

    def draw_rimmed_box(self, box_rect, box_color, 
                        rim_width=0, 
                        rim_color=pygame.Color('black')):
        """ Ritar en streckad låda. Strecket ritas utanför lådan."""
        if rim_width:
            # Räkna ut streckets kanter
            rim_rect = pygame.Rect(box_rect.left - rim_width,
                            box_rect.top - rim_width,
                            box_rect.width + rim_width * 2,
                            box_rect.height + rim_width * 2)
            # Och rita strecket
            pygame.draw.rect(self.screen, rim_color, rim_rect)
        # Därefter rita själva lådan
        pygame.draw.rect(self.screen, box_color, box_rect)    

    def draw_score(self):
        """Ritar upp spelarens score i vänstra hörnet."""
        score = 'Score: ' + str(self.player_score)
        score_msg = self.my_font.render(score, True, pygame.Color('white'))
        self.screen.blit(score_msg, self.SCORE_RECT)

    def intro(self):
        """Spelets intro loop.
        
        Spelar musik. Visar logo, om man trycker space visas 
        instruktioner. Enter för att starta spelet!
        
        """
        show_instructions = False
        while True:
            # Sätt spelet till 30 FPS
            time_passed = self.clock.tick(30)
            # Kontrollera spelarens input        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()    
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.locals.K_ESCAPE: 
                        self.quit() 
                    elif event.key == pygame.K_SPACE: 
                        show_instructions = not show_instructions
                    elif event.key == pygame.locals.K_RETURN:
                        self.coin.play()
                        # Den spelar långsamt.. så vänta lite
                        time.sleep(1)
                        self.initialize()
                        self.run()
            # Rita introbilden
            self.screen.blit(self.intropic, (0, 0))
            # Om spelaren vill se instruktiner, rita de över
            if show_instructions:
                self.draw_instructions()
            # Uppdatera skärmen sist
            pygame.display.flip()
        
    def run(self):
        """Spelets main loop."""
        timer = 0
        bosstimer = 0
        creep_timer = 0
        self.bosstime = False
        self.bonus_active = False
        self.bonus_done = False
        self.big_bad_boss = None
        self.phase_two = False
        self.second_boss = False
        self.other_boss = None
        bonus_timer = 0 
        
        while True:
            # Limit frame speed to 30 FPS
            time_passed = self.clock.tick(30) 
            timer += time_passed
            bosstimer += time_passed
            bonus_timer += time_passed
            creep_timer += time_passed
            
            # Kolla spel-timers
            # TODO! NGT SNYGGARE UTAN ALLA IFSATSER!
            # Gör random monster varje sekund!
            if(timer>1000 and not self.bosstime and not self.second_boss):
                r = random.randint(0,100)
                # Chans att nytt monster spawnar varje sekund!
                if(r<65):
                    self.spawn_monster(1)
                    timer = 0
            # Bonus efter X sekunder
            if(bonus_timer>13000 and not self.player.power==5 and not self.bosstime):
                self.spawn_bonus_monsterfiskar();
                bonus_timer = 0
            # BOSS EFTER 20 SEKUNDER
            if(bosstimer>20000 and not self.bosstime and not self.phase_two):
                y = 50
                x = self.SCREEN_WIDTH
                self.bosstime = True
                self.big_bad_boss = BossTaggfiskEnemy(screen=self.screen,
                                   img_filename=os.path.join('images','taggfisk-mindre.png'),
                                   init_position=(x, y))
                self.enemy_grp.add(self.big_bad_boss)
                bosstimer = 0
            # IF BOSS MAKE EXTRA MOBS
            if(timer>1000 and self.bosstime):
                r = random.randint(0,100)
                if(r<25):
                    self.spawn_monster(1, 1)
                    timer = 0
            # CHECK IF BOSS DEAD
            if(self.big_bad_boss and self.big_bad_boss.is_dead() and self.bosstime):
                self.bosstime = False
                self.phase_two = True
                bosstimer = 0
            # Och x sekunder efter första bossen dör kommer nästa!
            if bosstimer > 20000 and self.phase_two and not self.second_boss:
                self.second_boss = True
                y = 50
                x = self.SCREEN_WIDTH
                self.other_boss = BossBlackfiskEnemy(screen=self.screen,
                                   img_filename=os.path.join('images','bigger_blackfisk.png'),
                                   init_position=(x, y))
                self.enemy_grp.add(self.other_boss)   
            if creep_timer>1000 and self.phase_two and not self.second_boss:
                r = random.randint(0,100)
                # 25% chans att nytt monster spawnar varje sekund!
                if(r<25):
                    self.spawn_creeps()
                    creep_timer = 0
                r_lila = random.randint(0, 100)
                if(r_lila<5):
                    self.spawn_monster(1, lila=True)       
            if self.other_boss:
                if self.other_boss.is_dead():
                    self.endloop()        
                
            # KONTROLLERA PLAYER INPUT ----------------------------------------    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()    
                elif event.type == pygame.KEYDOWN: 
                    # Om Escape - avsluta spelet
                    if event.key == pygame.locals.K_ESCAPE: 
                        self.quit()
                    # Skeppets rörelse
                    elif event.key == pygame.locals.K_a: 
                        self.player.x = -6
                    elif event.key == pygame.locals.K_d: 
                        self.player.x = 6
                    elif event.key == pygame.locals.K_w: 
                        self.player.y = -6 
                    elif event.key == pygame.locals.K_s: 
                        self.player.y = 6 
                    # Om return - Spela ljud och avfyra vapnet!                        
                    elif event.key == pygame.locals.K_RETURN:
                        self.bubble.play()
                        self.player.fire_weapon()
                # Om uppknapp - sluta röra skeppet                             
                elif event.type == pygame.locals.KEYUP:
                    if event.key == pygame.locals.K_a:
                        self.player.x = 0
                    elif event.key == pygame.locals.K_d:
                        self.player.x = 0
                    elif event.key == pygame.locals.K_w:
                        self.player.y = 0
                    elif event.key == pygame.locals.K_s:
                        self.player.y = 0
   
            # UPPDATERA ALLA OBJEKT -------------------------------------------
            self.player_grp.update()
            self.player.playershots_grp.update()
            self.powerup_grp.update(time_passed)
            self.bonus_enemy_grp.update(time_passed)            
            self.enemy_grp.update(time_passed)
            if self.big_bad_boss:
                self.big_bad_boss.shot_grp.update(time_passed)
            if self.other_boss:
                self.other_boss.shot_grp.update(time_passed)                
            for creep in self.creeps:
                creep.update(time_passed)                
            # Förflytta bakgrunderna x pixlar vänster/uppdatering
            self.bg_x -= 0.5
            self.fg_x -= 2
            self.ffg_x -= 2.5
            # Om hela bakgrunden spelats upp, börja om
            # !TODO VERKAR INTE FUNGERA!
            if(self.bg_x==-4167):
                print "change bg"
                self.bg_x = 0
            if(self.fg_x==-8000):
                print "change fg"
                self.fg_x = 0
               
            # KONTROLLERA KOLLISIONER ----------------------------------------
            for hit in pygame.sprite.groupcollide(self.player_grp, self.enemy_grp, 1, 1):
                self.game_over()
            for hit in pygame.sprite.groupcollide(self.player_grp, self.bonus_enemy_grp, 1, 1):
                self.game_over()
            for hit in pygame.sprite.groupcollide(self.player_grp, self.creeps, 1, 1):
                self.game_over()                
            if self.big_bad_boss:
                for hit in pygame.sprite.groupcollide(self.player_grp, self.big_bad_boss.shot_grp, 1, 1):
                    self.game_over()
            if self.other_boss:
                for hit in pygame.sprite.groupcollide(self.player_grp, self.other_boss.shot_grp, 1, 1):
                    self.game_over()                    
            # Kontrollera kollisioner fiende/player-skott
            for enemy in pygame.sprite.groupcollide(self.enemy_grp, self.player.playershots_grp, 0, 1):
                self.player_score += 1000
                enemy.decrease_health(1)
            for enemy in pygame.sprite.groupcollide(self.creeps, self.player.playershots_grp, 0, 1):
                self.player_score += 1000
                enemy.decrease_health(1)
            # Kontrollera kollisioner bonus/player-skott
            for enemy in pygame.sprite.groupcollide(self.bonus_enemy_grp, self.player.playershots_grp, 0, 1):
                # Ge spelaren poäng
                self.player_score += 1000
                # Och skada fienden
                enemy.decrease_health(1)
                if len(self.bonus_enemy_grp)==1 and not self.bonus_active:
                    self.bonus_active = True
                    self.powerup_grp.add(Powerup(self.screen, (enemy.rect.x, enemy.rect.y)))
            # Kontrollera kollisioner bonus/spelaren
            for powerup in pygame.sprite.groupcollide(self.powerup_grp, self.player_grp, 1, 0):
                powerup.powerup_sound.play()   
                self.bonus_active = False
                self.player.power += 2
                
            # RITA ALLA OBJEKT ------------------------------------------------ 
            # Bakgrunden måste ritas först = längst bak
            self.screen.blit(self.background_image, (self.bg_x, 0))
            self.screen.blit(self.foreground_image, (self.fg_x, 0))
            self.player_grp.draw(self.screen)
            self.powerup_grp.draw(self.screen)
            for creep in self.creeps:
                creep.draw()
            for enemy in self.bonus_enemy_grp:
                enemy.draw()            
            for enemy in self.enemy_grp:
                enemy.draw()
            if self.big_bad_boss:
                for shot in self.big_bad_boss.shot_grp:
                    shot.rita()
            if self.other_boss:
                for shot in self.other_boss.shot_grp:
                    shot.rita()                    
            self.player.playershots_grp.draw(self.screen)
            # Växter i förgrunden! ^__^
            self.screen.blit(self.fore_foreground_image, (self.ffg_x, 0))
            self.draw_score()            
            
            # BOUNDARY TEST            
            #self.player.show_boundary()
            #for shot in self.playershots_grp:
            #    shot.show_boundary()
            #for enemy in self.enemy_grp:
            #   enemy.show_boundary()
            
            # Flippa displayen
            pygame.display.flip()

    def game_over(self):
        """Game over loop."""
        while True:
            # Kontrollera player inputs       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()    
                elif event.type == pygame.KEYDOWN: 
                    # Om Escape - avsluta spelet
                    if event.key == pygame.locals.K_ESCAPE: 
                        self.quit()
                    elif event.key == pygame.locals.K_y:
                        self.intro()
                    elif event.key == pygame.locals.K_n:
                        self.quit()                 
            self.screen.blit(self.gameOverImage, (45,170))
            self.screen.blit(self.gameOverRetry, (135,280))
            pygame.display.flip()    
            
    def endloop(self):
        """End loop."""
        while True:
            # Kontrollera player inputs       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()    
                elif event.type == pygame.KEYDOWN: 
                    # Om Escape - avsluta spelet
                    if event.key == pygame.locals.K_ESCAPE: 
                        self.quit()
                    elif event.key == pygame.locals.K_y:
                        self.intro()
                    elif event.key == pygame.locals.K_n:
                        self.quit()                 
            self.screen.blit(self.woo, (45,100))
            self.screen.blit(self.wooo, (45,190))
            pygame.display.flip()         

def main():
    game = Game()
    game.intro()
    
if __name__=="__main__":
    main()