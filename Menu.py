import pygame,ImageFuncs,webbrowser



class Menu(object):
    """handles everything about the menu; from
        storing and blitting text to handling
        input."""

    def __init__(self):
        """Creates the Menu, pretty self-explainitory"""
        
        self.menu_font = pygame.font.Font("pixelFont.ttf", 25)
        self.header_font = pygame.font.Font("pixelFont.ttf", 32)
        self.footer_font = pygame.font.Font("pixelFont.ttf", 15)

        self.texts = ["START", "TUTORIAL", "HELP", "LINKS", "QUIT"]

        self.title = "NLC Game and Simulation Submission - 2015"

        self.footer = "Open source project. NickandNicksGames 2015"

        self.text_rects = []
        self.title_render = self.header_font.render(self.title, True, (255, 255, 255))
        self.title_rect = self.title_render.get_rect()
        self.title_rect.center = (500, self.title_rect.h)
        self.clicked = False
        self.clicked_time = 0

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
        self.footer_rect.center = (500, 600 - self.footer_rect.h)
        
        self.text_rects.append(self.footer_rect)

    def handle_mouse_input(self, pos, buttons, help = False, rects = []):
        if help == False:
            if buttons[0]:
                for RECT in self.text_rects:
                    if RECT.collidepoint(pos):
                        return self.text_rects.index(RECT)

        else:
            if buttons[0]:
                for RECT in rects:
                    if RECT.collidepoint(pos):
                        return rects.index(RECT)

        return None

    def help_screen(self,screen,mouse_pos):
        screen.fill((0,0,0))
        self.img = pygame.image.load("res/base.png").convert()
        self.ImageFuncs = ImageFuncs.ImageFuncs(32,32,self.img)
        self.img_lst = []
        self.img_lst.append(self.ImageFuncs.get_image(0,1))
        self.img_lst.append(self.ImageFuncs.get_image(1,2))
        self.img_lst.append(self.ImageFuncs.get_image(0,3))
        self.img_lst.append(self.ImageFuncs.get_image(2,2))
        menu_cursor_image = self.ImageFuncs.get_image(3, 1)
        menu_cursor_image.set_colorkey((255, 0, 255))

        open_file = open("helptxt.txt", 'r')
        linelst =[]
        contents = open_file.readlines()
        for i in range(len(contents)):
             linelst.append(contents[i].strip('\n'))
        for i in linelst:
            if i == '':
                linelst.pop(linelst.index(i))
        open_file.close()



        for i in self.img_lst:
            i.set_colorkey((255,0,255))
            index = self.img_lst.index(i)
            screen.blit(i,(100, 100 + i.get_height() * index * 3))
            txt = self.menu_font.render(linelst[index], True, (255, 255, 255))
            txt_rect = txt.get_rect()
            txt_rect.midleft = (160,117 + i.get_height() * index * 3)
            screen.blit(txt,txt_rect)

        txt = self.menu_font.render("Press ESCAPE to go back", True, (255, 0, 255))
        txt_rect = txt.get_rect()
        txt_rect.center = (500, 500)
        screen.blit(txt,txt_rect)
        screen.blit(menu_cursor_image, (mouse_pos[0]-16, mouse_pos[1]-16))




    def links(self,screen,mouse_pos,tick):
        screen.fill((0,0,0))
        self.img = pygame.image.load("res/base.png").convert()
        self.ImageFuncs = ImageFuncs.ImageFuncs(32,32,self.img)
        self.img_lst = []
        self.img_lst.append(self.ImageFuncs.get_image(0,1))
        self.img_lst.append(self.ImageFuncs.get_image(1,2))
        self.img_lst.append(self.ImageFuncs.get_image(0,3))
        self.img_lst.append(self.ImageFuncs.get_image(2,2))
        menu_cursor_image = self.ImageFuncs.get_image(3, 1)
        menu_cursor_image.set_colorkey((255, 0, 255))

        open_file = open("links.txt", 'r')
        linelst =[]
        text_rects = []
        contents = open_file.readlines()
        for i in range(len(contents)):
             linelst.append(contents[i].strip('\n'))
        for i in linelst:
            if i == '':
                linelst.pop(linelst.index(i))
        open_file.close()



        for i in self.img_lst:
            i.set_colorkey((255,0,255))
            index = self.img_lst.index(i)
            screen.blit(i,(100, 100 + i.get_height() * index * 3))
            txt = self.menu_font.render(linelst[index], True, (255, 255, 255))
            txt_rect = txt.get_rect()
            text_rects.append(txt_rect)
            txt_rect.midleft = (160,117 + i.get_height() * index * 3)
            screen.blit(txt,txt_rect)

        txt = self.menu_font.render("Press ESCAPE to go back", True, (255, 0, 255))
        txt_rect = txt.get_rect()
        txt_rect.center = (500, 500)
        screen.blit(txt,txt_rect)
        screen.blit(menu_cursor_image, (mouse_pos[0]-16, mouse_pos[1]-16))

        option = self.handle_mouse_input(mouse_pos, pygame.mouse.get_pressed(),True,text_rects)
        for event in pygame.event.get():
            if option is not None and event.type == pygame.MOUSEBUTTONUP:
                if option == 0:
                    self.clicked = True
                    webbrowser.open_new(r"http://en.wikipedia.org/wiki/Computer_virus")
                if option == 1:
                    self.clicked = True
                    webbrowser.open_new(r"http://en.wikipedia.org/wiki/Rootkit")
                if option == 2:
                    self.clicked = True
                    webbrowser.open_new(r"http://en.wikipedia.org/wiki/Spambot")
                if option == 3:
                    self.clicked = True
                    webbrowser.open_new(r"http://en.wikipedia.org/wiki/Web_Bot")



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
