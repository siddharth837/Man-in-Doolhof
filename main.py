import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Man in Doolhof.')

#define game variables
tile_size = 40
gameOver=0


#load images
#sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('PygameImages/skyImage.png')


class Player():
	def __init__(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'PygameImages/rightRunning{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0

	def update(self):
		dx = 0
		dy = 0
		walk_cooldown = 5
		global gameOver
		if gameOver == 0:
		#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False:
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


		#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


		#add gravity
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y

		#check for collision
		for tile in world.tile_list:
			#check for collision in x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			#check for collision in y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground i.e. jumping
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				#check if above the ground i.e. falling
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
		#Check for collision with enemies
		if pygame.sprite.spritecollide(self, blob_group , False ):
			gameOver=-1
			print("gamever")
		if pygame.sprite.spritecollide(self, lava_group , False):
			gameOver=-1
			print("gameover")
		if pygame.sprite.spritecollide(self, diamondGroup , True):
			gameOver=1
		



		#update player coordinates
		self.rect.x += dx
		self.rect.y += dy

		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0

		#draw player onto screen
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)




class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('PygameImages/dirtImage.png')
		grass_img = pygame.image.load('PygameImages/grass.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
            
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 26)
					blob_group.add(blob)
				if tile == 4:
					lava=Lava(col_count * tile_size, row_count * tile_size + 26)
					lava_group.add(lava)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)



class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PygameImages/enemy1.png')
		self.image = pygame.transform.scale(self.image,(50,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		if gameOver == 0:
			self.rect.x += self.move_direction
			self.move_counter += 1
			if abs(self.move_counter) > 50:
				self.move_direction *= -1
				self.move_counter *= -1


class Gameover(pygame.sprite.Sprite):
	def __init__(self,x,y):

		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("PygameImages/gameOver.png")
		self.image=pygame.transform.scale(self.image,(500,100))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def renew(self):
		if gameOver == -1:
			screen.blit(self.image,self.rect)	


class Diamond(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("PygameImages/crown.png")
		self.image=pygame.transform.scale(self.image,(40,40))
		self.rect=self.image.get_rect()
		
		self.rect.x=x
		self.rect.y=y
		
	def create(self):
		screen.blit(self.image,self.rect)	
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PygameImages/lava.png')
		self.image = pygame.transform.scale(self.image,(40,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1





world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130)
over= Gameover(160,300)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
diamondGroup=pygame.sprite.Group()
world = World(world_data)

diamond=Diamond(695,80)
diamondGroup.add(diamond)
def restart():
	global gameOver
	if gameOver==1:	 
		pygame.font.init()
		#sur_obj=pygame.display.set_mode((300,200))
		#pygame.display.set_caption("Font Explanation")
		Black=(0,0,0)
		font_obj = pygame.font.SysFont('Comic Sans MS', 40)
		text_obj=font_obj.render("Press R to restart the game.",False,Black) 
		screen.blit(text_obj,(160,500))
def win():
	if gameOver==1:
		pygame.font.init()
		Black=(0,0,0)
		font_obj=pygame.font.SysFont('Comic Sans MS', 40)
		text_obj=font_obj.render("Congrats!! You won the game.", False, Black)
		screen.blit(text_obj,(190,300))
def changeOver():
	global gameOver
	if gameOver==1:
		key=pygame.key.get_pressed()
		if key[pygame.K_r]:
			gameOver=0
			
run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))
	#screen.blit(sun_img, (100, 100))
	global text_obj
	restart()
	win()
	world.draw()

	blob_group.update()
	blob_group.draw(screen)
	lava_group.draw(screen)
	over.renew()

	player.update()
	diamond.create()
	changeOver()

	diamondGroup.update()
	diamondGroup.draw(screen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()