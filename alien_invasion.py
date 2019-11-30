import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Overall class to maanage game assets and behaviour"""

	def __init__(self):
		"""initialize the game, and create game resourecs"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		#instance to store game statistics
		self.stats = GameStats(self)

		self.bg_color = (self.settings.bg_color)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		#makes the play button
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""start main loop"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()
 
	def _check_events(self):
		#Watch for keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self,mouse_pos):
		"""starts a new game when the player clicks play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#reset the game statistics
			self.stats.reset_stats()
			self.stats.game_active = True

			#get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#hides mouse cursor when playing
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
            	#responds to key pressing
			if event.key == pygame.K_RIGHT:
				self.ship.moving_right = True
			elif event.key == pygame.K_LEFT:
				self.ship.moving_left = True
			elif event.key == pygame.K_q:
				sys.exit()
			elif event.key == pygame.K_SPACE:
				self._fire_bullet()
			elif event.key == pygame.K_P:
				

	def _check_keyup_events(self, event):
				#responds to key releasing
			if event.key == pygame.K_RIGHT:
				self.ship.moving_right = False
			elif event.key == pygame.K_LEFT:
				self.ship.moving_left = False

	def _fire_bullet(self):
		"""Creat a bullet and add it to the bullet group"""
		"""if statement limits amount of bullets allowed to three based on bullet settings"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		self.bullets.update()

		#removes offscreen bullets
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		#checks for any bullets that have hit aliens
		# If there is a collision, remove the bullet and alien
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if not self.aliens:
			#Destroys bullets that are presents and creates a new fleet
			self.bullets.empty()
			self._create_fleet()

	def _update_aliens(self):
		"""updates the position of all aliens in the fleet"""
		"""checks if the fleet is at an edge then updates the position for all aliens"""
		self._check_fleet_edges()
		self.aliens.update()
		#look for ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		#look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""respond to the ship being hit by an alien"""
		if self.stats.ships_left > 0:
		#decrease one life
			self.stats.ships_left -= 1
		#get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()
		#create a new fleet and centers the ship
			self._create_fleet()
			self.ship.center_ship()
		#pause the game
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)



	def _create_fleet(self):
		"""creats the fleet of aliens"""
		#make an alien and find t he number of aliens in a row
		#spacing between each alien is one alien width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

	
		#Determines the amount of aliens that can fit on rows on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)
		
		#create the full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)


	def _create_alien(self, alien_number, row_number):
		#creat an alien and place it in the row
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien_width = alien.rect.width
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""respond approriately if any aliens have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		#make the most recently draw screen visible
			self.screen.fill(self.settings.bg_color)
			self.ship.blitme()
			for bullet in self.bullets.sprites():
				bullet.draw_bullet()
			self.aliens.draw(self.screen)

			#draw the play button if the game is inactive
			if not self.stats.game_active:
				self.play_button.draw_button()

			pygame.display.flip()

	def _check_aliens_bottom(self):
		"""check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#If an alien reaches the bottom I make the game behave as if the ship got hit
				self._ship_hit()
				break


if __name__ == '__main__':
	#make a game instance and run
	ai = AlienInvasion()
	ai.run_game()


