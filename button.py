import pygame


class Button:
    def __init__(
        self,
        x,y
        ,width,height,
        text = "Button",
        font = None,
        text_color = (255,255,255),
        button_color = (100,100,100),
        hover_color= (150,150,150),
        action = None,
    ):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False

        if font is None:
            if not pygame.font.get_init():
                pygame.font.init()
            self.font = pygame.font.Font(None,30)
        else:
            self.font = font

        #put text on surface
        self.text_surf = self.font.render(self.text,True,self.text_color)
        #center the text on the button
        self.text_rect = self.text_surf.get_rect (center=self.rect.center)

    def draw(self,surface):
        color = self.hover_color if self.is_hovered else self.button_color
        pygame.draw.rect(surface,color,self.rect,border_radius = 5)
        surface.blit(self.text_surf,self.text_rect)

    def handle_event(self,event):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        #checking for click now
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1 and self.is_hovered:
                if self.action:
                    self.action() # calls the function connected to the button
                return True #buttong is clicked
        return False #button not clicked
