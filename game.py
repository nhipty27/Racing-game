import pygame
from pygame.locals import *
import os, sys
from sprites import Racer, Item, Car
import random, math

cooldown = 300

pygame.init()
pygame.font.init()
pygame.mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
MINIGAME_COLOR = (28, 170, 156)

button_sound = pygame.mixer.Sound(os.path.join('assets','SFX','switch2.wav'))
finish_sound = pygame.mixer.Sound(os.path.join('assets','SFX','finish_sound.wav'))
win_sound = pygame.mixer.Sound(os.path.join('assets','SFX','win_sound.mp3'))
lose_sound = pygame.mixer.Sound(os.path.join('assets','SFX','lose_sound.wav'))


maps = []
map1 = pygame.image.load(os.path.join("assets","map1.png"))
maps.append(map1)
map2 = pygame.image.load(os.path.join("assets","map2.png"))
maps.append(map2)
map3 = pygame.image.load(os.path.join("assets","map3.png"))
maps.append(map3)
map4 = pygame.image.load(os.path.join("assets","map4.png"))
maps.append(map4)

choosemaps = []
choosemap1 = pygame.image.load(os.path.join("assets","choosecharacter","map1.jpg"))
choosemaps.append(choosemap1)
choosemap2 = pygame.image.load(os.path.join("assets","choosecharacter","map2.png"))
choosemaps.append(choosemap2)
choosemap3 = pygame.image.load(os.path.join("assets","choosecharacter","map3.png"))
choosemaps.append(choosemap3)
choosemap4 = pygame.image.load(os.path.join("assets","choosecharacter","map4.jpg"))
choosemaps.append(choosemap4)



class Game():
	def __init__(self):
		self.width = 1200
		self.height = 700
		self.FPS = 20
		self.win = pygame.display.set_mode((self.width,self.height))
		pygame.display.set_caption('Racing Betting')
		self.display = pygame.Surface((self.width,self.height))
		self.main_font = 'Cucho Bold.otf'
		self.instruction = pygame.image.load(os.path.join('assets', 'instruction.png'))
		self.bg = pygame.transform.scale(pygame.image.load(os.path.join('assets/bg.jpg')),(self.width, self.height))
		self.map = None
		self.choosemap = None
		self.username = ''
		self.check_input_name = False
		self.money = 0
		self.wincount, self.wincountfake= 0,0
		self.losecount, self.losecountfake = 0,0

		self.bet = 0
		self.NumOfItem = 0
		self.music_list =['BGcountry.mp3','BGnight.mp3','BGcity.ogg','BGdesert.mp3']
		self.music_to_play = None
		self.menu_music = True
		self.rank_list = []
		self.key_pressed,self.click, self.back, self.enter, self.delete, self.useitem = False, False, False, False, False, False
		self.run_map_screen = False
		self.run_minigame = None
		self.now = 0
		self.selected_racer = ''
		self.play = False
		self.run = True
		self.run_music = True
		self.mouse_pos = []
		self.keys = [False,False,False,False,False,False]
		self.main_menu = MainMenu(self)
		self.settings = SettingsMenu(self)
		self.shop = ShopMenu(self)
		self.help = HelpMenu(self)
		self.curr_menu = self.main_menu
		self.clock = pygame.time.Clock()
		self.race_pos = [666,608,550,492,434,377]
		self.run_sound = True
		self.run_choose = False
		self.run_present = False
		self.playsound = True
		self.vt = 0
		self.my_list = []
		self.read_data()
		self.racers = pygame.sprite.Group()
		self.read_data()
		self.NumOfItemfake = self.NumOfItem
		self.fakemoney = self.money
	def check_events(self):
		for event in pygame.event.get():
			self.mouse_pos = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				self.play = False
				self.run_map_screen = False
				self.run = False
				self.curr_menu.run_display = False
				self.run_minigame = False
				self.run_ranking = False
				self.run_choose = False
				self.run_present = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.click = True
			if event.type == pygame.KEYDOWN:
				self.key_pressed = True
				if event.key == pygame.K_ESCAPE:
					self.back = True
				if event.key == K_f:
					self.useitem = True
				if event.key == K_1:
					self.keys[0] = True
				elif event.key == K_2:
					self.keys[1] = True
				elif event.key == K_3:
					self.keys[2] = True
				elif event.key == K_4:
					self.keys[3] = True
				elif event.key == K_5:
					self.keys[4] = True
				elif event.key == K_6:
					self.keys[5] = True

	def read_data(self):
		with open('vd.txt', 'r') as f:
			data = f.read()
			my = data.splitlines()
			f.seek(0, 0)
		f.close()
		self.username = my[0]

		with open('user.txt', 'r') as ff:
			data1 = ff.read()
		self.my_list = data1.splitlines()
		ff.close()
		i = 0
		a = []
		while i < len(self.my_list):
			if self.username == self.my_list[i]:
				self.vt = i + 2
				a = self.my_list[self.vt].split()
				a[0] = int(a[0])  # thắng
				a[1] = int(a[1])  # thua
				a[2] = int(a[2])  # điểm
				a[3] = int(a[3])  # bùa
				self.wincount = a[0]
				self.losecount = a[1]
				self.money = a[2]
				self.NumOfItem = a[3]
			i += 3

	def update_data(self):
		j = 1
		self.my_list[self.vt] = str(self.wincount) + ' ' + str(self.losecount) + ' ' + str(self.money) + ' ' + str(self.NumOfItem)
		with open('user.txt', 'w') as f:
			f.write(self.my_list[0])
			while j < len(self.my_list):
				f.write("\n" + self.my_list[j])
				j += 1
			f.close()

	def draw_text (self, text, size, x, y, color):
		self.font = pygame.font.Font(self.main_font, size)
		text_surface = self.font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.center = (x, y)
		self.display.blit(text_surface, text_rect)

	def create_racer_lists(self):
		random.shuffle(self.race_pos)
		self.map1 = pygame.sprite.Group()
		self.map2 = pygame.sprite.Group()
		self.map3 = pygame.sprite.Group()
		self.map4 = pygame.sprite.Group()


		self.chimy = Car(self,'Chimy',0,self.race_pos[0])
		self.tata = Car(self, 'Tata', 0, self.race_pos[1])
		self.tan = Car(self, 'Tan', 0, self.race_pos[2])
		self.yeonie = Car(self, 'Yeonie', 0, self.race_pos[3])
		self.shoky = Car(self, 'Shoky', 0, self.race_pos[4])
		self.koya = Car(self, 'Koya', 0, self.race_pos[5])
		self.map1.add(self.chimy,self.tata,self.tan,self.yeonie,self.shoky,self.koya)

		self.cutegirl = Racer(self, 'cutegirl', 0, self.race_pos[0])
		self.flatboy = Racer(self, 'flatboy', 0, self.race_pos[1])
		self.cowboy = Racer(self, 'cowboy', 0, self.race_pos[2])
		self.cowboygirl = Racer(self, 'cowboygirl', 0, self.race_pos[3])
		self.ninjaboy = Racer(self, 'ninjaboy', 0, self.race_pos[4])
		self.ninjagirl = Racer(self, 'ninjagirl', 0, self.race_pos[5])
		self.map4.add(self.cutegirl, self.flatboy, self.cowboy, self.cowboygirl, self.ninjaboy, self.ninjagirl)

		self.linh = Car(self,'linh',0, self.race_pos[0])
		self.nghia = Car(self,'nghia',0, self.race_pos[1])
		self.nam = Car(self,'nam',0, self.race_pos[2])
		self.long = Car(self,'long',0, self.race_pos[3])
		self.nhi = Car(self,'nhi',0, self.race_pos[4])
		self.kiet = Car(self,'kiet',0, self.race_pos[5])
		self.map3.add(self.linh,self.nghia,self.nam,self.long,self.nhi,self.kiet)

		self.dino = Racer(self, 'dino', 0, self.race_pos[0])
		self.santa = Racer(self, 'santa', 0, self.race_pos[1])
		self.pumpkin = Racer(self, 'pumpkin', 0, self.race_pos[2])
		self.knight = Racer(self, 'knight', 0, self.race_pos[3])
		self.zombieboy = Racer(self, 'zombieboy', 0, self.race_pos[4])
		self.zombiegirl = Racer(self, 'zombiegirl', 0, self.race_pos[5])
		self.map2.add(self.dino, self.santa, self.pumpkin, self.knight, self.zombieboy, self.zombiegirl)

	def new(self):
		self.all_sprites = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		for pos in self.race_pos:
			for i in range(2):
				self.item = Item(self, random.choice([200,250, 300,350, 400,450, 500,550, 600,650, 700,750, 800,850, 900,950]), pos)
				self.all_sprites.add(self.item)
				self.items.add(self.item)
		self.all_sprites.add(self.racers)



	def update(self):
		self.all_sprites.update()
		if self.useitem and self.NumOfItem>0:
			self.reset_keys()
			self.NumOfItem-=1
			self.NumOfItemfake = self.NumOfItem
			i = 0
			for racer in self.racers:
				if racer.name == self.selected_racer:
					self.item = Item(self,racer.rect.right + 30,self.race_pos[i])
					self.items.add(self.item)
				i+=1
		for racer in self.racers:
			hits = pygame.sprite.spritecollide(racer, self.items, True)
			for item in hits:
				if item.type == 'speedup':
					racer.speeduptime = 40
					racer.speedup = True
				elif item.type == 'slowdown':
					racer.slowdowntime = 40
					racer.slowdown = True
				elif item.type == 'teleport':
					racer.teleport()
				elif item.type == 'stop':
					racer.stoptime = 40
				elif item.type == 'turnback':
					racer.turnbacktime = 30
					racer.turnback = True
				elif item.type == 'backtostart':
					racer.back_to_start()

	def draw(self):
		self.win.blit(self.display, (0, 0))
		self.display.blit(self.map, (0, 0))
		self.racers.draw(self.display)
		self.draw_text('Money: ' + str(self.money), 30, 1100, 50, BLACK)
		self.draw_text('Items: ' + str(self.NumOfItem),30,1100,90,BLACK)
		self.draw_text('You choose: ' + self.selected_racer, 40, self.width/2, 50, BLACK)
		for racer in self.racers:
			for item in self.items:
				if item.y == racer.y and item.rect.left - racer.rect.right <= 40:
					item.draw(self.display)

		for racer in self.racers:
			if racer.rect.right >= self.width and racer.name not in self.rank_list:
				self.rank_list.append(racer.name)

		if len(self.rank_list) == 6:
			for racer in self.racers:
				if racer.name == self.rank_list[0]:
					racer.winning = True
				else:
					racer.idle = True
			if self.selected_racer == self.rank_list[0]:
				self.fakemoney = self.money + self.bet
				image = pygame.image.load(os.path.join('assets','win.png'))
				self.wincountfake = self.wincount + 1
				if self.run_sound:
					if self.playsound:
						win_sound.play()
						self.playsound = False
			else:
				self.money = self.fakemoney - self.bet
				image = pygame.image.load(os.path.join('assets', 'lose.png'))
				self.losecountfake = self.losecount+1
				if self.run_sound:
					if self.playsound:
						lose_sound.play()
						self.playsound = False
			for i in range(6):
				if self.selected_racer == self.rank_list[i]:
					self.draw_text('Your rank: ' + str(i+1),50,self.width/2,650,WHITE)

			rect = image.get_rect()
			rect.center = (self.width/2,self.height/2)
			self.display.blit(image,rect)
			if self.key_pressed:
				self.run_ranking = True
				self.ranking_screen()
				self.play = False
		pygame.display.update()


	def reset_keys(self):
		self.click, self.key_pressed = False, False
		self.back, self.enter, self.delete, self.useitem = False, False, False, False
		self.keys[0],self.keys[1],self.keys[2],self.keys[3],self.keys[4],self.keys[5] = False, False, False, False, False, False
	'''
	
	Game loop
	
	'''
	def game_loop(self):
		self.load_music()
		while self.play:
			self.clock.tick(self.FPS)
			self.check_events()
			self.update()
			self.draw()

	def load_music(self):
		if self.menu_music:
			self.music_to_play = 'menu.wav'
		pygame.mixer.music.load(os.path.join('assets', self.music_to_play))
		if self.run_music:
			pygame.mixer.music.play(-1)
	'''
	Ranking screen
	'''
	def ranking_screen(self):
		ranking_images = []
		ranking_rects = []
		for racer in self.rank_list:
			ranking_image = pygame.image.load(os.path.join('assets', 'CharacterRankings', racer + '.png'))
			ranking_images.append(ranking_image)
			rect = ranking_image.get_rect()
			ranking_rects.append(rect)
		ranking_rects[0].center = (1005,230)
		ranking_rects[1].center = (1005,310)
		ranking_rects[2].center = (1005,390)
		ranking_rects[3].center = (1005,470)
		ranking_rects[4].center = (1005,550)
		ranking_rects[5].center = (1005,630)

		next_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets','next_inactive.png')),(70,70))
		next_active = pygame.transform.scale(pygame.image.load(os.path.join('assets','next_active.png')),(70,70))
		next_rect = next_active.get_rect()
		x, y = 1100, 620
		next_rect.center = (x, y)
		state = next_inactive
		while self.run_ranking:
			self.win.blit(self.display, (0, 0))
			self.reset_keys()
			self.check_events()
			image = pygame.image.load(os.path.join('assets','ranking.png'))
			self.display.blit(image, (0,0))
			for i in range (6):
				self.display.blit(ranking_images[i],ranking_rects[i])
			self.draw_text(self.rank_list[0], 50, self.width/2,230,BLACK)
			self.draw_text(self.rank_list[1], 50, self.width/2,310,BLACK)
			self.draw_text(self.rank_list[2], 50, self.width/2,390,BLACK)
			self.draw_text(self.rank_list[3], 50, self.width/2,470,BLACK)
			self.draw_text(self.rank_list[4], 50, self.width/2,550,BLACK)
			self.draw_text(self.rank_list[5], 50, self.width/2,630,BLACK)
			self.draw_text('Money: ' + str(self.money), 40, 1080, 50, BLACK)
			state = next_inactive
			distance = math.hypot(x - self.mouse_pos[0], y - self.mouse_pos[1])
			if distance < 35:
				state = next_active
				if self.click:
					if self.selected_racer == self.rank_list[0]:
						self.run_present = True
						self.run_ranking = False
						self.bet = 0
						self.rank_list = []
						self.selected_racer = ''
						self.racers.empty()
						self.items.empty()
						self.playsound = True
						self.present_screen()
					else:
						self.curr_menu.run_display = True
						self.run_ranking = False
						self.bet = 0
						self.rank_list = []
						self.selected_racer = ''
						self.racers.empty()
						self.items.empty()
						self.playsound = True
						self.fakemoney = self.money
						self.wincount = self.wincountfake
						self.losecount = self.losecountfake
						self.NumOfItem = self.NumOfItemfake
						self.music_to_play = 'menu.wav'
						self.update_data()
			self.display.blit(state, next_rect)
			pygame.display.update()

	"Present screen"
	def present_screen(self):
		present_image = pygame.image.load(os.path.join('assets', 'present_box.png'))
		present_rect = present_image.get_rect()
		present_rect.center = (self.width/2,self.height/2)
		no_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'no_inactive.png')), (70, 70))
		no_active = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'no_active.png')), (70, 70))
		yes_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'yes_inactive.png')), (70, 70))
		yes_active = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'yes_active.png')), (70, 70))
		next_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'next_inactive.png')), (70, 70))
		next_active = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'next_active.png')), (70, 70))
		next_rect = next_active.get_rect()
		x2, y2 = 1100, 620
		next_rect.center = (x2, y2)
		x1, y1 = self.width/2 - 100, self.height/2 + 250
		x3, y3 = self.width/2 + 100, self.height/2 + 250
		no_rect = no_active.get_rect()
		no_rect.center = (x1, y1)
		yes_rect = yes_active.get_rect()
		yes_rect.center = (x3, y3)
		state = no_inactive
		state1 = yes_inactive
		state2 = next_inactive
		present = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 5, 10])
		check = False
		check1 = False
		while self.run_present:
			self.win.blit(self.display, (0, 0))
			self.reset_keys()
			self.check_events()
			image = pygame.image.load(os.path.join('assets', 'ChooseGift.png'))
			self.display.blit(image, (0, 0))
			state = no_inactive
			state1 = yes_inactive
			state2 = next_inactive
			distance = math.hypot(x1 - self.mouse_pos[0], y1 - self.mouse_pos[1])
			distance1 = math.hypot(x3 - self.mouse_pos[0], y3 - self.mouse_pos[1])
			distance2 = math.hypot(x2 - self.mouse_pos[0], y2 - self.mouse_pos[1])
			if distance < 35:
				state = no_active
				if self.click:
					self.money = self.fakemoney
					check = True
			if distance1 < 35:
				state1 = yes_active
				if self.click:
					self.fakemoney = self.money
					self.NumOfItemfake = self.NumOfItem + present
					check = True
					check1 = True
			if distance2 < 35:
				state2 = next_active
				if self.click:
					self.run_present = False
					self.curr_menu.run_display = True
					self.fakemoney = self.money
					self.wincount = self.wincountfake
					self.losecount = self.losecountfake
					self.NumOfItem = self.NumOfItemfake
					self.music_to_play = 'menu.wav'
					self.update_data()
			if check1:
				self.draw_text('You get ' + str(present) + ' mysterious item(s)!', 40, self.width / 2, 670, BLACK)
			self.draw_text('Congratulations! Do you want to open the gift?',50,self.width/2,40,BLACK)
			self.draw_text('If you open the gift, you will not receive money!',30,self.width/2,80,BLACK)
			self.display.blit(present_image,present_rect)
			self.display.blit(state, no_rect)
			self.display.blit(state1, yes_rect)
			if check:
				self.display.blit(state2, next_rect)
			pygame.display.update()



	"""
	select map screen
	"""

	def select_map(self, x, y, number, action = None):
		MAP = {
			'1': map1,
			'2': map2,
			'3': map3,
			'4': map4,
		}
		MAP[number] = pygame.transform.scale(MAP[number],(480,280))
		map_rect = MAP[number].get_rect()
		map_rect.topleft = (x,y)
		self.display.blit(MAP[number],map_rect)
		if map_rect.collidepoint(self.mouse_pos):
			if self.click:
				if action!=0:
					self.create_racer_lists()
					if action == '1':
						self.map = maps[0]
						self.choosemap = choosemaps[0]
						self.racers.add(self.map1)
						self.menu_music = False
						self.music_to_play = self.music_list[0]
					elif action == '2':
						self.map = maps[1]
						self.choosemap = choosemaps[1]
						self.racers.add(self.map2)
						self.menu_music = False
						self.music_to_play = self.music_list[1]
					elif action == '3':
						self.map = maps[2]
						self.choosemap = choosemaps[2]
						self.racers.add(self.map3)
						self.menu_music = False
						self.music_to_play = self.music_list[2]
					elif action == '4':
						self.map = maps[3]
						self.choosemap = choosemaps[3]
						self.racers.add(self.map4)
						self.menu_music = False
						self.music_to_play = self.music_list[3]
					self.run_map_screen = False
					self.run_choose = True
					self.new()
					self.choose_character()
	def map_screen(self):

		while self.run_map_screen:
			self.win.blit(self.display, (0, 0))
			self.reset_keys()
			self.check_events()
			self.select_map(100, 100, '1','1')
			self.select_map(self.width - 580, 100, '2','2')
			self.select_map(100, 400, '3','3')
			self.select_map(self.width - 580, 400, '4','4')
			self.draw_text('Please choose map!', 60, self.width/2, 50, BLACK)
			self.draw_text('Money: ' + str(self.money), 40, 1080, 50, BLACK)
			self.win.blit(self.display,(0,0))
			self.display.blit(self.bg, (0, 0))
			pygame.display.update()


	'''
	select character screen
	'''

	def betting(self):
		self.reset_keys()
		self.check_events()
		if self.keys[0]:
			self.bet = 10
		if self.keys[1]:
			self.bet = 50
		if self.keys[2]:
			self.bet = 100
		if self.keys[3]:
			self.bet = 200
		if self.keys[4]:
			self.bet = 500
		if self.keys[5]:
			self.bet = 1000


	def choose_character(self):
		choose_images = []
		choose_rects = []
		choose_rect = None
		names = []
		next_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'next_inactive.png')), (70, 70))
		next_active = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'next_active.png')), (70, 70))
		next_rect = next_active.get_rect()
		x, y = 1100, 620
		next_rect.center = (x, y)
		state = next_inactive
		self.selected = False
		for racer in self.racers:
			choose_image = pygame.image.load(os.path.join('assets', 'choosecharacter', racer.name + '.png'))
			choose_images.append(choose_image)
			rect = choose_image.get_rect()
			choose_rects.append(rect)
			names.append(racer.name)

		choose_rects[0].center = (268, 178)
		choose_rects[1].center = (598, 178)
		choose_rects[2].center = (953, 178)
		choose_rects[3].center = (268, 523)
		choose_rects[4].center = (598, 523)
		choose_rects[5].center = (953, 523)
		while self.run_choose:
			self.reset_keys()
			self.check_events()
			self.win.blit(self.display, (0, 0))
			self.display.blit(self.choosemap, (0, 0))
			for i in range (6):
				self.display.blit(choose_images[i],choose_rects[i])
			self.draw_text(names[0], 50, 268, 178 + 150, BLACK)
			self.draw_text(names[1], 50, 598, 178 + 150, BLACK)
			self.draw_text(names[2], 50, 953, 178 + 150, BLACK)
			self.draw_text(names[3], 50, 268, 523 + 150, BLACK)
			self.draw_text(names[4], 50, 598, 523 + 150, BLACK)
			self.draw_text(names[5], 50, 953, 523 + 150, BLACK)
			if not self.selected:
				if choose_rects[0].collidepoint(self.mouse_pos):
					if self.click:
						self.selected = True
						self.selected_racer = names[0]
				if choose_rects[1].collidepoint(self.mouse_pos):
					if self.click:
						self.selected = True
						self.selected_racer = names[1]
				if choose_rects[2].collidepoint(self.mouse_pos):
					if self.click:
						self.selected = True
						self.selected_racer = names[2]
				if choose_rects[3].collidepoint(self.mouse_pos):
					if self.click:
						self.selected = True
						self.selected_racer = names[3]
				if choose_rects[4].collidepoint(self.mouse_pos):
					if self.click:
						self.selected = True
						self.selected_racer = names[4]
				if choose_rects[5].collidepoint(self.mouse_pos):
					if self.click:
						self.selected = True
						self.selected_racer = names[5]

			if self.selected:
				bet_image = pygame.image.load(os.path.join('assets','BetRate.png'))
				rect = bet_image.get_rect()
				rect.center = (self.width/2,self.height/2)
				self.display.blit(bet_image,rect)
				state = next_inactive
				distance = math.hypot(x - self.mouse_pos[0], y - self.mouse_pos[1])
				self.draw_text('Use keyboard to choose bet rate!', 50, self.width/2, 50, BLACK)
				self.betting()
				if self.bet > self.money:
					self.draw_text('Don\'t have enough money, please choose again!', 50, self.width / 2, 600, BLACK)
				if self.bet <= self.money:
					self.draw_text('You bet ' + str(self.bet) + '$!', 50, self.width / 2, 600, BLACK)
					if distance < 35:
						state = next_active
						if self.click and self.bet!=0:
							choose_rects = []
							self.run_choose = False
							self.play = True

				self.display.blit(state, next_rect)
			pygame.display.update()


	'''
	Minigame
	'''

	def minigame(self):
		tab = pygame.image.load(os.path.join("assets/morp_tab.png")).convert()
		tab.set_colorkey((0, 0, 0))
		tab_pos = (300, 50)

		cross = pygame.image.load(os.path.join("assets/cross.png")).convert()
		cross.set_colorkey((0, 0, 0))
		cross_list = []

		circle = pygame.image.load(os.path.join("assets/circle.png")).convert()
		circle.set_colorkey((0, 0, 0))
		circle_list = []
		inspect_line = []
		cont = 0
		selected = 0
		cpu_level = 0
		win = 0
		player = 0
		cpu = 0
		lose = 0
		draw = 0
		draw2 = 0
		r = 0
		time = 0
		turn = "player"
		tab_case = [(300, 50), (500, 50), (700, 50),
					(300, 250), (500, 250), (700, 250),
					(300, 450), (500, 450), (700, 450)]

		t = tab_case
		win_line = [[t[0], t[1], t[2]], [t[3], t[4], t[5]], [t[6], t[7], t[8]],
					[t[0], t[3], t[6]], [t[1], t[4], t[7]], [t[2], t[5], t[8]],
					[t[0], t[4], t[8]], [t[6], t[4], t[2]]]

		pygame.key.set_repeat(200, 60)
		while self.run_minigame:
			pygame.time.Clock().tick(3)
			self.win.blit(self.display,(0, 0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:  # wait for events
					pygame.quit()
					sys.exit()
				if event.type == MOUSEBUTTONDOWN:
					if lose or draw:
						cross_list = [];
						circle_list = [];
						win = 0;
						lose = 0;
						draw = 0;
						self.display.fill(MINIGAME_COLOR);
						turn = "player"
						self.display.blit(tab, tab_pos);
						pygame.display.flip()
					if event.button == 1:
						if turn == "player":
							for case in tab_case:
								if event.pos[0] > case[0] and event.pos[0] < case[0] + 200 \
										and event.pos[1] > case[1] and event.pos[1] < case[1] + 200:
									if not case in cross_list and not case in circle_list:
										selected = 1
										cross_list.append(case)
										self.display.blit(cross, case)

							for line in win_line:
								cont = 0
								for case in line:
									for cross1 in cross_list:
										if cross1 == case: cont += 1
								if cont == 3 and not lose:
									win = 1
							if win:
								player += 1
							if selected:
								cont = 0
								selected = 0
								turn = "cpu"
			if turn == "cpu" and not win:
				time += 1
				if time == 3:
					time = 0

					if not selected and cpu_level == 0:

						for case in tab_case:
							if not selected:
								cont = 0
								r = random.randint(0, 8)
								for cross1 in cross_list:
									if tab_case[r] == cross1: cont += 1
								for circle1 in circle_list:
									if tab_case == case: cont += 1
								if not cont:
									if not tab_case[r] in circle_list and not tab_case[r] in cross_list:
										selected = 1
										circle_list.append(tab_case[r])
										self.display.blit(circle, tab_case[r])

					if not selected and cpu_level >= 0:

						for case in tab_case:
							if not selected:
								cont = 0
								for cross1 in cross_list:
									if cross1 == case: cont += 1
								for circle1 in circle_list:
									if circle1 == case: cont += 1
								if not cont:
									if not case in circle_list and not case in cross_list:
										selected = 1
										circle_list.append(case)
										self.display.blit(circle, case)

					for circle1 in circle_list:
						for line in win_line:
							cont = 0
							for case in line:
								if circle1 == case:
									inspect_line = line
									for case_inspect in inspect_line:
										for circle2 in circle_list:
											if case_inspect == circle2:
												cont += 1
							if cont == 3:
								lose = 1
					if lose:
						cpu = 0
					cont = 0
					cont2 = 0
					selected = 0
					turn = "player"

			if not win and not lose and not draw:
				for case in tab_case:
					for cross1 in cross_list:
						if cross1 == case: cont += 1
					for circle1 in circle_list:
						if circle1 == case: cont += 1
					if cont == 9:
						draw = 1
						draw2 += 1
				cont = 0

			self.display.fill(MINIGAME_COLOR)
			self.draw_text('Money: ' + str(self.money), 40, 1080, 50, WHITE)
			self.draw_text('You don\'t have', 40, 150, 200,WHITE)
			self.draw_text('enough money!', 40, 150, 250, WHITE)
			self.draw_text('Please play this', 40, 150, 300, WHITE)
			self.draw_text('to receive money', 40, 150, 350, WHITE)
			# result
			if win:
				while not self.key_pressed:
					self.win.blit(self.display, (0, 0))
					self.display.blit(self.bg, (0, 0))
					self.draw_text('You win! Here\'s 50$', 60, self.width / 2, self.height / 2, BLACK)
					self.draw_text('Press any key to continue!', 60, self.width / 2, 650, BLACK)
					self.check_events()
					pygame.display.update()
				self.run_minigame = False
				self.money += 50
				self.fakemoney = self.money
				self.run_map_screen = True
				self.map_screen()

			if lose:
				self.draw_text('You lose! Please try again', 50, self.width / 2, 650,WHITE)

			if draw:
				self.draw_text('You draw! Please try again',50,self.width/2,650,WHITE)

			self.display.blit(tab, tab_pos)
			for cross_pos in cross_list:
				self.display.blit(cross, cross_pos)
			for circle_pos in circle_list:
				self.display.blit(circle, circle_pos)

			pygame.display.flip()

			#self.minigame = False
		self.reset_keys()
		#self.map_screen()


#Menu
class Menu():
	def __init__(self,game):
		self.game = game
		self.run_display = True

		self.title = pygame.image.load(os.path.join('assets/title.png'))
		self.menubg = pygame.transform.scale(pygame.image.load(os.path.join('assets/bg.jpg')),(self.game.width,self.game.height))
	def blit_screen(self):
		self.game.win.blit(self.game.display,(0, 0))
		self.game.display.blit(self.menubg, (0, 0))

		pygame.display.update()

class MainMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
	def menu_button(self, x, y, text, size, action = None):
		inactive_button_img = pygame.image.load(os.path.join('assets/inactive_button.png'))
		active_button_img = pygame.image.load(os.path.join('assets/active_button.png'))
		rect = inactive_button_img.get_rect()
		rect.center = (x, y)
		self.game.display.blit(inactive_button_img,rect)
		if rect.collidepoint(self.game.mouse_pos):
			self.game.display.blit(active_button_img, rect)
			self.check_mouse(action)

		self.game.draw_text(text,size, x, y-5, WHITE)

	def draw(self):
		self.game.draw_text('Welcome ' + str(self.game.username),30,self.game.width/2,30,BLACK)
		self.game.draw_text('Money: ' + str(self.game.money), 30,1100,30,BLACK)
		self.game.draw_text('Wins: ' + str(self.game.wincount), 30, 1100, 60, BLACK)
		self.game.draw_text('Loses: ' + str(self.game.losecount), 30, 1100, 90, BLACK)
		self.game.draw_text('Items: ' + str(self.game.NumOfItem), 30, 1100, 120, BLACK)
		self.menu_button(self.game.width / 5, self.game.height / 2 - 160, "Play", 28, "Play")
		self.menu_button(self.game.width / 5, self.game.height / 2 - 80, "Settings", 30, "Settings")
		self.menu_button(self.game.width / 5, self.game.height / 2 , "Help", 30, "Help")
		self.menu_button(self.game.width / 5, self.game.height / 2 + 80, "Shop", 30, "Shop")
		self.menu_button(self.game.width / 5, self.game.height / 2 + 160, "Quit", 30, "Quit")
	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.reset_keys()
			self.game.check_events()
			self.check_mouse()
			self.draw()
			self.game.display.blit(self.title,(500, 270))
			self.blit_screen()

	def check_mouse(self,action = None):
		if self.game.click:
			if action != 0:
				if self.game.run_sound:
					button_sound.play()
				if action == "Play":
					if self.game.money == 0:
						self.game.run_minigame = True
						self.game.minigame()
					else:
						self.game.run_map_screen = True
						self.game.map_screen()
					self.run_display = False
				if action == "Settings":
					self.game.curr_menu = self.game.settings
					self.run_display = False
				if action == "Shop":
					self.game.curr_menu = self.game.shop
					self.run_display = False
				if action == "Help":
					self.game.curr_menu = self.game.help
					self.run_display = False
				if action == "Quit":
					pygame.quit()
					sys.exit()
class SettingsMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.reset_keys()
			self.game.check_events()
			if self.game.back:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
			self.music_option()
			self.blit_screen()
	def music_option(self):
		music_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets/music_inactive.png')),(230,230))
		music_active = pygame.transform.scale(pygame.image.load(os.path.join('assets/music_active.png')),(230,230))
		music_mute = pygame.transform.scale(pygame.image.load(os.path.join('assets/music_selected.png')),(230,230))
		sound_inactive = pygame.transform.scale(pygame.image.load(os.path.join('assets/sound_inactive.png')),(230,230))
		sound_active = pygame.transform.scale(pygame.image.load(os.path.join('assets/sound_active.png')),(230,230))
		sound_mute = pygame.transform.scale(pygame.image.load(os.path.join('assets/sound_selected.png')),(230,230))
		x1, y1 = 400, 335
		x3, y3 = 800, 335
		music_rect = music_active.get_rect()
		music_rect.center = (x1,y1)
		sound_rect = music_active.get_rect()
		sound_rect.center = (x3,y3)
		radius1, color1 = 115, music_inactive
		color3 = sound_inactive
		x2, y2 = pygame.mouse.get_pos()
		distance = math.hypot(x1 - x2, y1 - y2)
		distance1 = math.hypot(x3 - x2, y3 - y2)
		if self.game.run_music:
			color1 = music_inactive
		if not self.game.run_music:
			color1 = music_mute
		if distance < radius1:
			if self.game.run_music:
				color1 = music_active
			if self.game.click:
				self.game.run_music = not self.game.run_music
		self.game.display.blit(color1, music_rect)
		if self.game.run_sound:
			color3 = sound_inactive
		if not self.game.run_sound:
			color3 = sound_mute
		if distance1 < radius1:
			if self.game.run_sound:
				color3 = sound_active
			if self.game.click:
				self.game.run_sound = not self.game.run_sound
		self.game.display.blit(color3, sound_rect)

class ShopMenu(Menu):
	def __init__(self,game):
		Menu.__init__(self,game)
	def display_menu(self):
		self.run_display = True
		shop_image = pygame.image.load(os.path.join('assets','shop','shop.png'))
		rect1 = pygame.Rect(322,304,172,135)
		rect2 = pygame.Rect(510,304,172,135)
		rect3 = pygame.Rect(322,453,172,135)
		rect4 = pygame.Rect(510,453,172,135)
		check1,check2,check3,check4 = False,False,False,False
		while self.run_display:
			self.game.win.blit(self.game.display,(0,0))
			self.game.reset_keys()
			self.game.check_events()
			self.game.display.blit(shop_image, (0, 0))
			self.game.draw_text('Money: ' + str(self.game.money), 30,1100,30,BLACK)
			if rect1.collidepoint(self.game.mouse_pos):
				if self.game.click and self.game.money>=10:
					check1 = True
					check2, check3, check4 = False, False, False
					self.game.NumOfItem = self.game.NumOfItemfake + 1
					self.game.money = self.game.fakemoney-10
					self.game.fakemoney = self.game.money
					self.game.NumOfItemfake = self.game.NumOfItem
					self.game.update_data()
			if rect2.collidepoint(self.game.mouse_pos):
				if self.game.click and self.game.money>=20:
					check2 = True
					check1, check3, check4 = False, False, False
					self.game.NumOfItem = self.game.NumOfItemfake + 2
					self.game.money = self.game.fakemoney - 20
					self.game.fakemoney = self.game.money
					self.game.NumOfItemfake = self.game.NumOfItem
					self.game.update_data()
			if rect3.collidepoint(self.game.mouse_pos):
				if self.game.click and self.game.money>=50:
					check3 = True
					check2, check1, check4 = False, False, False
					self.game.NumOfItem = self.game.NumOfItemfake + 5
					self.game.money = self.game.fakemoney - 50
					self.game.fakemoney = self.game.money
					self.game.NumOfItemfake = self.game.NumOfItem
					self.game.update_data()
			if rect4.collidepoint(self.game.mouse_pos):
				if self.game.click and self.game.money>=100:
					check4 = True
					check2, check3, check1 = False, False, False
					self.game.NumOfItem = self.game.NumOfItemfake + 10
					self.game.money = self.game.fakemoney - 100
					self.game.fakemoney = self.game.money
					self.game.NumOfItemfake = self.game.NumOfItem
					self.game.update_data()
			if check1:
				pygame.draw.rect(self.game.display, BLACK, rect1, 5)
			if check2:
				pygame.draw.rect(self.game.display, BLACK, rect2, 5)
			if check3:
				pygame.draw.rect(self.game.display, BLACK, rect3, 5)
			if check4:
				pygame.draw.rect(self.game.display, BLACK, rect4, 5)

			if self.game.back:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False

			pygame.display.update()
class HelpMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self,game)
	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.reset_keys()
			self.game.check_events()
			self.game.display.blit(self.game.instruction,(0,0))
			if self.game.back:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False
			self.blit_screen()

def run_game():
	g = Game()
	g.read_data()
	while g.run:
		g.load_music()
		g.curr_menu.display_menu()
		g.game_loop()
	pygame.quit()
	sys.exit()