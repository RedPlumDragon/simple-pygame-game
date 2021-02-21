# imports modules
import pygame
from pygame.locals import *
import random
import time
import getpass
import turtle
import os
import stat
import sys

# variables defined here becase of errors
# time that the game ran
start_time = None
# screen width and height
screen_width,screen_height = None,None
# the score
score = None
# the window
wn = None
# the score (current)
current_score = None
# the highscore
highscore_text = None
# the replay text
replay = None
# the player x and y
x,y = 0,0

# game fuction
def Game():

	# measures the time that the game runs
	global start_time
	start_time = time.time()

	# gets the user currently logged in
	user = getpass.getuser()

	# creates player
	class Player(pygame.sprite.Sprite):
		def __init__(self):
			super(Player, self).__init__()
			self.surf = pygame.image.load("/Users/" + user + "/" +  "Downloads/UFOh! Files/Spaceship.png").convert()
			self.surf.set_colorkey((0, 0, 0), RLEACCEL)
			self.rect = self.surf.get_rect()

	# creates enemies
	class Enemy(pygame.sprite.Sprite):
		def __init__(self):
			super(Enemy, self).__init__()
			self.surf = pygame.image.load("/Users/" + user + "/" +  "Downloads/UFOh! Files/UFO.png").convert()
			self.surf.set_colorkey((0,0,0), RLEACCEL)
			self.rect = self.surf.get_rect(
				center = (	random.randint(screen_width + 20, screen_width + 100),
					random.randint(0, screen_height)
					)
				)
			self.speed = random.randint(5, 20)

		def update(self):
			self.rect.move_ip(-self.speed, 0)
			if self.rect.right < 0:
				self.kill()

	# play background music
	pygame.mixer.init()
	pygame.mixer.music.load("/Users/" + user + "/" +  "Downloads/UFOh! Files/AnalogVideoGame.mp3")
	pygame.mixer.music.play(loops=-1)

	# sound effect
	crash = pygame.mixer.Sound("/Users/" + user + "/" +  "Downloads/UFOh! Files/8-bitExplosion.ogg")

	# initialize pygame
	pygame.init()

	# screen width and height
	global screen_width
	screen_width = 800
	global screen_height
	screen_height = 600

	# create screen
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("UFOh!")

	# creates function to move player
	def update(pressed_keys):
		if pressed_keys[K_UP] or pressed_keys[K_w]:
			global y
			y -= 7

		if  pressed_keys[K_DOWN] or pressed_keys[K_s]:
			y += 7

		if pressed_keys[K_LEFT] or pressed_keys[K_a]:
			global x
			x -= 7

		if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
			x += 7
		# keeps the player on the screen
		if y < 0:
			y = 0

		if y > screen_height - 35:
			y = screen_height - 35

		if x < 0:
			x = 0

		if x > screen_width - 95:
			x = screen_width - 95

	# create an enemy 4 times per second
	ADDENEMY = pygame.USEREVENT + 1
	pygame.time.set_timer(ADDENEMY, 250)

	# the player
	player = Player()

	# The background image
	bg = pygame.image.load("/Users/" + user + "/" +  "Downloads/UFOh! Files/SpaceBackground.png")

	# sprite groups
	enemies = pygame.sprite.Group()
	all_sprites = pygame.sprite.Group()
	all_sprites.add(player)

	# variable to see if the program is running
	running = True

	# create a clock
	clock = pygame.time.Clock()

	# main loop
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

			# add a new enemy when it is supposed to
			elif event.type == ADDENEMY:
				new_enemy = Enemy()
				enemies.add(new_enemy)
				all_sprites.add(new_enemy)

		# fill the screen with black
		screen.fill((0,0,0))

		# make a background image
		screen.blit(bg, (0,0))

		# get all the keys pressed
		pressed_keys  = pygame.key.get_pressed()

		# update the player sprite
		update(pressed_keys)

		# changes the x & y of the player
		player.rect.x,player.rect.y = x,y

		# update the enemy sprite
		enemies.update()

		# draw the sprites
		for entity in all_sprites:
			screen.blit(entity.surf, entity.rect)

		# checks for collisions with the player and the enemy
		if pygame.sprite.spritecollideany(player, enemies):
			player.kill()
			crash.play()
			pygame.time.wait(500)
			running = False

		# update the display
		pygame.display.flip()

		# slow enemies down
		clock.tick(30)

	# saves score
	st = os.stat("/Users/" + user + "/Downloads/scores.txt")
	os.chflags("/Users/" + user + "/Downloads/scores.txt", st.st_flags ^ stat.UF_HIDDEN)
	time_ran = "%s" % (time.time() - start_time)
	global score
	score = round(float(time_ran))
	highscore = open("/Users/" + user + "/Downloads/scores.txt", "a")
	highscore.write(str(score))
	highscore.write("""

""")
	highscore.close()

	# closes the pygame window
	pygame.display.quit()

	# starts up pygame again
	pygame.init()
	pygame.font.init()

	# makes a font
	font = pygame.font.SysFont("Comic Sans MS", 30)

	# makes some text
	global current_score
	current_score = font.render("Score: " + str(score),False, (255,255,255))
	highscore = open("/Users/" + user + "/Downloads/scores.txt", "r")
	highscore_read = highscore.readlines()
	highscore.close()
	highscore_read2 = []
	for i in highscore_read:
		try:
			highscore_read2.append(int(i.strip("\n")))
		except:
			highscore_read2.append(i.strip("\n"))

		try:
			highscore_read2.remove("")
		except:
			print()

	global highscore_text
	highscore_text = font.render("Highscore: " + str(int(max(highscore_read2))), False, (255,255,255))
	global replay
	replay = font.render("Press P To Play Again", False, (255,255,255))

	# creates a window
	global wn
	wn = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("UFOh!")

Game()

# variable that detects the user
user = getpass.getuser()

# creates a variable to see if program is running
endrun = True

# main loop at the end
while endrun:

	# checks if the user closed the window
	for event in pygame.event.get():
		if event.type == QUIT:
			endrun = False

	# fill the window with black
	wn.fill((0,0,0))

	#  write the score and highscore
	wn.blit(current_score, (335, 200))
	wn.blit(highscore_text, (311, 300))
	wn.blit(replay, (265, 450))

	# replay if the player wants to
	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_p]:
		Game()

	# flip the display
	pygame.display.flip()
