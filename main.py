import pygame as pg
import game
import os, sys

pg.init()
screen = pg.display.set_mode((1200, 765))
pg.display.set_caption('LOGIN')

COLOR_INACTIVE = pg.Color('PeachPuff1')
COLOR_ACTIVE = pg.Color('black')
FONT = pg.font.Font(None, 45)


class InputBox:

    def __init__(self, x, y, w, h, text='', text1=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.rect1 = pg.Rect(x, y, w, h)
        self.text = text
        self.text1= text1
        self.txt_surface = FONT.render(text, True, self.color)
        self.txt_surface1 = FONT.render(text, True, self.color)
        self.active = False
        self.iconn = pg.image.load(os.path.join('assets','bg1.png'))
        self.login = pg.image.load(os.path.join('assets','Login.2.png'))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)
        with open('vd.txt', 'w') as f:
            f.write(self.text)
        f.close()

    def handle_event2(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect1.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text1)

                elif event.key == pg.K_BACKSPACE:
                    self.text1 = self.text1[:-1]
                else:
                    self.text1 += event.unicode
                self.txt_surface1 = FONT.render('*'*len(self.text1), True, self.color)
        with open('vd.txt', 'a') as f:
            f.write("\n" + self.text1)
        f.close()
    def update(self):
        width = max(348, self.txt_surface.get_width()+10)
        self.rect.w = width
        width1 = max(348, self.txt_surface1.get_width() + 10)
        self.rect1.w = width1


    def draw(self, screen):
        screen.blit(self.iconn, (0, 0))
        screen.blit(self.login,(330,250))
        pg.draw.rect(screen, self.color, self.rect, 2)
        pg.draw.rect(screen, self.color, self.rect1, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        screen.blit(self.txt_surface1, (self.rect1.x+5, self.rect1.y+5))
    def draw1(self, screen):


        pg.draw.rect(screen, self.color, self.rect1, 2)

        screen.blit(self.txt_surface1, (self.rect1.x+5, self.rect1.y+5))






class Button:
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x, y,w,h)
        self.color = COLOR_INACTIVE
        self.text ="   "
        self.text1 ="  "
        self.active = False
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.txt_surface1 = FONT.render(self.text1, True, self.color)
        self.username= ''
        self.password =''
        self.text2=''
    def update(self, event):
        with open('vd.txt', 'r') as f:
            data = f.read()
            my = data.splitlines()
            f.seek(0,0)
            self.username =f.readline()
            self.password= f.readline()
        f.close()
        self.username = my[0]

        with open('user.txt', 'r') as ff:
            data = ff.read()
        my_list = data.splitlines()
        ff.close()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                i=0
                d=0
                self.text2=''
                while i < len(my_list):
                    if self.username == my_list[i] and self.password == my_list[i+1]:
                        game.run_game()

                        self.text2=''
                        break
                    elif self.username == '' or self.password == '':
                        self.text2='Moi nhap username va password'
                        break
                    else:
                        d=d+3
                    i=i + 3
                if d == len(my_list):
                    self.text2 = 'Ban nhap sai username hoac password'
                    print(self.text2)


            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def draw(self,screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(FONT.render(self.text2,True,self.color ), (380, 580))


    def update1(self, event):
        with open('vd.txt', 'r') as f:
            data = f.read()
            my = data.splitlines()
            f.seek(0, 0)
            self.username = f.readline()
            self.password = f.readline()
        f.close()
        self.username = my[0]
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active

                with open('user.txt','r') as ff:
                    data = ff.read()
                    my_list = data.splitlines()
                ff.close()
                j=0
                d=0
                self.text2=''
                while j < len(my_list):
                    if self.username== my_list[j] :
                        d=d+1
                        break
                    elif self.username == '' or self.password == '':
                        d=-1
                        break

                    j=j+3

                if d== 0:
                    with open('user.txt', 'a+') as f:
                        f.write( "\n" + self.username)
                        f.write("\n" + self.password)
                        f.write("\n" +"0 0 0 0")
                    f.close()
                    game.run_game()

                elif d==1:
                    print("Username already exists")
                    self.text2='Username already exists'
                elif d==-1:
                    self.text2 = 'Please enter username and password!'


            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def draw1(self,screen):
        screen.blit(self.txt_surface1, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(FONT.render(self.text2,True,self.color ), (380, 580))



def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(506, 303, 140, 47)
    input_box2 = InputBox(506, 383, 140, 48)
    b = Button(372,460,130,47)
    b2 = Button(522,460,178,47)

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            input_box1.handle_event(event)
            input_box2.handle_event2(event)
            b.update(event)
            b2.update1(event)
        input_box1.update()
        input_box2.update()
     #   screen.fill((30, 30, 30))

        input_box1.draw(screen)
        input_box2.draw1(screen)
        b.draw(screen)
        b2.draw1(screen)

        pg.display.flip()
        clock.tick(30)



main()
pg.quit()
sys.exit()