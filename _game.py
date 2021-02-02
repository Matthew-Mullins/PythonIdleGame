import json
import math
import pygame

from investment import *
from player import Player
from nav_bar import NavBar
from content import Content
from button import Button

class Game:
    # File Paths
    INVESTMENTS_FP = "investments.json"
    # Constants
    INIT_W = 800
    INIT_H = 450

    def __init__(self):
        # Initialize Screen
        pygame.init()
        pygame.display.set_caption('Basic Idle Game')
        self.font = pygame.font.Font("VT323-Regular.ttf", 16)

        # Create Surfaces
        self.screen = pygame.display.set_mode((Game.INIT_W, Game.INIT_H), pygame.RESIZABLE)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        nav_bar_w = 200
        nav_bar_h = 450
        self.nav_bar = NavBar(self, (nav_bar_w, nav_bar_h))
        self.nav_bar = self.nav_bar.convert()
        self.nav_bar.fill((0, 0, 0))
        content_w = 600
        content_h = 450
        self.content = Content(self, (nav_bar_w, nav_bar_h))
        self.content = self.content.convert()
        self.content.fill((0, 0, 0))

        # Initialize Clock
        self.clock = pygame.time.Clock()

        # Custom Events
        self.AUTO_SAVE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.AUTO_SAVE, 1000)

        # Create Player Object to Track Saveable Data
        self.player = Player(self)
        self.player.load(Game.INVESTMENTS_FP)

        # Create Left Panel Surface
        l_panel_w = int(200 * self.background.get_width() / Game.INIT_W)
        l_panel_h = int(Game.INIT_H * self.background.get_height() / Game.INIT_H)
        self.left_panel = pygame.Surface((l_panel_w, l_panel_h))
        l_panel_rect = self.left_panel.get_rect()
        self.left_panel.convert()
        self.left_panel_buttons = []
        unlocks_button = Button(self, l_panel_w, int(50 * self.background.get_width() / Game.INIT_W), 'UNLOCKS', (0, 50))
        upgrades_button = Button(self, l_panel_w, int(50 * self.background.get_width() / Game.INIT_W), 'UPGRADES', (0, 100))
        managers_button = Button(self, l_panel_w, int(50 * self.background.get_width() / Game.INIT_W), 'MANAGERS', (0, 150))
        investors_button = Button(self, l_panel_w, int(50 * self.background.get_width() / Game.INIT_W), 'INVESTORS', (0, 200))
        investments_button = Button(self, l_panel_w, int(50 * self.background.get_width() / Game.INIT_W), 'INVESTMENTS', (0, 250))
        self.left_panel_buttons.append(unlocks_button)
        self.left_panel_buttons.append(upgrades_button)
        self.left_panel_buttons.append(managers_button)
        self.left_panel_buttons.append(investors_button)
        self.left_panel_buttons.append(investments_button)

        # Create Surfaces for Each Page
        page_w = 600 * self.background.get_width() // Game.INIT_W
        page_h = Game.INIT_H * self.background.get_height() // Game.INIT_H
        # Investments
        self.investments_surface = pygame.Surface((page_w, page_h))
        investment_surface_rect = self.investments_surface.get_rect()
        self.investments_surface.convert()
        # Unlocks
        # Upgrades
        # Managers
        # Investors


        # Load Initial Page
        self.curr_page = self.investments_surface

        # Run Game
        self.run()

    def run(self):
        # Event Loop
        while True:
            self.clock.tick(60)

            self.left_panel.fill((0, 0, 0))
            self.curr_page.fill((0, 0, 0))
            self.background.fill((10, 10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    # Maintain Aspect Ratio
                    ASPECT_RATIO = 16. / 9.
                    # Get New Screen Size
                    new_screen_size = event.dict['size']
                    # Calculate Background Size to Fit Screen
                    if new_screen_size[0] > ASPECT_RATIO * new_screen_size[1]:
                        new_screen_height = int(new_screen_size[1])
                        new_screen_width = int(new_screen_height * ASPECT_RATIO)
                    else :
                        new_screen_width = int(new_screen_size[0])
                        new_screen_height = int(new_screen_width / ASPECT_RATIO)
                    self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                    self.background = pygame.transform.scale(self.background, (new_screen_width, new_screen_height))
                    self.investments_surface = pygame.transform.scale(self.investments_surface, (int(600 * new_screen_width / Game.INIT_W), new_screen_height))
                    self.curr_page = self.investments_surface
                    self.left_panel = pygame.transform.scale(self.left_panel, (int(200 * new_screen_width / Game.INIT_W), new_screen_height))
                    self.font = pygame.font.Font("VT323-Regular.ttf", int(16 * new_screen_height / 450))
                if event.type == self.AUTO_SAVE:
                    self.player.save()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    investment = self.player.investments["lemonade_stand"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    investment = self.player.investments["newspaper_delivery"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    investment = self.player.investments["car_wash"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    investment = self.player.investments["pizza_delivery"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    investment = self.player.investments["donut_shop"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    investment = self.player.investments["shrimp_boat"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    investment = self.player.investments["hockey_team"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    investment = self.player.investments["movie_studio"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    investment = self.player.investments["bank"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    investment = self.player.investments["oil_company"]
                    investment.purchase()

            self.draw_currency()
            for button in self.left_panel_buttons:
                button_surface, action = button.render()
                self.left_panel.blit(button_surface, button.position)
            index = 0
            for investment in self.player.investments.values():
                investment.update(self)
                offset_x = int(10 * self.background.get_width()  / Game.INIT_W) + (int(10 * self.background.get_width()  / Game.INIT_W) * (index % 2))
                offset_y = int(10 * self.background.get_width()  / Game.INIT_W) + (int(10 * self.background.get_height() / Game.INIT_H) * math.ceil((index - 1) / 2))
                investment_x = offset_x + int(285 * self.background.get_width() / Game.INIT_W) * (index % 2)
                investment_y = offset_y + int(78  * self.background.get_height() / Game.INIT_H) * math.floor(index / 2)
                investment.render(
                    (investment_x, investment_y)
                )
                index += 1

            self.background.blit(self.left_panel, (0, 0))
            self.background.blit(self.curr_page, (int(200 * self.background.get_width() / Game.INIT_W), 0))

            # Blit Everything to Screen
            center_background_w = self.screen.get_width() // 2 - self.background.get_width() // 2
            center_background_h = self.screen.get_height() // 2 - self.background.get_height() // 2
            self.screen.blit(self.background, (center_background_w, center_background_h))
            pygame.display.flip()

        pygame.quit()
        quit()

    def draw_currency(self):
        # Display Text
        currency, suffix = truncate_value(self.player.currency)
        text = self.font.render('$' + format(currency, '6.2f') + ' ' + suffix, 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.midtop = self.left_panel.get_rect().midtop
        self.left_panel.blit(text, textpos)
