import pygame


#define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

#define global variable
clicked = False
counter = 0


class button():
    # colours for button and text
    button_col = '#EA4C89'
    hover_col = '#F082AC'
    click_col = (50, 150, 255)
    text_col = white
    width = 250
    height = 70

    def __init__(self, x, y,font, text):
        self.x = x-self.width/2
        self.y = y -self.height/2
        self.text = text
        self.font= font

    def draw_button(self,screen):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect,0,20)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect,0,20)



        # add text to button
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 17    ))
        return action
