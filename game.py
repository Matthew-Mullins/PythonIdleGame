import json

import pygame

from investment import *

class Game:
    def __init__(self):
        # Initialize Screen
        pygame.init()
        self.screen = pygame.display.set_mode((800, 450))
        pygame.display.set_caption('Basic Idle Game')

        # Initialize Clock
        self.clock = pygame.time.Clock()

        # Custom Events
        self.INCREASE_CURRENCY_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.INCREASE_CURRENCY_EVENT, 1000)
        self.AUTO_SAVE = pygame.USEREVENT + 2
        pygame.time.set_timer(self.AUTO_SAVE, 5000)

        # Fill Background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.currency = 0

        self.investments = {
            "Lemonade Stand": LemonadeStand(self),
            "Hotdog Stand": HotdogStand(self),
            "Car Wash": CarWash(self),
            "Pizza Delivery": PizzaDelivery(self)
        }

        try:
            f = open("player_data.json", "r")
            player_data = json.load(f)
            self.currency = player_data['currency']
            for investment in self.investments.values():
                investment.load(player_data['investments'][investment.name])
            f.close()
        except:
            pass

        # Blit Everything to Screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # Event Loop
        while True:
            self.clock.tick(60)

            self.background.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == self.INCREASE_CURRENCY_EVENT:
                    income = 0
                    for investment in self.investments.values():
                        income += investment.revenue
                    self.currency += income
                if event.type == self.AUTO_SAVE:
                    investment_data = {}
                    for investment in self.investments.values():
                        investment_data[investment.name] = investment.level
                        if investment.name == "Lemonade Stand":
                            investment_data[investment.name] -= 1
                    player_data = {
                        "currency": self.currency,
                        "investments": investment_data
                    }
                    with open("player_data.json", "w") as f:
                        json.dump(player_data, f)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    stand = self.investments["Lemonade Stand"]
                    stand.upgrade()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    stand = self.investments["Hotdog Stand"]
                    stand.upgrade()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    stand = self.investments["Car Wash"]
                    stand.upgrade()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    stand = self.investments["Pizza Delivery"]
                    stand.upgrade()
                
                self.draw_currency()
                index = 0
                for inventment in self.investments.values():
                    inventment.render(((index % 2) * 300, (int((index) / 2)) * 150))
                    index += 1
                self.screen.blit(self.background, (0, 0))
                pygame.display.flip()

    def draw_currency(self):
        # Display Text
        currency, suffix = truncate_value(self.currency)
        self.font = pygame.font.Font(None, 36)
        text = self.font.render(str(round(currency, 2)) + ' ' + suffix +  ' $', 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.topright = self.background.get_rect().topright
        self.background.blit(text, textpos)