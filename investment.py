import math
import time
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
    if value < THOUSAND:
        new_val = value
        suffix = '  '
    elif value < MILLION:
        new_val /= float(THOUSAND)
        suffix = 'THO'
    elif value < BILLION:
        new_val /= float(MILLION)
        suffix = 'MIL'
    elif value < TRILLION:
        new_val /= float(BILLION)
        suffix = 'BIL'
    elif value < QUADRILLION:
        new_val /= float(TRILLION)
        suffix = 'TRI'
    elif value < QUINTILLION:
        new_val /= float(QUADRILLION)
        suffix = 'QUA'
    elif value < SEXTILLION:
        new_val /= float(QUINTILLION)
        suffix = 'QUI'
    elif value < SEPTILLION:
        new_val /= float(SEXTILLION)
        suffix = 'SEX'
    elif value < OCTILLION:
        new_val /= float(SEPTILLION)
        suffix = 'SEP'
    elif value < NONILLION:
        new_val /= float(OCTILLION)
        suffix = 'OCT'
    elif value < DECILLION:
        new_val /= float(NONILLION)
        suffix = 'NON'
    else:
        new_val /= float(DECILLION)
        suffix = 'DEC'
    return (new_val, suffix)

class Investment:
    SPACING = 16

    def __init__(self, game, inv_dict):
        self.game = game
        self.quantity = 0
        self.type = inv_dict['type']
        self.name = inv_dict['name']
        self.initial_cost = inv_dict['initial_cost']
        self.cost = self.initial_cost
        self.coefficient = inv_dict['coefficient']
        self.initial_time = inv_dict['initial_time']
        self.start_time = time.time()
        self.time = self.initial_time
        self.time_left = self.time
        self.initial_revenue = inv_dict['initial_revenue']
        self.revenue = 0
        self.revenue_scale = 1

    def get_upgrade_cost(self, number):
        sum = self.cost * self.coefficient
        for i in range(1, number):
            sum += sum * self.coefficient
        return sum

    def purchase(self):
        if self.game.currency < self.cost:
            return
        self.game.currency -= self.cost
        self.upgrade()

    def upgrade(self):
        self.quantity += 1
        if self.quantity % 10 == 0 and self.quantity != 0:
            self.revenue_scale += 1
        if self.quantity % 100 == 0 and self.quantity != 0:
            self.time /= 2
        self.revenue = self.quantity * self.initial_revenue * self.revenue_scale
        self.cost *= self.coefficient

    def update(self, game):
        if self.quantity > 0:
            cur_time = time.time()
            self.time_left = self.start_time + self.time - cur_time
            if self.time_left <= 0:
                self.time_left = self.time
                self.start_time = cur_time
                self.game.currency += self.revenue

    def render(self, position=(0, 0)):
        # Display Text
        name_text = self.game.font.render(self.name, 1, (255, 255, 255))
        name_text_pos = name_text.get_rect()
        name_text_pos.topleft = self.game.background.get_rect().topleft
        name_text_pos.x += position[0]
        name_text_pos.y += position[1] + (Investment.SPACING * self.game.background.get_height() / 450)
        self.game.background.blit(name_text, name_text_pos)

        quantity_text = self.game.font.render('Level: ' + str(self.quantity), 1, (255, 255, 255))
        quantity_text_pos = quantity_text.get_rect()
        quantity_text_pos.topleft = self.game.background.get_rect().topleft
        quantity_text_pos.x += position[0]
        quantity_text_pos.y += position[1] + (2 * Investment.SPACING * self.game.background.get_height() / 450)
        self.game.background.blit(quantity_text, quantity_text_pos)

        revenue, suffix = truncate_value(self.revenue)
        revenue_text = self.game.font.render('Revenue: ' + format(revenue, '6.2f') + ' ' + suffix, 1, (255, 255, 255))
        revenue_text_pos = revenue_text.get_rect()
        revenue_text_pos.topleft = self.game.background.get_rect().topleft
        revenue_text_pos.x += position[0]
        revenue_text_pos.y += position[1] + (3 * Investment.SPACING * self.game.background.get_height() / 450)
        self.game.background.blit(revenue_text, revenue_text_pos)

        cost, suffix = truncate_value(self.cost)
        upgrade_text = self.game.font.render('Upgrade: ' + format(cost, '6.2f') + ' ' + suffix, 1, (255, 255, 255))
        upgrade_text_pos = upgrade_text.get_rect()
        upgrade_text_pos.topleft = self.game.background.get_rect().topleft
        upgrade_text_pos.x += position[0]
        upgrade_text_pos.y += position[1] + (4 * Investment.SPACING * self.game.background.get_height() / 450)
        self.game.background.blit(upgrade_text, upgrade_text_pos)

        if self.quantity > 0:
            max_width = (200 * self.game.background.get_width() / 800)
            height = (15 * self.game.background.get_height() / 450)
            progress = 0
            if self.time > 0.15:
                progress = 1. - ((self.time_left) / (self.time))
                pygame.draw.rect(self.game.background, (255 - (255 * progress), 0 + (255 * progress), 0), pygame.Rect(position[0], position[1] + (5 * Investment.SPACING * self.game.background.get_height() / 450), max_width * progress, height))
                pygame.draw.rect(self.game.background, (128, 128, 128), pygame.Rect(position[0], position[1] + (5 * Investment.SPACING * self.game.background.get_height() / 450), max_width, height), 1)
            else:
                progress = 100
                pygame.draw.rect(self.game.background, (0, 255, 0), pygame.Rect(position[0], position[1] + (5 * Investment.SPACING * self.game.background.get_height() / 450), max_width, height))
                pygame.draw.rect(self.game.background, (128, 128, 128), pygame.Rect(position[0], position[1] + (5 * Investment.SPACING * self.game.background.get_height() / 450), max_width, height), 1)
