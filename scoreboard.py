import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """reports scoring information"""

    def __init__(self, ai_game):
        """initializes scorekeeping attribute"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #preps the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_ammo()


    def prep_score(self):
        """renders the score in an image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score " "{:,}".format(rounded_score)    
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)

        # displays the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """turn the high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score " "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.settings.bg_color)

        #centers the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        #turns the level in the rendered image
        level_str = "Level " + str(self.stats.level)
        
        self.level_image = self.font.render(level_str, True, 
            self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """draws scores, level and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.normal_ammo_image, self.normal_ammo_rect)
        self.ships.draw(self.screen)

    def prep_ships(self):
        """shows how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_ammo(self):
        #renders normal ammo count
        normal_ammo_str = "Ammo" " " + str(self.stats.ammo_count)

        self.normal_ammo_image = self.font.render(normal_ammo_str, True, 
            self.text_color, self.settings.bg_color)

        self.normal_ammo_rect = self.normal_ammo_image.get_rect()
        self.normal_ammo_rect.bottomright = self.screen_rect.bottomright