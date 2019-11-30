import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Here I define the bullets"""

	def __init__(self,ai_game):
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#create a bullet then instantly set it in the right position above the ship
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		#store the bullet position as float
		self.y = float(self.rect.y)

	def update(self):
		"""shooting 'animation'"""
		#updates the decimal position
		self.y -= self.settings.bullet_speed
		#update the rect position
		self.rect.y = self.y

	def draw_bullet(self):
		"""let's the bullet appear on the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)
