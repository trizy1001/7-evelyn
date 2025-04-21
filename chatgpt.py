import pygame as pg
from sys import exit 

pg.init()
clock = pg.time.Clock()
pg.font.init()

window = pg.display.set_mode((1024, 600), pg.RESIZABLE)
pg.display.set_caption("Evelyn")

# ---- Panel Position ---------------------------------------------------------------------------
x = 0
y = 0
# --- Panel Size -------------------------------------------------------------------------------
width = 200
height = 600

class ui_panels:
    def __init__(self):
        # ================================ Panel Variables ==============================================
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
        try:
            self.img_1 = pg.image.load("donuts/donut_1.png")
            self.img_2 = pg.image.load("donuts/donut_2.png")
            self.img_3 = pg.image.load("donuts/donut_3.png")
            self.img_4 = pg.image.load("donuts/donut_4.png")
        except:
            print("Warning: One or more donut images are missing.")
            self.img_1 = self.img_2 = self.img_3 = self.img_4 = pg.Surface((1,1))
        
        # -- Buttons -----------------------------------------------------------------------------------
        try:
            self.order_btn = pg.image.load("buttons/cart_button.png")
            self.pay_btn = pg.image.load("buttons/pay_btn.png")
            self.view_cart_btn = pg.image.load("buttons/button.png")
        except:
            print("Warning: One or more button images are missing.")
            self.order_btn = self.pay_btn = self.view_cart_btn = pg.Surface((1,1))
        
        # -- Fonts --------------------------------------------------------------------------------------
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
        
    def draw_header(self):
        title = self.title_font.render("7-EVELYN", True, "#ffffff")
        title_rect = title.get_rect(center=(x + 150, y + 30))  # adjusted y a bit for vertical centering

        try:
            logo = pg.image.load("new_logo.png")
            logo = pg.transform.scale(logo, (70, 65))
        except:
            print("Warning: Logo image not found.")
            logo = pg.Surface((70, 65))
            logo.fill("#ffffff")
        logo_rect = logo.get_rect(center=(x + 35, y + 33))

        window.blit(title, title_rect)
        window.blit(logo, logo_rect)

    def left_panel(self):
        mouse_pos = pg.mouse.get_pos() 
        left_panel_rect = pg.Rect(x, y + 65, self.left_pnl.get_width(), self.left_pnl.get_height())

        if left_panel_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            self.trigger_exp = True
        elif not left_panel_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            self.trigger_exp = False
                
        # Animate sliding effect
        if self.trigger_exp:
            self.frame_motion += self.animation
            if self.frame_motion >= 130:
                self.frame_motion = 130
        else:
            self.frame_motion -= self.animation
            if self.frame_motion <= 0:
                self.frame_motion = 0

        self.left_pnl = pg.Surface((self.frame_motion + 100, height))    
        self.left_pnl.fill(self.color)

    def draw(self):
        window.blit(self.header_pnl, (x, y))
        window.blit(self.left_pnl, (x, y + 65))
        window.blit(self.right_pnl, (x + 824, y))

panel = ui_panels()

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    
    window.fill("#545454")   
    panel.draw()
    panel.draw_header()
    panel.left_panel()
    

    pg.display.update()    
    clock.tick(90)
