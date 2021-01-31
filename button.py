import pygame

class Button:
    COLOR_BACKGROUND = (0, 0, 0)
    COLOR_HOVER = (32, 32, 32)
    COLOR_CLICK = (64, 64, 64)
    COLOR_TEXT = (255, 255, 255)
    COLOR_BORDER_DARK = (128, 128, 128)
    COLOR_BORDER_LIGHT = (255, 255, 255)

    def __init__(self, game, x, y, width, height, text):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.clicked = False
        self.action = False

    def render(self):
        # Reset Action
        self.action = False

        # Get Cursor Position
        cur_pos = pygame.mouse.get_pos()

        # Create pygame Rect for Button
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Check Mouse Over and Click Conditions
        if button_rect.collidepoint(cur_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(self.game.background, Button.COLOR_CLICK, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                self.action = True
            else:
                pygame.draw.rect(self.game.background, Button.COLOR_HOVER, button_rect)
        else:
            pygame.draw.rect(self.game.background, Button.COLOR_BACKGROUND, button_rect)

        # Add Button Shading
        pygame.draw.line(self.game.background, Button.COLOR_BORDER_LIGHT, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(self.game.background, Button.COLOR_BORDER_LIGHT, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(self.game.background, Button.COLOR_BORDER_DARK,  (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.game.background, Button.COLOR_BORDER_DARK,  (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # Add Text to Button
        text_img = self.game.font.render(self.text, True, Button.COLOR_TEXT)
        text_w = text_img.get_width()
        text_h = text_img.get_height()
        self.game.background.blit(text_img, (self.x + self.width // 2 - text_w // 2, self.y + self.height // 2 - text_h // 2))
        return self.action