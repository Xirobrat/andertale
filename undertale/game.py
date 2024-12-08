import pygame
import sys
from random import randint


lost = 0

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.speed = player_speed
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):

    def update(self, win_width):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 25:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < 570:
            self.rect.y += self.speed

        if keys[pygame.K_x]:
            self.pause = True


        if keys[pygame.K_z]:
            self.pause = False



class Enemy(GameSprite):
    def update(self, win_height, win_width):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            global lost
            lost += 1
            self.rect.y = -40
            self.rect.x = randint(0, win_width - 80)

class Enemy2(GameSprite):
    def update(self, win_height, win_width):
        self.rect.y -= self.speed

        if self.rect.y <= -40:
            global lost
            lost += 1
            self.rect.y = 640
            self.rect.x = randint(0, win_width - 80)

class Enemy3(GameSprite):
    def update(self, win_height, win_width):
        self.rect.x -= self.speed

        if self.rect.x <= -40:
            global lost
            lost += 1
            self.rect.x = 740
            self.rect.y = randint(0, win_height - 60)

class Enemy4(GameSprite):
    def update(self, win_height, win_width):
        self.rect.x += self.speed

        if self.rect.x >= 740:
            global lost
            lost += 1
            self.rect.x = -40
            self.rect.y = randint(0, win_height - 60)



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen_width = 700
        self.screen_height = 600
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), self.screen_size)


        self.player = Player('player.png', 335, 300, 25, 25, 7.5, self.screen)


        self.enemies = pygame.sprite.Group()
        self.enemies2 = pygame.sprite.Group()
        self.enemies3 = pygame.sprite.Group()

        
        self.generate_enemies()
        self.generate_enemies2()
        self.generate_enemies3()
        self.generate_enemies4()
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.finished = False
        self.pause = False

        self.hp_boss = False
        
        self.ticks = pygame.time.get_ticks()

        self.times = self.ticks

        self.win = 0

        self.hp = 1


        self.statistic_font = pygame.font.Font(None, 35)
        self.resalt_font = pygame.font.Font(None, 85)

        self.game_run()



    def generate_enemies(self):
        for i in range(3):
            enemy = Enemy("ufo1.png", randint(0, self.screen_width - 60), -40, randint(40, 80), randint(40, 60), randint(3, 7), self.screen)
            self.enemies2.add(enemy)

    def generate_enemies2(self):
        for i in range(3):
            enemy2 = Enemy2("ufo1.png", randint(0, self.screen_width - 60), 600, randint(40, 60), randint(40, 60), randint(3, 7), self.screen)
            self.enemies2.add(enemy2)

    def generate_enemies3(self):
        for i in range(3):
            enemy2 = Enemy3("ufo1.png", 700, randint(0, self.screen_height - 80), randint(40, 60), randint(40, 60), randint(3, 7), self.screen)
            self.enemies2.add(enemy2)

    def generate_enemies4(self):
        for i in range(3):
            enemy2 = Enemy4("ufo1.png", 0, randint(0, self.screen_height - 80), randint(40, 60), randint(40, 60), randint(3 , 7), self.screen)
            self.enemies2.add(enemy2)



    def game_run(self):
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)   
        while self.running:      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                    if event.key == pygame.K_x and self.pause == False:
                        self.pause = True

                    if event.key == pygame.K_z and self.pause == True:
                        self.pause = False
                        
                        
            if not self.finished:
                if self.pause == False:
                        
                    global lost
                    
                    self.screen.blit(self.background, (0, 0))

                    self.player.update(self.screen_width) 
                    self.player.draw()  


                    self.enemies.update(self.screen_width, self.screen_height)
                    self.enemies.draw(self.screen)  

                    self.enemies2.update(self.screen_width, self.screen_height)
                    self.enemies2.draw(self.screen)
                    self.seconds = (pygame.time.get_ticks() - self.ticks) // 1000

                    if pygame.sprite.spritecollide(self.player, self.enemies, True):
                        self.hp -= 1
                        enemy2 = Enemy("ufo1.png", randint(0, self.screen_width - 80), -40, 80, 80, randint(1, 5), self.screen)
                        self.enemies2.add(enemy2)

                    if pygame.sprite.spritecollide(self.player, self.enemies2, True):
                        self.hp -= 1
                        enemy = Enemy("ufo1.png", randint(0, self.screen_width - 80), -40, 80, 50, randint(1, 5), self.screen)
                        self.enemies.add(enemy)

                    if self.hp <= 0:
                        self.finished = True
                        lusetext = self.resalt_font.render("GAME OVER", True, (255, 255, 255))
                        self.screen.blit(lusetext, (170, 250))

                    if self.pause == True:
                        lusetext = self.resalt_font.render("Pause", True, (255, 255, 255))
                        self.screen.blit(lusetext, (225, 250))






                    text_score = self.statistic_font.render("время: " + str(self.seconds), 1, (255, 255, 255))
                    self.screen.blit(text_score, (10, 20))


                 
            else:
                self.finished = False
                lost = 0
                self.hp = 1
                self.player = Player('player.png', 335, 300, 25, 25, 7.5, self.screen)
                
                for enemy in self.enemies:
                    enemy.kill()

                for enemy2 in self.enemies2:
                    enemy2.kill()





            
                self.generate_enemies()
                self.generate_enemies2()
                self.generate_enemies3()
                self.generate_enemies4()
                pygame.time.delay(1000)
                self.ticks = pygame.time.get_ticks()
                

                
            self.clock.tick(self.fps)
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game()







