import json
import math

import pygame

from investment import *
from player import Player
from button import Button

class Game:
    INVESTMENTS_FP = "investments.json"

    INIT_W = 800
    INIT_H = 450

    def __init__(self):
        # Initialize Screen
        pygame.init()
        self.screen = pygame.display.set_mode((Game.INIT_W, Game.INIT_H), pygame.RESIZABLE)
        pygame.display.set_caption('Basic Idle Game')
        self.font = pygame.font.Font("VT323-Regular.ttf", 16)

        # Initialize Clock
        self.clock = pygame.time.Clock()

        # Custom Events
        self.AUTO_SAVE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.AUTO_SAVE, 1000)

        # Fill Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        # Create Player Object to Track Saveable Data
        self.player = Player(self)

        # Instantiate Investments from Json
        with open(Game.INVESTMENTS_FP, "r") as f:
            data = json.load(f)
            for investment_dict in data.get('investments'):
                self.player.investments[investment_dict.get('type')] = Investment(self, investment_dict)

        # Load Player Save
        self.player.load()

        # Event Loop
        while True:
            self.clock.tick(60)

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
            index = 0
            for investment in self.player.investments.values():
                investment.update(self)
                investment.render((int(190 * self.background.get_width() / 800) + (index % 2) * int(305 * self.background.get_width() / 800), int(25 * self.background.get_height() / 450) + (int(index / 2)) * int(85 * self.background.get_height() / 450)))
                index += 1
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
        textpos.midtop = self.background.get_rect().midtop
        self.background.blit(text, textpos)
