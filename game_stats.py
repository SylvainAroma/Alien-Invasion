class GameStats:
	"""Track statistics for alien invasion"""

	def __init__(self, ai_game):
		"""initialize statistics"""
		self.settings = ai_game.settings
		self.reset_stats()

	def reset_stats(self):
		"""initialize staistics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0

		#start the game in an inactive state
		self.game_active = False

