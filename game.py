import json
import math
from enum import Enum
import pygame

from utility import truncate_value
from investment import Investment
from player import Player
from button import Button

class ContentState(Enum):
    UNLOCKS     = 1
    UPGRADES    = 2
    MANAGERS    = 3
    INVESTORS   = 4
    INVESTMENTS = 5

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

class Game:
    # File Paths
    INVESTMENTS_FP = "investments.json"
    UPGRADES_FP = "upgrades.json"
    MANAGERS_FP = "managers.json"
    # Constants
    AUTO_SAVE_INTERVAL_MS = 1000

    GAME_FPS = 60

    ASPECT_RATIO = 16 / 9
    INIT_SCREEN_W = 800
    INIT_SCREEN_H = 450
    INIT_NAVBAR_W = 200
    INIT_NAVBAR_H = INIT_SCREEN_H
    INIT_NAVBAR_X = 0
    INIT_NAVBAR_Y = 0
    INIT_BUTTON_W = INIT_NAVBAR_W
    INIT_BUTTON_H = 40
    INIT_CONTENT_W = 600
    INIT_CONTENT_H = INIT_SCREEN_H
    INIT_CONTENT_X = INIT_NAVBAR_W
    INIT_CONTENT_Y = 0

    FONT_NAME    = "VT323-Regular.ttf"
    FONT_SIZE_H1 = 48
    FONT_SIZE_H2 = 40
    FONT_SIZE_H3 = 32
    FONT_SIZE_H4 = 24
    FONT_SIZE_H5 = 16
    FONT_SIZE_H6 = 8

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption('Bits and Bytes')
        game_icon = pygame.image.load('floppy_pixel.png')
        game_icon = pygame.transform.smoothscale(game_icon, (32, 32))
        pygame.display.set_icon(game_icon)

        # Initialize Clock
        self.clock = pygame.time.Clock()

        # Custom User Events
        self.AUTO_SAVE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.AUTO_SAVE, Game.AUTO_SAVE_INTERVAL_MS)

        # Create Player Object
        self.player = Player(self)
        self.player.load(Game.INVESTMENTS_FP, Game.UPGRADES_FP, Game.MANAGERS_FP)

        # Set Default Font Sizes
        self.font_h1 = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H1)
        self.font_h2 = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H2)
        self.font_h3 = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H3)
        self.font_h4 = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H4)
        self.font_h5 = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H5)
        self.font_h6 = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H6)

        # Create Surfaces
        self.screen = pygame.display.set_mode((Game.INIT_SCREEN_W, Game.INIT_SCREEN_H), pygame.RESIZABLE)
        # Background -> Screen
        self.background = pygame.Surface(self.screen.get_size())
        self.background_rect = self.background.get_rect()
        self.background = self.background.convert()
        # NavBar -> Background
        self.nav_bar = pygame.Surface((Game.INIT_NAVBAR_W, Game.INIT_NAVBAR_H))
        self.nav_bar_rect = self.nav_bar.get_rect()
        self.nav_bar = self.nav_bar.convert()
        # Content -> Background
        self.content = pygame.Surface((Game.INIT_CONTENT_W, Game.INIT_CONTENT_H))
        self.content_rect = self.content.get_rect()
        self.content_rect.topleft = self.nav_bar_rect.topright
        self.content = self.content.convert()

        # Create Buttons
        unlock_button = Button(self, 'UNLOCKS', ContentState.UNLOCKS, self.set_state)
        upgrade_button = Button(self, 'UPGRADES', ContentState.UPGRADES, self.set_state)
        manager_button = Button(self, 'MANAGERS', ContentState.MANAGERS, self.set_state)
        investor_button = Button(self, 'INVESTORS', ContentState.INVESTORS, self.set_state)
        investment_button = Button(self, 'INVESTMENTS', ContentState.INVESTMENTS, self.set_state)
        self.nav_bar_buttons = [
            unlock_button,
            upgrade_button,
            manager_button,
            investor_button,
            investment_button
        ]

        # Initial State
        self.set_state(ContentState.INVESTMENTS)

    def run(self):
        # Exit Condition
        running = True
        while running:
            # Advance Clock
            self.clock.tick(Game.GAME_FPS)

            # Clear Surfaces
            self.screen.fill((Color.BLACK))
            self.background.fill(Color.WHITE)
            self.nav_bar.fill((0, 128, 0))
            self.content.fill((0, 0, 128))

            # Reset Mouse Buttons
            self.mouse_buttons_pressed = (False, False, False, False, False)
            # Event Loop
            for event in pygame.event.get():
                # Close Event
                if event.type == pygame.QUIT:
                    running = False
                    break
                # Resize Event
                if event.type == pygame.VIDEORESIZE:
                    # Resize Screen
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                # Auto Save Event
                if event.type == self.AUTO_SAVE:
                    self.player.save()
                # Check Mouse Button Press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_buttons_pressed = (event.button == 1, event.button == 2, event.button == 3, event.button == 4, event.button == 5)

            # Update Investments
            for investment in self.player.investments.values():
                investment.update()

            # Blit NavBar on Background
            # Draw Elements on NavBar
            render_navbar(self)
            self.background.blit(self.nav_bar, self.nav_bar_rect)
            # Blit Content on Background
            # Draw Elements on Content
            render_content(self)
            self.background.blit(self.content, self.content_rect)

            # Get New Screen Size
            screen_w = self.screen.get_rect().width
            screen_h = self.screen.get_rect().height
            # Calculate New Background Size
            if screen_w > screen_h * Game.ASPECT_RATIO:
                new_bg_h = screen_h
                new_bg_w = int(screen_h * Game.ASPECT_RATIO)
            else:
                new_bg_w = screen_w
                new_bg_h = int(screen_w / Game.ASPECT_RATIO)
            # Resize Background
            self.background_rect.center = (screen_w // 2, screen_h // 2)
            self.background_rect.width = new_bg_w
            self.background_rect.height = new_bg_h

            self.screen.blit(pygame.transform.scale(self.background, (new_bg_w, new_bg_h)), self.background_rect)

            # Flip Display
            pygame.display.flip()

        # Close Application
        pygame.quit()
        quit()

    def set_state(self, state):
        self.content_state = state

    def prestige(self):
        pass

def render_navbar(game):
    currency, suffix = truncate_value(game.player.currency)
    # Current
    current_text = game.font_h4.render('Current', 1, (255, 255, 255))
    current_text_rect = current_text.get_rect()
    current_text_rect.midtop = game.nav_bar_rect.midtop
    game.nav_bar.blit(current_text, current_text_rect)
    # Currency
    currency_font = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H1)
    currency_text = currency_font.render('$' + format(currency, '6.2f'), 1, (255, 255, 255))
    currency_text_rect = currency_text.get_rect()
    currency_text_rect.midtop = current_text_rect.midbottom
    game.nav_bar.blit(currency_text, currency_text_rect)
    # Suffix
    suffix_font = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H4)
    suffix_text = suffix_font.render(suffix, 1, (255, 255, 255))
    suffix_text_rect = suffix_text.get_rect()
    suffix_text_rect.midtop = currency_text_rect.midbottom
    game.nav_bar.blit(suffix_text, suffix_text_rect)
    # Draw Buttons
    button_font = pygame.font.Font(Game.FONT_NAME, Game.FONT_SIZE_H2)
    button_spacing = 10
    button_w = Game.INIT_BUTTON_W
    button_h = Game.INIT_BUTTON_H
    for i in range(len(game.nav_bar_buttons)):
        midtop = (suffix_text_rect.midbottom[0], suffix_text_rect.midbottom[1] + int(button_h) * i + button_spacing * (i))
        button = game.nav_bar_buttons[i]
        if button.render((button_w, button_h), midtop):
            button.function(button.state)
    # Draw Lifetime Earnings
    lifetime, suffix = truncate_value(game.player.lifetime_earnings)
    suffix_text = game.font_h4.render(suffix, 1, (255, 255, 255))
    suffix_text_rect = suffix_text.get_rect()
    suffix_text_rect.midbottom = game.nav_bar.get_rect().midbottom
    game.nav_bar.blit(suffix_text, suffix_text_rect)
    lifetime_earnings_text = game.font_h1.render('$' + format(lifetime, '6.2f'), 1, (255, 255, 255))
    lifetime_earnings_text_rect = lifetime_earnings_text.get_rect()
    lifetime_earnings_text_rect.midbottom = suffix_text_rect.midtop
    game.nav_bar.blit(lifetime_earnings_text, lifetime_earnings_text_rect)
    lifetime_text = game.font_h4.render('Lifetime', 1, (255, 255, 255))
    lifetime_text_rect = lifetime_text.get_rect()
    lifetime_text_rect.midbottom = lifetime_earnings_text_rect.midtop
    game.nav_bar.blit(lifetime_text, lifetime_text_rect)


def render_content(game):
    if game.content_state == ContentState.INVESTMENTS:
        index = 0
        for investment in game.player.investments.values():
            spacing_w = Investment.INIT_SPACING
            spacing_h = Investment.INIT_SPACING
            investment_x = int(spacing_w + spacing_w * math.floor(index / 5) + math.floor(index / 5) * Investment.INIT_INVESTMENT_W)
            investment_y = int(spacing_h + spacing_h * (index % 5) + (index % 5) * Investment.INIT_INVESTMENT_H)
            investment.render(game.content, (investment_x, investment_y))
            index += 1
    elif game.content_state == ContentState.UNLOCKS:
        index = 0
        for investment in game.player.investments.values():
            for unlock in investment.unlocks:
                if investment.quantity < unlock.get('goal'):
                    spacing_w = int(Investment.INIT_SPACING)
                    spacing_h = int(Investment.INIT_SPACING)
                    unlock_x = int(spacing_w + spacing_w * math.floor(index / 5) + math.floor(index / 5) * Investment.INIT_INVESTMENT_W)
                    unlock_y = int(spacing_h + spacing_h * (index % 5) + (index % 5) * Investment.INIT_INVESTMENT_H)
                    unlock_w = int(Investment.INIT_INVESTMENT_W)
                    unlock_h = int(Investment.INIT_INVESTMENT_H)
                    # Unlock Surface
                    unlock_surface = pygame.Surface((unlock_w, unlock_h))
                    unlock_surface_rect = unlock_surface.get_rect()
                    unlock_surface.convert()
                    # Investment Name
                    investment_name_font = pygame.font.Font(game.FONT_NAME, game.FONT_SIZE_H4)
                    investment_name_text = investment_name_font.render(investment.name, 1, (255, 255, 255))
                    investment_name_rect = investment_name_text.get_rect()
                    investment_name_rect.topleft = unlock_surface_rect.topleft
                    unlock_surface.blit(investment_name_text, investment_name_rect)
                    # Next Upgrade Quantity
                    upgrade_quantity_font = pygame.font.Font(game.FONT_NAME, game.FONT_SIZE_H4)
                    upgrade_quantity_text = upgrade_quantity_font.render('Next: ' + str(unlock.get('goal')), 1, (255, 255, 255))
                    upgrade_quantity_rect = upgrade_quantity_text.get_rect()
                    upgrade_quantity_rect.topright = unlock_surface_rect.topright
                    unlock_surface.blit(upgrade_quantity_text, upgrade_quantity_rect)
                    # Affected Investment
                    affected_investment_font = pygame.font.Font(game.FONT_NAME, game.FONT_SIZE_H4)
                    affected_investment_text = affected_investment_font.render('Affect: ' + str(unlock.get('target_investment')), 1, (255, 255, 255))
                    affected_investment_rect = upgrade_quantity_text.get_rect()
                    affected_investment_rect.midleft = unlock_surface_rect.midleft
                    unlock_surface.blit(affected_investment_text, affected_investment_rect)
                    # Next Upgrade Effect
                    effect_font = pygame.font.Font(game.FONT_NAME, game.FONT_SIZE_H4)
                    effect_text = effect_font.render('Effect: ' + str(unlock.get('speed_effect')) + 'x Sp / ' + str(unlock.get('profit_effect')) + 'x Pr', 1, (255, 255, 255))
                    effect_rect = effect_text.get_rect()
                    effect_rect.bottomleft = unlock_surface_rect.bottomleft
                    unlock_surface.blit(effect_text, effect_rect)
                    unlock_surface_rect.topleft = (unlock_x, unlock_y)
                    game.content.blit(unlock_surface, unlock_surface_rect)
                    break
            index += 1
    elif game.content_state == ContentState.UPGRADES:
        index = 0
        for upgrade in game.player.upgrades.values():
            if upgrade.render(index):
                index += 1
    elif game.content_state == ContentState.MANAGERS:
        index = 0
        for manager in game.player.managers.values():
            if manager.render(index):
                index += 1
    elif game.content_state == ContentState.INVESTORS:
        pass