import math
import time
import operator
import pygame

from utility import truncate_value

class Investment:
    INIT_SPACING = 10
    INIT_INVESTMENT_W = 285
    INIT_INVESTMENT_H = 78

    def __init__(self, game, inv_dict):
        self.game = game

        self.type               = inv_dict.get('type')
        self.name               = inv_dict.get('name')
        self.initial_cost       = inv_dict.get('initial_cost')
        self.coefficient        = inv_dict.get('coefficient')
        self.initial_time       = inv_dict.get('initial_time')
        self.initial_revenue    = inv_dict.get('initial_revenue')
        self.unlocks            = inv_dict.get('unlocks')
        self.has_started        = inv_dict.get('has_started')

        self.quantity = 0
        
        self.cost = self.initial_cost
        self.cost_scale = 1
        
        self.time = self.initial_time
        self.time_left = 0
        self.last_time = 0
        
        self.revenue = 0
        self.revenue_multiple = 1

        self.is_managed = False

    def serialize(self):
        investment_dict = {}
        investment_dict['quantity']     = self.quantity
        investment_dict['time_left']    = self.time_left
        investment_dict['has_started']  = self.has_started
        investment_dict['is_managed']   = self.is_managed
        return investment_dict

    def deserialize(self, investment_dict):
        self.upgrade(investment_dict.get('quantity'))
        self.time_left = investment_dict.get('time_left')
        self.last_time = time.time()
        self.has_started = investment_dict.get('has_started')

    def reset(self):
        self.quantity = 0
        self.cost = self.initial_cost
        self.cost_scale = 1
        self.time = self.initial_time
        self.time_left = 0
        self.last_time = 0
        self.revenue = 0
        self.revenue_multiple = 1

    def start(self):
        if not self.has_started and self.quantity > 0:
            self.has_started = True
            cur_time = time.time()
            self.time_left = self.time
            self.last_time = cur_time

    def update(self):
        if self.has_started:
            cur_time = time.time()
            self.time_left -= cur_time - self.last_time
            self.last_time = cur_time
            if self.time_left <= 0:
                self.game.player.currency += self.revenue
                self.game.player.lifetime_earnings += self.revenue
                self.has_started = False
                self.time_left = self.time
                if self.is_managed:
                    self.start()

    def purchase(self, quantity):
        if self.game.player.currency < self.get_upgrade_cost(quantity):
            return
        self.game.player.currency -= self.get_upgrade_cost(quantity)
        self.upgrade(quantity)

    def get_upgrade_cost(self, quantity):
        sum = (self.cost * self.cost_scale) * self.coefficient
        for i in range(1, quantity):
            sum += sum * self.coefficient
        return sum

    def upgrade(self, quantity):
        for _ in range(quantity):
            self.quantity += 1
            for unlock in self.unlocks:
                if unlock.get('goal') == self.quantity:
                    for _type, investment in self.game.player.investments.items():
                        if _type == unlock.get('target_investment'):
                            investment.revenue_multiple *= unlock.get('profit_effect')
                            investment.time /= unlock.get('speed_effect')
                            investment.time_left = min(investment.time_left, investment.time)
                            investment.update_revenue()
            self.update_revenue()
            self.cost *= self.coefficient

    def update_revenue(self):
        self.revenue = self.quantity * self.initial_revenue * self.revenue_multiple

    def render(self, surface, position=(0, 0)):
        # Surface Width
        surface_w = surface.get_width()
        surface_h = surface.get_height()
        investment_w = Investment.INIT_INVESTMENT_W
        investment_h = Investment.INIT_INVESTMENT_H
        # Investment Surface
        investment_surface = pygame.Surface((investment_w, investment_h), pygame.SRCALPHA)
        investment_rect = investment_surface.get_rect()
        investment_rect.topleft = tuple(map(operator.add, self.game.content_rect.topleft, position))
        investment_surface.convert()
        pygame.draw.rect(investment_surface, (0, 0, 0), pygame.Rect(0, 0, investment_w, investment_h), border_top_left_radius=(investment_h // 2), border_bottom_left_radius=(investment_h // 2))
        # Add Button
        start_button = pygame.draw.circle(investment_surface, (128, 128, 128), (investment_h // 2, investment_h // 2), investment_h // 2, 2)
        # Scale Cursor Position
        cur_pos = pygame.mouse.get_pos()
        cur_pos_scaled_bg_x = int((cur_pos[0] - self.game.background_rect.topleft[0]) * (self.game.INIT_SCREEN_W / self.game.background_rect.width))
        cur_pos_scaled_bg_y = int((cur_pos[1] - self.game.background_rect.topleft[1]) * (self.game.INIT_SCREEN_H / self.game.background_rect.height))
        cur_pos_scaled_content_x = int((cur_pos_scaled_bg_x - self.game.content_rect.topleft[0]) * (self.game.INIT_CONTENT_W / self.game.content_rect.width))
        cur_pos_scaled_content_y = int((cur_pos_scaled_bg_y - self.game.content_rect.topleft[1]) * (self.game.INIT_CONTENT_H / self.game.content_rect.height))
        cur_pos_scaled_inv_x = int((cur_pos_scaled_content_x - position[0]) * (Investment.INIT_INVESTMENT_W / investment_rect.width))
        cur_pos_scaled_inv_y = int((cur_pos_scaled_content_y - position[1]) * (Investment.INIT_INVESTMENT_H / investment_rect.height))
        cur_pos_scaled = (cur_pos_scaled_inv_x, cur_pos_scaled_inv_y)

        if start_button.collidepoint(cur_pos_scaled):
            start_button = pygame.draw.circle(investment_surface, (192, 192, 192), (investment_h // 2, investment_h // 2), investment_h // 2, 2)
            if self.game.mouse_buttons_pressed[0]:
                self.start()
                
        # Investment Name
        name_split = self.name.split()
        name_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H5)
        for i in range(len(name_split)):
            name_text = name_font.render(name_split[i], 1, (255, 255, 255))
            name_text_rect = name_text.get_rect()
            name_text_rect.midtop = start_button.midtop
            name_text_rect.midtop = tuple(map(operator.add, name_text_rect.midtop, (0, self.game.FONT_SIZE_H5 + self.game.FONT_SIZE_H5 * i)))
            investment_surface.blit(name_text, name_text_rect)
        # Investment Quantity
        quantity_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H3)
        quantity_text = quantity_font.render(str(self.quantity), 1, (255, 255, 255))
        quantity_text_rect = quantity_text.get_rect()
        quantity_text_rect.midbottom = start_button.midbottom
        investment_surface.blit(quantity_text, quantity_text_rect)
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
                progress = 1. - max(0, ((self.time_left) / (self.time)))
            else:
                progress = 1
            pygame.draw.rect(revenue_surface, (128 * (1 - progress), 128 * progress, 0), pygame.Rect(revenue_rect.left, revenue_rect.top, revenue_rect.width * progress, revenue_rect.height))
            pygame.draw.rect(revenue_surface, (128, 128, 128), revenue_rect, 1)
        # Revenue Text
        revenue, suffix = truncate_value(self.revenue)
        revenue_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H4)
        revenue_text = revenue_font.render(format(revenue, '.2f'), 1, (255, 255, 255))
        revenue_text_pos = revenue_text.get_rect()
        revenue_text_pos.midtop = revenue_rect.midtop
        revenue_surface.blit(revenue_text, revenue_text_pos)
        # Revenue Suffix Text
        suffix_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H5)
        suffix_text = suffix_font.render(suffix, 1, (255, 255, 255))
        suffix_text_pos = suffix_text.get_rect()
        suffix_text_pos.midbottom = revenue_rect.midbottom
        revenue_surface.blit(suffix_text, suffix_text_pos)
        investment_surface.blit(revenue_surface, (investment_h, 0))
        # Purchase Surface
        purchase_w = revenue_w - investment_h
        purchase_h = revenue_h
        purchase_surface = pygame.Surface((purchase_w, purchase_h))
        purchase_surface.fill((255, 165, 0))
        purchase_rect = purchase_surface.get_rect()
        purchase_rect.bottomleft = start_button.bottomright
        purchase_surface.convert()
        purchase_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H4)
        if purchase_rect.collidepoint(cur_pos_scaled):
            purchase_surface.fill((128, 80, 0))
            if self.game.mouse_buttons_pressed[0]:
                self.purchase(1)
        # Buy Text
        buy_text = purchase_font.render("Buy", 1, (0, 0, 0))
        buy_text_pos = buy_text.get_rect()
        buy_text_pos.topleft = tuple(map(operator.sub, purchase_rect.topleft, purchase_rect.topleft))
        purchase_surface.blit(buy_text, buy_text_pos)
        # Buy Quantity Text
        buy_quantity_text = purchase_font.render("x" + "1", 1, (0, 0, 0))
        buy_quantity_text_pos = buy_quantity_text.get_rect()
        buy_quantity_text_pos.bottomleft = tuple(map(operator.sub, purchase_rect.bottomleft, purchase_rect.topleft))
        purchase_surface.blit(buy_quantity_text, buy_quantity_text_pos)
        # Cost Text
        cost, suffix = truncate_value(self.get_upgrade_cost(1))
        cost_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H4)
        cost_text = cost_font.render(format(cost, '6.2f'), 1, (0, 0, 0))
        cost_text_pos = cost_text.get_rect()
        cost_text_pos.topright = tuple(map(operator.sub, purchase_rect.topright, purchase_rect.topleft))
        purchase_surface.blit(cost_text, cost_text_pos)
        # Cost Suffix Text
        suffix_text = purchase_font.render(suffix, 1, (0, 0, 0))
        suffix_text_pos = suffix_text.get_rect()
        suffix_text_pos.bottomright = tuple(map(operator.sub, purchase_rect.bottomright, purchase_rect.topleft))
        purchase_surface.blit(suffix_text, suffix_text_pos)
        investment_surface.blit(purchase_surface, (investment_h, revenue_h))
        # Time Surface
        time_w = revenue_w - purchase_w
        time_h = purchase_h
        time_surface = pygame.Surface((time_w, time_h))
        time_rect = time_surface.get_rect()
        time_surface.convert()
        # Time Text
        time_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H5)
        time_text = time_font.render(format(self.time_left if self.time > 0.5 else 0, '05.02f'), 1, (255, 255, 255))
        time_text_pos = time_text.get_rect()
        time_text_pos.center = time_rect.center
        time_surface.blit(time_text, time_text_pos)
        investment_surface.blit(time_surface, (investment_h + purchase_w, revenue_h))
        surface.blit(investment_surface, tuple(map(operator.sub, investment_rect.topleft, self.game.content_rect.topleft)))