#Setting up Pygame
import pygame
import os 
import time
import random

pygame.font.init()
pygame.init() 

#Setting up display
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADER")

#Display - Enemy Ship
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))

#Display - Player Ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

#Display - Lasers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

#Display - Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bg.jpg')), (WIDTH, HEIGHT))

#Looping Music
music = pygame.mixer.music.load(os.path.join('assets','Light-Years.mp3'))
pygame.mixer.music.play(-1)

class Laser:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self, vel):
		self.y += vel

	def off_screen(self, height):
		return not(self.y <= height and self.y >= 0)

	def collision(self, obj):
		return collide(self, obj)

class Ship:
	COOLDOWN = 40

	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.player_img = None
		self.laser_img = None
		self.lasers = []
		self.cool_down_counter = 0

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

	#Prohibits spamming the Space Bar
	def cooldown(self):
		if self.cool_down_counter >= self.COOLDOWN:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(window)

	def move_lasers(self, vel, obj):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				obj.health -= 10
				self.lasers.remove(laser)

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()


class Player(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x,y,health)
		self.ship_img = YELLOW_SPACE_SHIP
		self.laser_img = YELLOW_LASER
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health

	def move_lasers(self, vel, objs):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)

	def draw(self, window):
		super().draw(window)
		self.healthbar(window)

	def healthbar(self, window):
		pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
		pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
	COLOR_MAP = {
				"red":(RED_SPACE_SHIP, RED_LASER),
				"blue":(BLUE_SPACE_SHIP, BLUE_LASER),
				"green": (GREEN_SPACE_SHIP, GREEN_LASER)
				}
	def __init__(self, x, y, color, health=100):
		super().__init__(x, y, health)
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self, vel):
		self.y += vel

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x-20, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1


def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


#The main loop
def main():
	run = True
	FPS = 80
	level = 0
	lives = 5
	main_font = pygame.font.SysFont('comicsans', 50)
	lost_font = pygame.font.SysFont('comicsans', 60)

	enemies = []
	wave_length = 5
	enemy_vel = 1

	player_vel = 5

	laser_vel = 5

	player = Player(300, 630)

	clock = pygame.time.Clock()

	lost_count = 0

	lost = False

	def redraw_window():
		WIN.blit(BG, (0,0))
		
		lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
		level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

		#This will draw "Lives" and "Level" text 
		WIN.blit(lives_label, (10,10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		for enemy in enemies:
			enemy.draw(WIN)

		player.draw(WIN)

		if lost:
			lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

		#lives_label and level_label will update continuously as 
		#redraw_window is called
		pygame.display.update()

	while run:
		clock.tick(FPS)
		redraw_window()

		#Different scenarios in which the player loses
		if lives <= 0 or player.health <= 0:
			lost = True
			lost_count += 1

		if lost:
			if lost_count>FPS * 3:
				run = False
			else:
				continue

		#If all enemies have been eliminated, the next level starts
		#and 5 more enemies start to move Down
		if len(enemies) == 0:
			level += 1
			wave_length += 5
			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(['red','blue', 'green']))
				enemies.append(enemy)

		#Lets player Quit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		#Player movement and shooting
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and player.x - player_vel > 0: 
			player.x -= player_vel
		if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  
			player.x += player_vel
		if keys[pygame.K_w] and player.y - player_vel > 0: 
			player.y -= player_vel
		if keys[pygame.K_s] and player.y + player_vel + player.get_height()+ 10 < HEIGHT:
			player.y += player_vel
		if keys[pygame.K_SPACE]:
			player.shoot()

		#Enemies move Down and shoot at random
		for enemy in enemies[:]:
			enemy.move(enemy_vel)
			enemy.move_lasers(laser_vel, player)

			if random.randrange(0, 2*80) == 1:
				enemy.shoot()

			#If a player collides with laser, 10 health is lost
			if collide(enemy, player):
				player.health -= 10
				enemies.remove(enemy)

			#If an enemy moves off the screen, a life is lost
			elif enemy.y + enemy.get_height() > HEIGHT:
				lives -= 1
				enemies.remove(enemy)



		player.move_lasers(-laser_vel, enemies)

#main_menu will execute first, and run the 
#main loop once the mouse button is clicked
def main_menu():
	title_font = pygame.font.SysFont('comicsans', 70)
	run = True
	while run:
		WIN.blit(BG, (0, 0))
		title_label = title_font.render("Click the mouse to begin...", 1, (255,255,255))
		WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()

	pygame.quit()

main_menu()
# If you are using a newer verison of Python it wont like that floating points
# were generated as the health bar is calculated. It is just a warning.
