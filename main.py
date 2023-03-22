# Import 
from numpy import left_shift
import pygame, sys
from os import path
from pygame.event import get
from player import Player
import obstacle
from alien import Alien
from alien import Extra
from random import choice
from random import randint
from laser import Laser
from alienlaser import AlienLaserClass
import time
import numpy as np

game_index = 0
award_index = False

# Path Function
def getFile(fileName):
    return path.join(path.dirname(__file__), fileName)

# Game Class 
class Game():
    def __init__(self):

        # Player Setup
        player_sprite = Player((screen_width/2, screen_height-10), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Title Setup
        self.title_surf = pygame.image.load(getFile('graphics/Title.png')).convert_alpha()
        self.title_rec = self.title_surf.get_rect(center = (screen_width/2,screen_height - (screen_height*.85)))

        # Health & Score Setup
        self.lives = 3
        self.live_surface = pygame.image.load(getFile('graphics/player/player_1.png')).convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surface.get_size()[0] * 2 + 20 )
        self.score = 0
        self.extra_score = 0
        self.obstacle_score = 0
        self.font = pygame.font.Font(getFile('font/8bit.ttf'), 8)
        self.font_title = pygame.font.Font(getFile('font/8bit.ttf'), 20)
        self.font_main_menu = pygame.font.Font(getFile('font/8bit.ttf'), 15)
        self.font_giant = pygame.font.Font(getFile('font/8bit.ttf'), 50)
        self.font_gianter = pygame.font.Font(getFile('font/8bit.ttf'), 60)


        # Obstacle Setup 
        self.shape = obstacle.shape 
        self.block_size = 6
        self.blockgroup = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_load_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 500)


        # Alien Setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        # Extra Alien Setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_rate = randint(500,900)

    def name_screen(self):
            
            # Alien Laser Sound
            pygame.mixer.Sound.stop(alien_laser_sound)
            
            # BG Fill
            screen.fill((18, 92, 19))

            # Name Title
            message_surf_1 = self.font_giant.render('Name', False,(62, 124, 23))
            message_rect_1 = message_surf_1.get_rect(center = (screen_width/2, screen_height/3))

            # Name
            player_name_rect = pygame.Rect(0, screen_height/2, 600, 150)
            player_name_rect_color = pygame.Color(64, 124, 23, 255)
            global text_surf_small
            global text_surf_small_rect 
            text_surf = self.font_gianter.render(player_name, True, (232, 225, 217))
            text_surf_small = self.font.render(f'Player: {player_name}', True, (236,235,231))
            text_surf_small_rect = text_surf_small.get_rect(bottomleft = (10,screen_height-10))

            # Scores 
            


            
            # Show
            pygame.draw.rect(screen, player_name_rect_color, player_name_rect)
            screen.blit(message_surf_1, message_rect_1)
            if time.time() % .8 > 0.2:
                screen.blit(text_surf,(player_name_rect.x + 100 , player_name_rect.y + 20))

            # Back 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                global game_index
                game_index = 0         
        
    def main_menu(self):
                global player_name
                player_name = ''

                # Alien Laser Sound
                pygame.mixer.Sound.stop(alien_laser_sound)

                # Play
                message_surf_1 = self.font_main_menu.render('Play', False,(255, 248, 243))
                message_rect_1 = message_surf_1.get_rect(center = (screen_width/2, screen_height/2.3))
                message_surf_2 = self.font.render('(P)', False,(103, 111, 163))
                message_rect_2 = message_surf_2.get_rect(center = (screen_width/2 - 60, screen_height/2.3))
                
                # High Scores
                message_surf_3 = self.font_main_menu.render('High Scores', False,(255, 248, 243))
                message_rect_3 = message_surf_3.get_rect(center = (screen_width/2, screen_height/2))
                message_surf_4 = self.font.render('(H)', False,(103, 111, 163))
                message_rect_4 = message_surf_4.get_rect(center = (screen_width/2 - 120, screen_height/2))

                # Exit
                message_surf_5 = self.font_main_menu.render('Exit', False,(255, 248, 243))
                message_rect_5 = message_surf_5.get_rect(center = (screen_width/2, screen_height/1.75))
                message_surf_6 = self.font.render('(X)', False,(103, 111, 163))
                message_rect_6 = message_surf_6.get_rect(center = (screen_width/2 - 60, screen_height/1.75))

                
                # Show BG
                screen.fill((15, 14, 14))

                # Show surfaces
                screen.blit(self.title_surf, self.title_rec)
                screen.blit(message_surf_1,message_rect_1)
                screen.blit(message_surf_2,message_rect_2)
                screen.blit(message_surf_3, message_rect_3)
                screen.blit(message_surf_4, message_rect_4)
                screen.blit(message_surf_5, message_rect_5)
                screen.blit(message_surf_6, message_rect_6)

                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p]:
                    global game_index
                    game_index = 1
                if keys[pygame.K_x]:
                    pygame.QUIT()
                    exit()
                if keys[pygame.K_h]:
                    game_index = 5
                    self.read_score()
   
    def save_score(self):
        with open(getFile('scores.txt'), "a") as file_scores:
            file_scores.write(str(player_name) + ' ' + f'{self.score}\n')

    def read_score(self):
        with open(getFile('scores.txt'), "r") as file_scores:
            lines = file_scores.readlines()[1:]

        global score_list
        global name_list
        name_list = []
        score_list = []
        for line in lines:
            value = line.split(' ')
            name_list.append(value[0])
            score_list.append(value[1][:-1])
            length_list = len(name_list)
        print(score_list)
        print(name_list)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 50, x_offset= 70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0: 
                    alien_sprite = Alien('green', x, y)
                elif 1 <= row_index <= 2: 
                    alien_sprite = Alien('yellow', x, y)
                else: 
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)
    
    def alien_position_check(self): 
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(1)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance 

    def alien_shoot(self): 
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = AlienLaserClass(random_alien.rect.center, 8, screen_height)
            self.alien_lasers.add(laser_sprite)
            
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block  = obstacle.Block(self.block_size, (161, 51, 51),x,y)
                    self.blockgroup.add(block)

    def create_load_obstacles(self, *offset, x_start, y_start,):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def extra_alien_timer(self):
        self.extra_spawn_rate -= 1
        if self.extra_spawn_rate <= 0 :
            self.extra.add(Extra(choice(['right','left']), screen_width))
            self.extra_spawn_rate = randint(400,800)
            
    def collision_check(self):
        # Player Lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Obstacles
                if pygame.sprite.spritecollide(laser, self.blockgroup, True):
                    laser.kill()
                # Aliens
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                        self.extra_score += alien.value
                        self.obstacle_score += alien.value
                    alien_dead_sound = pygame.mixer.Sound(getFile('audio/alienhit.mp3'))
                    alien_dead_sound.play()
                    laser.kill()
                # Extra Alien
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 200
                    laser.kill()  

        # Alien Lasers
        if self.alien_lasers: 
            for laser in self.alien_lasers: 

                # Obstacles
                if pygame.sprite.spritecollide(laser, self.blockgroup, True):
                    laser.kill()

                # Player
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.death_screen()
        # Alien 
        if self.aliens:
            for alien in self.aliens: 
                pygame.sprite.spritecollide(alien, self.blockgroup, True)
                if pygame.sprite.spritecollide(alien, self.player, True):
                    global game_index
                    game_index = 4

    def display_lives(self): 
        for live in range(self.lives - 1): 
            x = self.live_x_start_pos - (live * (self.live_surface.get_size()[0] + 3))
            screen.blit(self.live_surface,(x - 10,8))

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', False, (236,235,231))
        score_rect = score_text.get_rect(topleft = (0,0))
        screen.blit(score_text,score_rect)

    def extra_life(self):
        if self.extra_score >= 1500:
            self.extra_score = 0
            self.lives += 1
        if self.obstacle_score >= 3500:
            self.obstacle_score = 0
            self.blockgroup.empty()
            self.create_load_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 500)
 
    def no_aliens(self):
        if not self.aliens.sprites():
            global game_index
            game_index = 3

    def no_lives(self):
        if self.lives == 0: 
            global game_index
            game_index = 4

    def end_screen(self):

        # Pauses all sounds
        pygame.mixer.pause()
        
        # Fill Screen 
        screen.fill((46, 76, 109)) 

        # Text Surfaces & Rectangles
        victory_surface = self.font_title.render('Round Over!', False, 'white')
        victory_rect = victory_surface.get_rect(center = (screen_width/2, screen_height/2))
        message_surf_1 = self.font.render('Press P to keep playing.', False, 'white')
        message_rect_1 = message_surf_1.get_rect(center = (screen_width/2, screen_height/2 + 50))
        message_surf_2 = self.font.render('Press X to exit.', False, 'white')
        message_rect_2 = message_surf_1.get_rect(center = (screen_width/2, screen_height/2 + 100))

        # Text Drawing
        screen.blit(victory_surface,victory_rect)
        screen.blit(message_surf_1, message_rect_1)
        screen.blit(message_surf_2, message_rect_2)  

        # Keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            global game_index
            game_index = 2
            pygame.mixer.unpause()
            self.alien_setup(rows = 6, cols = 8)
            self.run()
        if keys[pygame.K_x]:
            self.save_score()
            global player_name
            player_name = ''
            game_index = 0
            self.score = 0

    def death_screen(self):
        
        # Alien Laser Sound
        pygame.mixer.Sound.stop(alien_laser_sound)

        # Screen Fill
        screen.fill((155, 0, 0))

        # Messages
        message_surf_1 = self.font_title.render('YOU DIED', False, 'black')
        message_rect_1 = message_surf_1.get_rect(center = (screen_width/2, screen_height/2 + 100))
        message_surf_2 = self.font_title.render('Press P to try again', False, (44, 39, 46))
        message_rect_2 = message_surf_2.get_rect(center = (screen_width/2, screen_height/2 + 160))

        # Draw Messages
        screen.blit(message_surf_1, message_rect_1)
        screen.blit(message_surf_2, message_rect_2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.save_score()
            pygame.mixer.Sound.play(alien_laser_sound)
            global player_name
            global game_index
            player_name = ''
            game_index = 1
            self.lives = 3
            self.score = 0
            self.aliens.empty()
            self.alien_lasers.empty()
            self.blockgroup.empty()
            self.create_load_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 500)
            self.alien_setup(6,8)

    def display_name(self):
        screen.blit(text_surf_small, text_surf_small_rect)
        
    def high_score_screen(self):
        
        # Alien Laser Sound
        pygame.mixer.Sound.stop(alien_laser_sound)
        
        # Screen Fill
        screen.fill('black')

        # Sorted Lists
        list_index = np.argsort(score_list)[::-1]
        sorted_name_list = np.array(name_list)[list_index]
        sorted_score_list = np.array(score_list)[list_index]


        # Variables
        for index in range(len(name_list)):
            name_surf = self.font_title.render(sorted_name_list[index], False,(62, 124, 23))
            name_rect = name_surf.get_rect(center = (screen_width/3, screen_height*(0.1*(index + 1 ))))
            score_surf = self.font_title.render(sorted_score_list[index], False,(62, 124, 23))
            score_rect = score_surf.get_rect(center = (screen_width - screen_width/3, screen_height*(0.1*(index + 1))))
            screen.blit(score_surf, score_rect)
            screen.blit(name_surf, name_rect)
            if index >= 8:
                break



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            global game_index
            game_index = 0

        if keys[pygame.K_SPACE]:
            print(sorted_score_list)
            print(sorted_name_list)

    def run(self):
        # Updates 
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        self.extra.update()

        # Checkers & Timers
        self.alien_position_check()
        self.extra_alien_timer()
        self.collision_check()


        # Player
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        # Obstacles
        self.blockgroup.draw(screen)

        # Aliens
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)

        # Extra Alien 
        self.extra.draw(screen)

        # Lives 
        self.display_lives()
        self.display_score()
        self.extra_life()
        self.display_name()

        # Victory Screen & Death Screen
        self.no_aliens()
        self.no_lives()

# CRT Effect Class
class CRT_Effect:
    def __init__(self):
        self.tv = pygame.image.load(getFile('graphics/tv.png')).convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width,screen_height))

    def create_lines(self):
        line_height = 3
        line_amount = int(screen_height/line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black',(0,y_pos),(screen_width, y_pos) ,1)

    def draw(self):
        self.tv.set_alpha(randint(75,100))
        self.create_lines()
        screen.blit(self.tv,(0,0))


        
# Main Loop
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Space Invaders')
    screen_width = 600 
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT_Effect()
    icon = pygame.image.load(getFile('graphics/icon.png'))
    player_name = ''
    pygame.display.set_icon(icon)

    AlienLaser = pygame.USEREVENT + 1
    pygame.time.set_timer(AlienLaser, 600)

    # Image Import
    BG = pygame.image.load(getFile('graphics/bg/static_bg.png')).convert()
    shot = pygame.image.load(getFile('graphics/player/player_4.png')).convert_alpha()
    shot = pygame.transform.scale(shot, (36,42))

    # Sound Import 
    alien_laser_sound = pygame.mixer.Sound(getFile('audio/alienlaser.aiff'))
    key_sound = pygame.mixer.Sound(getFile('audio/key.mp3'))
    error_sound = pygame.mixer.Sound(getFile('audio/error.aiff'))
    backspace_sound = pygame.mixer.Sound(getFile('audio/backspace.mp3'))
    click_sound = pygame.mixer.Sound(getFile('audio/click.mp3'))
    

    



    while True: 
        # Draw CRT Effect
        crt.draw()

        # Screen Update
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                sys.exit()
            if event.type == AlienLaser:
                game.alien_shoot()
                alien_laser_sound.set_volume(0.3)
                alien_laser_sound.play()
            if game_index == 1:
                if len(player_name) <= 5:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            pygame.mixer.Sound.play(backspace_sound)
                            player_name = player_name[:-1]
                        elif event.key == pygame.K_CAPSLOCK:
                            pygame.mixer.Sound.play(click_sound)
                        elif event.key == pygame.K_RETURN and len(player_name) == 5:
                            game_index = 2
                        elif event.key == pygame.K_RETURN:
                            pygame.mixer.Sound.play(error_sound)
                        elif event.key == pygame.K_SPACE:
                            player_name = player_name[:-1]
                            pygame.mixer.Sound.play(error_sound)
                        else:
                            pygame.mixer.Sound.play(key_sound)
                            player_name += event.unicode
                else: 
                    player_name = player_name[:-1]
        if game_index == 0:
            # Reset Screen
            screen.fill([0, 0, 0])
            game.main_menu()
        elif game_index == 1:
            # Reset Screen
            screen.fill([0, 0, 0])
            game.name_screen()
        elif game_index == 2:

            # Reset Screen
            screen.fill([0, 0, 0])

            # Static background
            screen.blit(BG, (0,0))        

            # Run Game
            game.run()
        elif game_index == 3: 
            # Reset Screen
            screen.fill([0, 0, 0])
            game.end_screen()
        elif game_index == 4:
            # Reset Screen
            screen.fill([0, 0, 0])
            game.death_screen()
        elif game_index == 5:
            screen.fill([0, 0, 0])
            game.high_score_screen()











