import pygame, random, time, os
class Car(pygame.sprite.Sprite):
    def __init__(self, game,name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.name = name
        self.chooseimage = pygame.image.load(os.path.join('assets','choosecharacter',self.name + '.png'))
        self.image = pygame.image.load(os.path.join('assets', 'car', self.name + '.png'))
        self.image_copy = self.image.copy()
        self.flip = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect()
        self.y = y
        self.rect.midleft = (x, y)
        self.speed = random.randrange(3, 5)
        self.current_speed = self.speed
        self.winning = False
        self.idle = False
        self.speedup, self.slowdown, self.turnback = False, False, False
        self.stoptime = 0
        self.speeduptime = 0
        self.turnbacktime = 0
        self.slowdowntime = 0
    def speed_up(self):
        self.current_speed = self.speed + 1
    def slow_down(self):
        self.current_speed = self.speed - 1
    def back_to_start(self):
        self.rect.x = 0
    def teleport(self):
        self.rect.x += 200
    def update(self):
        if self.rect.x + self.image.get_width() < self.game.width and self.stoptime <= 0:
            self.rect.x += self.current_speed

        # to speed up racer
        if self.speedup:
            if self.speeduptime > 0 and self.current_speed != self.speed + 1:
                self.current_speed = self.speed + 1
                self.speeduptime -= 1
            if self.speeduptime <= 0:
                self.current_speed = self.speed
                self.speedup = False
        # to slow down racer:
        if self.slowdown:
            if self.slowdowntime > 0 and self.current_speed != self.speed - 1:
                self.current_speed = self.speed - 1
                self.slowdowntime -= 1
            if self.slowdowntime <= 0:
                self.current_speed = self.speed
                self.slowdown = False
        # to stop racer
        if self.stoptime > 0:
            # self.current_speed = 0
            self.stoptime -= 1
        # to turn back racer:
        if self.turnback:
            if self.turnbacktime > 0 and self.current_speed >= 0:
                self.image = self.flip
                self.current_speed = -self.speed
            self.turnbacktime -= 1
            if self.turnbacktime <= 0:
                self.current_speed = self.speed
                self.image = self.image_copy
                self.turnback = False


    def draw(self, win):
        win.blit(self.image, self.rect)
class Racer(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.name = name
        self.running = True
        self.winning = False
        self.flipping = False
        self.idle = False
        self.speedup,self.slowdown,self.turnback = False, False, False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.chooseimage = pygame.image.load(os.path.join('assets', 'choosecharacter', self.name + '.png'))
        self.image = self.running_frames[0]
        self.rect = self.image.get_rect()
        self.y = y
        self.rect.midleft =(x,y)
        self.speed = random.randrange(3,5)
        self.current_speed = self.speed
        self.stoptime = 0
        self.speeduptime = 0
        self.turnbacktime = 0
        self.slowdowntime = 0
    def get_numofsprite(self):
        if self.name == 'cutegirl':
            return 20, 16, 30
        elif self.name == 'cowboy':
            return 10, 10, 10
        elif self.name == 'cowboygirl':
            return 8, 10, 7
        elif self.name == 'dino':
            return 8, 10, 12
        elif self.name == 'flatboy':
            return 15, 15, 15
        elif self.name == 'knight':
            return 10, 10, 10
        elif self.name == 'ninjaboy':
            return 10, 10, 10
        elif self.name == 'ninjagirl':
            return 10, 10, 10
        elif self.name == 'pumpkin':
            return 8, 10, 10
        elif self.name == 'santa':
            return 11, 15, 16
        elif self.name == 'zombieboy':
            return 10, 15, 8
        elif self.name == 'zombiegirl':
            return 10, 15, 8
    def load_images(self):
        self.run_sprite_num, self.idle_sprite_num,self.win_sprite_num = self.get_numofsprite()
        self.running_frames = []
        for i in range (1,self.run_sprite_num+1):
            self.running_frames.append(pygame.image.load(os.path.join('assets', self.name, 'run',str(i) + '.png')))
        self.flipping_frames = []
        for frame in self.running_frames:
            self.flipping_frames.append(pygame.transform.flip(frame,True,False))
        self.idle_frames = []
        for i in range (1,self.idle_sprite_num+1):
            self.idle_frames.append(pygame.image.load(os.path.join('assets', self.name, 'idle', str(i) + '.png')))
        self.winning_frames = []
        for i in range (1,self.win_sprite_num+1):
            self.winning_frames.append(pygame.image.load(os.path.join('assets', self.name, 'win', str(i) + '.png')))

    def back_to_start(self):
        self.rect.x = 0
    def teleport(self):
        self.rect.x += 150
    def update(self):
        self.animate()
        if self.rect.x + self.image.get_width() < self.game.width and self.stoptime <= 0:
            self.rect.x += self.current_speed
        #to speed up racer
        if self.speedup:
            if self.speeduptime>0 and self.current_speed!=self.speed+1:
                self.current_speed = self.speed + 1
                self.speeduptime-=1
            if self.speeduptime<=0:
                self.current_speed = self.speed
                self.speedup = False
        # to slow down racer:
        if self.slowdown:
            if self.slowdowntime > 0 and self.current_speed != self.speed - 1:
                self.current_speed = self.speed - 1
                self.slowdowntime -= 1
            if self.slowdowntime <= 0:
                self.current_speed = self.speed
                self.slowdown = False
        #to stop racer
        if self.stoptime>0:
            #self.current_speed = 0
            self.stoptime-=1
        #if self.stoptime<=0:
        #    self.current_speed = self.speed
        #to turn back racer:
        if self.turnback:
            if self.turnbacktime > 0:
                self.flipping = True
                self.current_speed = -self.speed
                self.turnbacktime-=1
            if self.turnbacktime<=0:
                self.flipping = False
                self.current_speed = self.speed
                self.turnback = False



    def animate(self):
        now = pygame.time.get_ticks()
        if not self.winning and not self.flipping and not self.idle:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.running_frames)
                self.image = self.running_frames[self.current_frame]
        if self.winning:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.winning_frames)
                self.image = self.winning_frames[self.current_frame]
        if self.flipping:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.flipping_frames)
                self.image = self.flipping_frames[self.current_frame]
        if self.idle:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]
    def draw(self, win):
        win.blit(self.image, self.rect)

class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.type = random.choice(['speedup','speedup','speedup','speedup','speedup','slowdown','turnback','teleport','stop','speedup','slowdown','turnback','teleport','stop','speedup','slowdown','turnback','teleport','teleport','backtostart'])
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets','item',self.type + '.png')),(50,50))
        self.rect = self.image.get_rect()
        self.rect.midleft = (self.x,self.y)
    def update(self):
        pass
    def draw(self, win):
        win.blit(self.image, self.rect)
