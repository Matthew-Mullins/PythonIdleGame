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
        suffix = 'THOUSAND'
    elif value < BILLION:
        new_val /= float(MILLION)
        suffix = 'MILLION'
    elif value < TRILLION:
        new_val /= float(BILLION)
        suffix = 'BILLION'
    elif value < QUADRILLION:
        new_val /= float(TRILLION)
        suffix = 'TRILLION'
    elif value < QUINTILLION:
        new_val /= float(QUADRILLION)
        suffix = 'QUADRILLION'
    elif value < SEXTILLION:
        new_val /= float(QUINTILLION)
        suffix = 'QUINTILLION'
    elif value < SEPTILLION:
        new_val /= float(SEXTILLION)
        suffix = 'SEXTILLION'
    elif value < OCTILLION:
        new_val /= float(SEPTILLION)
        suffix = 'SEPTILLION'
    elif value < NONILLION:
        new_val /= float(OCTILLION)
        suffix = 'OCTILLION'
    elif value < DECILLION:
        new_val /= float(NONILLION)
        suffix = 'NONILLION'
    else:
        new_val /= float(DECILLION)
        suffix = 'DECILLION'
    return (new_val, suffix)

class Investment:
    INIT_SPACING = 10
    INIT_INVESTMENT_W = 285
    INIT_INVESTMENT_H = 78

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
        self.revenue_multiple = 1
        self.unlocks = inv_dict.get('unlocks')

    def get_upgrade_cost(self, number):
        sum = self.cost * self.coefficient
        for i in range(1, number):
            sum += sum * self.coefficient
        return sum

    def purchase(self):
        if self.game.player.currency < self.cost:
            return
        self.game.player.currency -= self.cost
        self.upgrade()

    def upgrade(self):
        self.quantity += 1
        for unlock in self.unlocks:
            if unlock.get('goal') == self.quantity:
                for _type, investment in self.game.player.investments.items():
                    if _type == unlock.get('target_investment'):
                        investment.revenue_multiple *= unlock.get('profit_effect')
                        investment.time /= unlock.get('speed_effect')
        self.revenue = self.quantity * self.initial_revenue * self.revenue_multiple
        self.cost *= self.coefficient

    def update(self, game):
        if self.quantity > 0:
            cur_time = time.time()
            self.time_left = self.start_time + self.time - cur_time
            if self.time_left <= 0:
                self.time_left = self.time
                self.start_time = cur_time
                self.game.player.currency += self.revenue * self.game.player.revenue_scale

    def render(self, surface, position=(0, 0)):
        # Surface Width
        surface_w = surface.get_width()
        surface_h = surface.get_height()
        investment_w = int(Investment.INIT_INVESTMENT_W * surface_w / self.game.INIT_CONTENT_W)
        investment_h = int(Investment.INIT_INVESTMENT_H * surface_h / self.game.INIT_CONTENT_H)
        # Investment Surface
        investment_surface = pygame.Surface((investment_w, investment_h))
        investment_rect = investment_surface.get_rect()
        investment_surface.convert()
        # Add Button
        start_button = pygame.draw.circle(investment_surface, (128, 128, 128), (investment_h // 2, investment_h // 2), investment_h // 2, 2)
        name_split = self.name.split()
        name_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H5 * investment_h / Investment.INIT_INVESTMENT_H))
        for i in range(len(name_split)):
            name_text = name_font.render(name_split[i], 1, (255, 255, 255))
            name_text_rect = name_text.get_rect()
            name_text_rect.midtop = (start_button.midtop[0] + 0, start_button.midtop[1] + int(self.game.FONT_SIZE_H5 * investment_h / Investment.INIT_INVESTMENT_H) + int(self.game.FONT_SIZE_H5 * investment_h / Investment.INIT_INVESTMENT_H) * i)
            investment_surface.blit(name_text, name_text_rect)

        # Investment Quantity
        quantity_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H3 * investment_h / Investment.INIT_INVESTMENT_H))
        quantity_text = quantity_font.render(str(self.quantity), 1, (255, 255, 255))
        quantity_text_pos = quantity_text.get_rect()
        quantity_text_pos.midbottom = start_button.midbottom
        investment_surface.blit(quantity_text, quantity_text_pos)
        # Revenue Surface
        revenue_w = investment_w - investment_h
        revenue_h = investment_h // 2
        revenue_surface = pygame.Surface((revenue_w, revenue_h))
        revenue_rect = revenue_surface.get_rect()
        revenue_surface.convert()
        # Progress Bar
        if self.quantity > 0:
            max_width = revenue_w
            height = revenue_h
            progress = 0
            if self.time > 0.15:
                progress = 1. - ((self.time_left) / (self.time))
            else:
                progress = 1
            pygame.draw.rect(revenue_surface, (128 - (128 * progress), 0 + (128 * progress), 0), pygame.Rect(revenue_rect.left, revenue_rect.top, revenue_rect.width * progress, revenue_rect.height))
            pygame.draw.rect(revenue_surface, (128, 128, 128), revenue_rect, 1)
        # Revenue Text
        revenue, suffix = truncate_value(self.revenue)
        revenue_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H4 * investment_h / Investment.INIT_INVESTMENT_H))
        revenue_text = revenue_font.render(format(revenue, '.2f'), 1, (255, 255, 255))
        revenue_text_pos = revenue_text.get_rect()
        revenue_text_pos.midtop = revenue_rect.midtop
        revenue_surface.blit(revenue_text, revenue_text_pos)
        # Revenue Suffix Text
        suffix_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H5 * investment_h / Investment.INIT_INVESTMENT_H))
        suffix_text = suffix_font.render(suffix, 1, (255, 255, 255))
        suffix_text_pos = suffix_text.get_rect()
        suffix_text_pos.midbottom = revenue_rect.midbottom
        revenue_surface.blit(suffix_text, suffix_text_pos)
        investment_surface.blit(revenue_surface, (investment_h, 0))
        # Purchase Surface
        purchase_w = revenue_w - investment_h
        purchase_h = revenue_h
        purchase_surface = pygame.Surface((purchase_w, purchase_h))
        purchase_surface.fill((128, 64, 0))
        purchase_rect = purchase_surface.get_rect()
        purchase_surface.convert()
        purchase_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H5 * investment_h / Investment.INIT_INVESTMENT_H))
        # Buy Text
        buy_text = purchase_font.render("Buy", 1, (255, 255, 255))
        buy_text_pos = buy_text.get_rect()
        buy_text_pos.topleft = purchase_rect.topleft
        purchase_surface.blit(buy_text, buy_text_pos)
        # Buy Quantity Text
        buy_quantity_text = purchase_font.render("x" + "1", 1, (255, 255, 255))
        buy_quantity_text_pos = buy_quantity_text.get_rect()
        buy_quantity_text_pos.bottomleft = purchase_rect.bottomleft
        purchase_surface.blit(buy_quantity_text, buy_quantity_text_pos)
        # Cost Text
        cost, suffix = truncate_value(self.cost)
        cost_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H4 * investment_h / Investment.INIT_INVESTMENT_H))
        cost_text = cost_font.render(format(cost, '6.2f'), 1, (255, 255, 255))
        cost_text_pos = cost_text.get_rect()
        cost_text_pos.topright = purchase_rect.topright
        purchase_surface.blit(cost_text, cost_text_pos)
        # Cost Suffix Text
        suffix_text = purchase_font.render(suffix, 1, (255, 255, 255))
        suffix_text_pos = suffix_text.get_rect()
        suffix_text_pos.bottomright = purchase_rect.bottomright
        purchase_surface.blit(suffix_text, suffix_text_pos)
        investment_surface.blit(purchase_surface, (investment_h, revenue_h))
        # Time Surface
        time_w = revenue_w - purchase_w
        time_h = purchase_h
        time_surface = pygame.Surface((time_w, time_h))
        time_rect = time_surface.get_rect()
        time_surface.convert()
        # Time Text
        time_font = pygame.font.Font(self.game.FONT_NAME, int(self.game.FONT_SIZE_H5 * investment_h / Investment.INIT_INVESTMENT_H))
        time_text = time_font.render(format(self.time_left if self.time > 0.1 else 0, '05.02f'), 1, (255, 255, 255))
        time_text_pos = time_text.get_rect()
        time_text_pos.center = time_rect.center
        time_surface.blit(time_text, time_text_pos)
        investment_surface.blit(time_surface, (investment_h + purchase_w, revenue_h))

        surface.blit(investment_surface, position)
