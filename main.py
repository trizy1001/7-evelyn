import pygame as pg
import json
from sys import exit 



pg.init()
clock = pg.time.Clock()
pg.font.init()



window = pg.display.set_mode(((1024, 600)), pg.RESIZABLE)
pg.display.set_caption("Evelyn")

#---- Panel Position ---------------------------------------------------------------------------
x = 0
y = 0
    # --- Panel Size -------------------------------------------------------------------------------
width = 200
height = 600


class ui_panels:
    def __init__(self,):
# ================================ Panel Variables ===============================================================================

    # --- Panel Color ------------------------------------------------------------------------------
        self.color = "#000000"
        self.container_color = "#f5f5f5"
        self.button_color = "#87aee3"
    # -- Panels ------------------------------------------------------------------------------------
        self.header_pnl = pg.Surface((width + 615, 60))
        self.header_pnl.fill(self.color)
        self.left_pnl = pg.Surface((width, height))
        self.left_pnl.fill(self.color)
        self.right_pnl = pg.Surface((width + 795, height))
        self.right_pnl.fill(self.color)
    # -- products container ------------------------------------------------------------------------
        self.products_container = pg.Surface((width - 70, height - 500))  
        self.products_container.fill(self.container_color)
        
    # -- Product img -------------------------------------------------------------------------------
        self.img_1 = pg.image.load("donuts/donut_1.png")
        self.img_2 = pg.image.load("donuts/donut_2.png")
        self.img_3 = pg.image.load("donuts/donut_3.png")
        self.img_4 = pg.image.load("donuts/donut_4.png")
    # -- buttons -----------------------------------------------------------------------------------
        self.order_btn = pg.image.load("buttons/cart_button.png")
        self.pay_btn = pg.image.load("buttons/pay_btn.png")
        self.view_cart_btn = pg.image.load("buttons/button.png")
    # -- text ---------------------------------------------------------------------------------------
        self.title_font = pg.font.SysFont("Arial", 32)
        self.small_font = pg.font.SysFont("Arial", 16)
        self.medium_font = pg.font.SysFont("Arial", 20)
    # -- Others -------------------------------------------------------------------------------------
        self.trigger_exp = False
        self.animation = 20
        self.frame_motion = 0
        self.item_motion = 0
        self.select_item = None
        self.mouse_pressed = False
        self.scroll_y = 0
        
        
        # Load items once
        with open('item-data.json', 'r') as file:
            self.data_items = json.load(file)
        
#============  DTO GAGAWA NG MGA FUNCTIONS KINEME  ===========================================================

    
    def draw_header(self):
        self.title = self.title_font.render("7-EVELYN", True, "#ffffff")
        self.title_rect = self.title.get_rect(center=(x + 150, y + 20))
        self.logo = pg.image.load("new_logo.png")
        self.logo = pg.transform.scale(self.logo, (70, 65))
        self.logo_rect = self.logo.get_rect(center=(x + 35, y + 33))
        window.blit(self.title, self.title_rect)
        window.blit(self.logo, self.logo_rect)
    
    
    def left_panel(self):
        self.left_pnl_rect = self.left_pnl.get_rect(topleft=(x, y))
        mouse_pos = pg.mouse.get_pos() 
        
        if self.left_pnl_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            if not self.trigger_exp:
                self.trigger_exp = True
        elif not self.left_pnl_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            if not self.trigger_exp:
                self.trigger_exp = False
                
                
        if not self.trigger_exp:
            self.left_pnl = pg.Surface((self.frame_motion + 100, height))    
            self.left_pnl.fill(self.color)
            self.frame_motion -= self.animation
        else:
            self.left_pnl = pg.Surface((self.frame_motion + 100, height))
            self.left_pnl.fill(self.color)
            self.frame_motion += self.animation
            if self.frame_motion >= 130:
                self.frame_motion = 130    
    
    def scroll_pad(self):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4: self.scroll_y -= 30
            elif event.button == 5: self.scroll_y += 30
        if self.scroll_y >= 0:
            self.scroll_y = 0
    
    def items(self, category=None):
        display_items = self.data_items['items']
        if category:
            display_items = [item for item in display_items if item['category'] == category]

        x_offset, y_offset = 100, 100
        container_width, container_height = 200, 250
        items_container_row, item_sapcing = 4, 20
        
        for index, item in enumerate(display_items):
            if index % items_container_row == 0 and index != 0:
                x_offset = 100 
                y_offset += container_height + item_sapcing
                
            item = pg.Surface((container_width, container_height))
            item.fill(self.container_color)
            window.blit(item, (x_offset + 50, y_offset + self.scroll_y))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    def draw(self):
        window.blit(self.header_pnl, (x, y))
        window.blit(self.left_pnl, (x, y + 65))
        window.blit(self.right_pnl, (x + 824, y))
        
'''  

    `window.blit(self.title, self.title_rect)` is blitting (drawing) the rendered text surface
    `self.title` onto the main window surface at the position specified by `self.title_rect`. Similarly,
    `window.blit(self.logo, self.logo_rect)` is blitting the loaded and scaled logo image `self.logo`
    onto the main window surface at the position specified by `self.logo_rect`. This is how text and
    images are displayed on the screen in the specified positions within the UI panel.
'''   


panel = ui_panels()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            
    window.fill("#545454")   
    panel.draw()
    panel.draw_header()
    panel.left_panel()
    panel.scroll_pad()
    panel.items()
    
    
    
    pg.display.update()    
    clock.tick(90)