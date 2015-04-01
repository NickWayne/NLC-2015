import pygame


class Menu(object):
    """handles everything about the menu; from
        storing and blitting text to handling
        input."""

    def __init__(self):
        """Creates the Menu, pretty self-explainitory"""
        
        self.menu_font = pygame.font.Font(None, 25)
        self.header_font = pygame.font.Font(None, 50)
        self.footer_font = pygame.font.Font(None, 15)

        self.texts = ["start", "tutorial", "help", "credits"]

        self.title = "NLC Game 2015"

        self.footer = "Open source project. NickandNicksGames 2015"

        self.text_rects = []
        self.title_render = self.header_font.render(self.title, True, (255, 255, 255))
        self.title_rect = self.title_render.get_rect()
        self.title_rect.center = (500, self.title_rect.h)

        self.text_rects.append(self.title_rect)

        for TEXT in self.texts:
            TEXT_render = self.menu_font.render(TEXT, True, (255, 255, 255))
            TEXT_index = self.texts.index(TEXT)
            
            TEXT_rect = TEXT_render.get_rect()
            TEXT_rect.center = (500, 
                    200 + TEXT_rect.h * TEXT_index * 3)

            self.text_rects.append(TEXT_rect)

        self.footer_render = self.footer_font.render(self.footer, True, (255, 255, 255))
        self.footer_rect = self.footer_render.get_rect()
        self.footer_rect.center = (500, 500 - self.footer_rect.h)
        
        self.text_rects.append(self.footer_rect)

    def handle_mouse_input(self, pos, buttons):
        if buttons[0]:
            for RECT in self.text_rects:
                if RECT.collidepoint(pos):
                    return self.text_rects.index(RECT)

        return None

    def render(self, surface):
        """Renders the text stored in the class to the screen"""

        surface.blit(self.title_render, self.title_rect)

        for TEXT in self.texts:
            TEXT_render = self.menu_font.render(TEXT, True, (255, 255, 255))
            TEXT_index = self.texts.index(TEXT)
            
            TEXT_rect = TEXT_render.get_rect()
            TEXT_rect.center = (500, 
                    200 + TEXT_rect.h * TEXT_index * 3)

            surface.blit(TEXT_render, TEXT_rect)

        surface.blit(self.footer_render, self.footer_rect)
