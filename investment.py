import pygame

def truncate_value(value):
    THOUSAND        = 10 ** 3
    MILLION         = 10 ** 6
    BILLION         = 10 ** 9
    TRILLION        = 10 ** 12
    QUADRILLION     = 10 ** 15
    QUINTILLION     = 10 ** 18
    SEXTILLION      = 10 ** 21
    SEPTILLION      = 10 ** 24
    OCTILLION       = 10 ** 27
    NONILLION       = 10 ** 30
    DECILLION       = 10 ** 33

    new_val = value
    suffix = ''
    if value < MILLION:
        new_val /= float(THOUSAND)
        suffix = 'thousand'
    elif value < BILLION:
        new_val /= float(MILLION)
        suffix = 'million'
    elif value < TRILLION:
        new_val /= float(BILLION)
        suffix = 'billion'
    elif value < QUADRILLION:
        new_val /= float(TRILLION)
        suffix = 'trillion'
    else:
        new_val = 0
        suffix = 'someting'
    return (new_val, suffix)

class Investment:
    def __init__(self, game):
        self.game = game
        self.name = ''
        self.level = 0
        self.initial_revenue = 0
        self.revenue = 0
        self.revenue_scale = 1
        self.initial_cost = 0
        self.cost = 0
        self.upgrade_scale = 0

    def upgrade(self):
        if self.game.currency < self.cost:
            return
        self.game.currency -= self.cost
        self.level += 1
        if self.level % 10 == 0 and self.level != 0:
            self.revenue_scale += 1
        self.revenue = self.level * self.initial_revenue * self.revenue_scale
        self.cost *= self.upgrade_scale

    def load(self, level):
        for i in range(level):
            self.level += 1
            if self.level % 10 == 0 and self.level != 0:
                self.revenue_scale += 1
            self.revenue = self.level * self.initial_revenue * self.revenue_scale
            self.cost *= self.upgrade_scale

    def render(self, position=(0, 0)):
        # Display Text
        self.font = pygame.font.Font(None, 36)
        name_text = self.font.render(self.name, 1, (255, 255, 255))
        name_text_pos = name_text.get_rect()
        name_text_pos.topleft = self.game.background.get_rect().topleft
        name_text_pos.x += position[0]
        name_text_pos.y += position[1] + 30
        self.game.background.blit(name_text, name_text_pos)

        level_text = self.font.render('Level: ' + str(self.level), 1, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.topleft = self.game.background.get_rect().topleft
        level_text_pos.x += position[0]
        level_text_pos.y += position[1] + 60
        self.game.background.blit(level_text, level_text_pos)

        revenue, suffix = truncate_value(self.revenue)
        revenue_text = self.font.render('Revenue: ' + str(round(revenue, 2)) + ' ' + suffix, 1, (255, 255, 255))
        revenue_text_pos = level_text.get_rect()
        revenue_text_pos.topleft = self.game.background.get_rect().topleft
        revenue_text_pos.x += position[0]
        revenue_text_pos.y += position[1] + 90
        self.game.background.blit(revenue_text, revenue_text_pos)

        cost, suffix = truncate_value(self.cost)
        upgrade_text = self.font.render('Upgrade: ' + str(round(cost, 2)) + ' ' + suffix, 1, (255, 255, 255))
        upgrade_text_pos = upgrade_text.get_rect()
        upgrade_text_pos.topleft = self.game.background.get_rect().topleft
        upgrade_text_pos.x += position[0]
        upgrade_text_pos.y += position[1] + 120
        self.game.background.blit(upgrade_text, upgrade_text_pos)

class LemonadeStand(Investment):
    def __init__(self, game):
        Investment.__init__(self, game)
        self.name = 'Lemonade Stand'
        self.level = 1
        self.initial_revenue = 1
        self.revenue = self.initial_revenue
        self.initial_cost = 4
        self.cost = self.initial_cost
        self.upgrade_scale = 1.07

class HotdogStand(Investment):
    def __init__(self, game):
        Investment.__init__(self, game)
        self.name = 'Hotdog Stand'
        self.level = 0
        self.initial_revenue = 60
        self.revenue = 0
        self.initial_cost = 60
        self.cost = self.initial_cost
        self.upgrade_scale = 1.15

class CarWash(Investment):
    def __init__(self, game):
        Investment.__init__(self, game)
        self.name = 'Car Wash'
        self.level = 0
        self.initial_revenue = 540
        self.revenue = 0
        self.initial_cost = 720
        self.cost = self.initial_cost
        self.upgrade_scale = 1.14

class PizzaDelivery(Investment):
    def __init__(self, game):
        Investment.__init__(self, game)
        self.name = 'Pizza Delivery'
        self.level = 0
        self.initial_revenue = 4320
        self.revenue = 0
        self.initial_cost = 8640
        self.cost = self.initial_cost
        self.upgrade_scale = 1.13