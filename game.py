import json
import math

import pygame

from investment import *
from button import Button

class Game:
    INVESTMENTS_FP = "investments.json"

    def __init__(self):
        # Initialize Screen
        pygame.init()
        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
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

        # Inialize Values
        self.currency = 0

        # Create Investments
        self.investments = {}
        with open(Game.INVESTMENTS_FP, "r") as f:
            data = json.load(f)
            for investment in data['investments']:
                self.investments[investment['type']] = Investment(self, investment)

        # Try to Load Player Data from File
        try:
            f = open("player_data.json", "r")
            player_data = json.load(f)
            self.currency = player_data['currency']
            for investment in self.investments.values():
                if investment.type == 'lemonade_stand' and player_data['investments'][investment.type] == 0:
                    investment.upgrade()
                    continue
                for i in range(player_data['investments'][investment.type]):
                    investment.upgrade()
            f.close()
        except:
            for investment in self.investments.values():
                if investment.type == 'lemonade_stand':
                    investment.upgrade()

        # Event Loop
        while True:
            self.clock.tick(60)

            self.background.fill((10, 10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    new_screen_size = event.dict['size']
                    ASPECT_RATIO = 16. / 9.
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
                    investment_data = {}
                    for investment in self.investments.values():
                        investment_data[investment.type] = investment.quantity
                    player_data = {
                        "currency": self.currency,
                        "investments": investment_data
                    }
                    with open("player_data.json", "w") as f:
                        json.dump(player_data, f)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    investment = self.investments["lemonade_stand"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    investment = self.investments["newspaper_delivery"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    investment = self.investments["car_wash"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    investment = self.investments["pizza_delivery"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    investment = self.investments["donut_shop"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    investment = self.investments["shrimp_boat"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    investment = self.investments["hockey_team"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    investment = self.investments["movie_studio"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    investment = self.investments["bank"]
                    investment.purchase()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    investment = self.investments["oil_company"]
                    investment.purchase()
                
            self.draw_currency()
            index = 0
            for investment in self.investments.values():
                investment.update(self)
                investment.render(((index % 2) * int(200 * self.background.get_width() / 800), (int(index / 2)) * int(85 * self.background.get_height() / 450)))
                index += 1
            # Blit Everything to Screen
            center_background_w = self.screen.get_width() // 2 - self.background.get_width() // 2
            center_background_h = self.screen.get_height() // 2 - self.background.get_height() // 2
            self.screen.blit(self.background, (center_background_w, center_background_h))
            pygame.display.flip()

    def draw_currency(self):
        # Display Text
        currency, suffix = truncate_value(self.currency)
        text = self.font.render('$' + format(currency, '6.2f') + ' ' + suffix, 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.midtop = self.background.get_rect().midtop
        self.background.blit(text, textpos)
