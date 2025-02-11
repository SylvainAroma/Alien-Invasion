import pygame
from settings import Settings
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self, ai_game):
		"""initialize the ship and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()


	#$load ship img and its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		#start ship at bottom
		self.rect.midbottom = self.screen_rect.midbottom

		#store a decimal value for the ships position
		self.x = float(self.rect.x)

		#flag to control movement
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""updates position based on movement flag"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		#update rect object from self.x
		self.rect.x = self.x

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)