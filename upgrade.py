import math
import operator
import pygame

from investment import truncate_value

class Upgrade:
    INIT_SPACING = 10
    INIT_W = 285
    INIT_H = 78

    def __init__(self, game, upgrade_dict):
        self.game = game
        self.unlocked = False
        self.name = upgrade_dict.get('name')
        self.type = upgrade_dict.get('type')
        self.cost = upgrade_dict.get('cost')
        self.desc = upgrade_dict.get('description')
        effects = upgrade_dict.get('effects')
        self.sp_effect = effects.get('speed')
        self.pr_effect = effects.get('profit')

    def purchase(self, player):
        if self.unlocked:
            return
        if player.currency < self.cost:
            return
        player.currency -= self.cost
        self.unlock()

    def unlock(self):
        self.unlocked = True
        for investment in self.game.player.investments.values():
            if self.type == investment.type:
                investment.revenue_multiple *= self.pr_effect
                investment.time /= self.sp_effect
                investment.time_left = min(investment.time_left, investment.time)
            elif self.type == 'all':
                investment.revenue_multiple *= self.pr_effect
                investment.time /= self.sp_effect
                investment.time_left = min(investment.time_left, investment.time)
            investment.update_revenue()

    def render(self, index):
        if self.unlocked:
            return False
        # Upgrade Positions
        upgrade_x = int(Upgrade.INIT_SPACING + (Upgrade.INIT_SPACING * (index % 2)) + Upgrade.INIT_W * (index % 2))
        upgrade_y = int(Upgrade.INIT_SPACING + (Upgrade.INIT_SPACING * math.floor(index / 2)) + (Upgrade.INIT_H * math.floor(index / 2)))
        # Upgrade Surface
        upgrade_surface = pygame.Surface((Upgrade.INIT_W, Upgrade.INIT_H))
        upgrade_surface_rect = upgrade_surface.get_rect()
        upgrade_surface_rect.topleft = (upgrade_x, upgrade_y)
        upgrade_surface.convert()
        # Upgrade Name
        upgrade_name_text = self.game.font_h4.render(self.name, 1, (255, 255, 255))
        upgrade_name_text_rect = upgrade_name_text.get_rect()
        upgrade_name_text_rect.topleft = tuple(map(operator.sub, upgrade_surface_rect.topleft, upgrade_surface_rect.topleft))
        upgrade_surface.blit(upgrade_name_text, upgrade_name_text_rect)
        # Upgrade Type
        upgrade_type_text = self.game.font_h4.render(self.type, 1, (255, 255, 255))
        upgrade_type_text_rect = upgrade_type_text.get_rect()
        upgrade_type_text_rect.midleft = tuple(map(operator.sub, upgrade_surface_rect.midleft, upgrade_surface_rect.topleft))
        upgrade_surface.blit(upgrade_type_text, upgrade_type_text_rect)
        # Upgrade Description
        upgrade_desc_text = self.game.font_h5.render(self.desc, 1, (255, 255, 255))
        upgrade_desc_text_rect = upgrade_desc_text.get_rect()
        upgrade_desc_text_rect.bottomleft = tuple(map(operator.sub, upgrade_surface_rect.bottomleft, upgrade_surface_rect.topleft))
        upgrade_surface.blit(upgrade_desc_text, upgrade_desc_text_rect)
        # Upgrade Button
        upgrade_button_surface = pygame.Surface((Upgrade.INIT_H, Upgrade.INIT_H))
        upgrade_button_surface.fill((255, 165, 0))
        upgrade_button_surface_rect = upgrade_button_surface.get_rect()
        upgrade_button_surface_rect.topright = tuple(map(operator.sub, upgrade_surface_rect.topright, upgrade_surface_rect.topleft))
        # Check Button Hover
        cur_pos = pygame.mouse.get_pos()
        cur_pos_scaled_bg_x = int((cur_pos[0] - self.game.background_rect.topleft[0]) * self.game.INIT_SCREEN_W / self.game.background_rect.width)
        cur_pos_scaled_bg_y = int((cur_pos[1] - self.game.background_rect.topleft[1]) * self.game.INIT_SCREEN_H / self.game.background_rect.height)
        cur_pos_scaled_content_x = int((cur_pos_scaled_bg_x - self.game.content_rect.topleft[0]) * (self.game.INIT_CONTENT_W / self.game.content_rect.width))
        cur_pos_scaled_content_y = int((cur_pos_scaled_bg_y - self.game.content_rect.topleft[1]) * (self.game.INIT_CONTENT_H / self.game.content_rect.height))
        cur_pos_scaled_upgrade_x = int((cur_pos_scaled_content_x - upgrade_x) * (Upgrade.INIT_W / upgrade_surface_rect.width))
        cur_pos_scaled_upgrade_y = int((cur_pos_scaled_content_y - upgrade_y) * (Upgrade.INIT_H / upgrade_surface_rect.height))
        cur_pos_scaled = (cur_pos_scaled_upgrade_x, cur_pos_scaled_upgrade_y)

        # Check Button Hover
        if self.cost < self.game.player.currency:
            if upgrade_button_surface_rect.collidepoint(cur_pos_scaled):
                upgrade_button_surface.fill((128, 80, 0))
                if self.game.mouse_buttons_pressed[0]:
                    self.purchase(self.game.player)
        else:
            upgrade_button_surface.fill((128, 128, 128))
        
        # Upgrade Cost
        cost, suffix = truncate_value(self.cost)
        upgrade_cost_text = self.game.font_h4.render(format(cost, '.2f'), 1, (0, 0, 0))
        upgrade_cost_text_rect = upgrade_cost_text.get_rect()
        upgrade_cost_text_rect.midtop = tuple(map(operator.sub, upgrade_button_surface_rect.midtop, upgrade_button_surface_rect.topleft))
        upgrade_button_surface.blit(upgrade_cost_text, upgrade_cost_text_rect)
        # Cost Suffix
        suffix_text = self.game.font_h5.render(suffix, 1, (0, 0, 0))
        suffix_text_rect = suffix_text.get_rect()
        suffix_text_rect.midtop = upgrade_cost_text_rect.midbottom
        upgrade_button_surface.blit(suffix_text, suffix_text_rect)
        # Buy Text
        buy_text = self.game.font_h3.render('Buy', 1, (0, 0, 0))
        buy_text_rect = buy_text.get_rect()
        buy_text_rect.midbottom = tuple(map(operator.sub, upgrade_button_surface_rect.midbottom, upgrade_button_surface_rect.topleft))
        
        upgrade_button_surface.blit(buy_text, buy_text_rect)
        upgrade_surface.blit(upgrade_button_surface, upgrade_button_surface_rect)
        self.game.content.blit(upgrade_surface, upgrade_surface_rect)
        return True