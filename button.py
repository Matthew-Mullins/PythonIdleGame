import pygame

class Button:
    COLOR_BACKGROUND = (0, 0, 0)
    COLOR_HOVER = (32, 32, 32)
    COLOR_CLICK = (64, 64, 64)
    COLOR_TEXT = (255, 255, 255)
    COLOR_BORDER_DARK = (128, 128, 128)
    COLOR_BORDER_LIGHT = (255, 255, 255)

    def __init__(self, game, text, state, function):
        self.game = game
        self.text = text
        self.state = state
        self.function = function
        self.clicked = False
        self.action = False

    def render(self, size, position):
        # Reset Action
        self.action = False

        # Get Cursor Position
        cur_pos = pygame.mouse.get_pos()
        scaled_cur_pos_x_bg = (cur_pos[0] - self.game.background_rect.topleft[0]) * (self.game.INIT_SCREEN_W / self.game.background_rect.width)
        scaled_cur_pos_y_bg = (cur_pos[1] - self.game.background_rect.topleft[1]) * (self.game.INIT_SCREEN_H / self.game.background_rect.height)
        scaled_cur_pos_x_nav = (scaled_cur_pos_x_bg - self.game.nav_bar_rect.topleft[0]) * (self.game.INIT_NAVBAR_W / self.game.nav_bar_rect.width)
        scaled_cur_pos_y_nav = (scaled_cur_pos_y_bg - self.game.nav_bar_rect.topleft[1]) * (self.game.INIT_NAVBAR_H / self.game.nav_bar_rect.height)
        scaled_cur_pos = (scaled_cur_pos_x_nav, scaled_cur_pos_y_nav)

        # Button Surface
        button_surface = pygame.Surface(size)
        button_surface_rect = button_surface.get_rect()
        button_surface_rect.midtop = position
        button_surface.convert()

        # Check Mouse Over and Click Conditions
        if button_surface_rect.collidepoint((scaled_cur_pos)):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                button_surface.fill(Button.COLOR_CLICK)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                self.action = True
            else:
                button_surface.fill(Button.COLOR_HOVER)
        else:
            button_surface.fill(Button.COLOR_BACKGROUND)

        # Add Button Shading
        pygame.draw.line(button_surface, Button.COLOR_BORDER_LIGHT, (0, 0), (size[0], 0), 2)
        pygame.draw.line(button_surface, Button.COLOR_BORDER_LIGHT, (0, 0), (0, size[1]), 2)
        pygame.draw.line(button_surface, Button.COLOR_BORDER_DARK,  (size[0] - 2, size[1] - 2), (size[0] - 2, -2), 2)
        pygame.draw.line(button_surface, Button.COLOR_BORDER_DARK,  (size[0] - 2, size[1] - 2), (-2, size[1] - 2), 2)

        # Add Text to Button
        button_font = pygame.font.Font(self.game.FONT_NAME, self.game.FONT_SIZE_H3)
        text_img = button_font.render(self.text, 1, Button.COLOR_TEXT)
        text_w = text_img.get_width()
        text_h = text_img.get_height()
        button_surface.blit(text_img, (size[0] // 2 - text_w // 2, size[1] // 2 - text_h // 2))
        self.game.nav_bar.blit(button_surface, button_surface_rect)
        return self.action