import pygame as pg
from pygame.locals import *
from sys import exit
import json
# Initialize Pygame
pg.init()
pg.font.init()
# DISPLAY SET UP
width, height = 1024, 600    
window = pg.display.set_mode((width, height))
pg.display.set_caption("Pygame Window")
clock = pg.time.Clock()
# SCREEN SETTINGS
WIDTH, HEIGHT = 1024, 600
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption('7/EVELYN Ordering System')
# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (100, 149, 237)
LIGHT_BLUE = (173, 216, 230)
SCREEN_COLOR = "#545454"
# POSITIONING
x = 0
y = 0
width = 200
height = 600
# FONTS
txt_color = WHITE 
small_font = pg.font.SysFont('Arial', 18)
medium_font = pg.font.SysFont('Arial', 24)
large_font = pg.font.SysFont('Arial', 36)
#===============================================================================================================
#=============================== ****HEADER PANEL ****===========================================================
#===============================================================================================================
class top_panel:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 700
        self.height = 60
        
        self.header_pnl_rect = pg.Rect(self.x, self.y, self.width, self.height)
        
        self.txt_color = WHITE 
        self.small_font = pg.font.SysFont('Arial', 18)
        self.medium_font = pg.font.SysFont('Arial', 24)
        self.large_font = pg.font.SysFont('Arial', 36)
        
    def draw_header(self):
        pg.draw.rect(window, BLACK, self.header_pnl_rect, 0, border_bottom_right_radius=20)
        
        logo = pg.image.load("new_logo.png").convert_alpha()
        logo = pg.transform.scale(logo, (70, 70))
        logo_rect = logo.get_rect(center=(self.x + 35, self.y + 38))
        window.blit(logo, logo_rect)
        
        self.text = self.large_font.render("7-EVELYN", True, self.txt_color)
        window.blit(self.text, (self.x + 80, self.y + 10))

header = top_panel()
#===============================================================================================================
#=============================== ****LEFT PANEL ****============================================================
#===============================================================================================================
class left_panel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.txt_color = BLACK
        self.small_font = pg.font.SysFont('Arial', 18)
        self.medium_font = pg.font.SysFont('Arial', 24)
        self.large_font = pg.font.SysFont('Arial', 36)

        self.left_pnl_rect = pg.Rect(self.x, self.y + 74, self.width - 130, self.height)
        
        self.sidebar_expanded = False
        self.panel_width = 200
        self.toggle_button = pg.Rect(5, 85, 60, 40)

        self.scroll_y = 0
        self.scroll_speed = 50
        self.max_scroll = 0
        
        self.animation = 100
        self.frame_motion = 0
        self.trigger_exp = False

        with open('item-data.json', 'r') as file:
            self.data_items = json.load(file)

        self.selected_category = None
# ===============================================================================================================
    def draw_left_pnl(self):
            # Draw the sidebar with current width (animated)
            self.left_pnl_rect = pg.Rect(self.x, self.y + 74, self.frame_motion, self.height)
            pg.draw.rect(window, BLACK, self.left_pnl_rect, 0, border_bottom_right_radius=20, border_top_right_radius=20)
            
            # Update toggle button position based on sidebar position
            self.toggle_button = pg.Rect(8, 90, 50, 40)
            pg.draw.rect(window, WHITE, self.toggle_button, 0, border_radius=3)
            pg.draw.line( window, BLACK, (10, 100), (50, 100), 3)
            pg.draw.line( window, BLACK, (10, 110), (50, 110), 3)
            pg.draw.line( window, BLACK, (10, 120), (50, 120), 3)
# ===============================================================================================================
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if self.toggle_button.collidepoint(mouse_x, mouse_y):
                self.sidebar_expanded = not self.sidebar_expanded

        elif event.type == pg.MOUSEWHEEL:
            self.scroll_y += event.y * self.scroll_speed
            self.scroll_y = max(-self.max_scroll, min(0, self.scroll_y))
# ===============================================================================================================
    def behavior(self):
        # Animate sidebar width
        if not self.sidebar_expanded and self.frame_motion > 0:
                self.frame_motion -= self.animation
                if self.frame_motion < 0:
                    self.frame_motion = 0
        if self.sidebar_expanded and self.frame_motion < 130:
                self.frame_motion += self.animation
                if self.frame_motion > 130:
                    self.frame_motion = 130
        self.left_pnl_rect = pg.Rect((self.x, self.y + 74, self.frame_motion + 70, height))
        pg.draw.rect(window, BLACK, self.left_pnl_rect, 0, border_bottom_right_radius=20, border_top_right_radius=20) 
# ===============================================================================================================
    def draw_items(self, category=None):
        items_to_draw = self.data_items['items']
        if category:
            items_to_draw = [item for item in self.data_items['items'] if item['category'] == category]

        # Layout settings
        item_space = 30
        items_per_row = 3
        item_width = 150
        item_height = 200

        # row ng items na ilalagay 
        total_rows = (len(items_to_draw) + items_per_row - 1) // items_per_row
        content_height = total_rows * (item_height + item_space)
        visible_height = self.height - 200  # Adjust based on top margin

        self.max_scroll = max(0, content_height - visible_height)

        # ito yung backgorund ng scroll pad
        items_area = pg.Rect(self.frame_motion + 95, 150, self.frame_motion + 700, visible_height)
        pg.draw.rect(window, SCREEN_COLOR, items_area, 0, border_radius=10)

        # dto nmn mag babase yung mga items kung san sila makikita or nakadisplay
        item_y = 180 + self.scroll_y
        item_x = self.frame_motion + 60  # x position for items

        for index, item in enumerate(items_to_draw):
            rect = pg.Rect(item_x + 18, item_y, item_width, item_height)

            if items_area.colliderect(rect):
                pg.draw.rect(window, WHITE, rect, 0, border_radius=10)
                try:
                    item_image = pg.image.load(item["image"]).convert_alpha()
                    item_image = pg.transform.scale(item_image, (item_width - 50, item_height - 100))
                    img_rect = item_image.get_rect(center=(item_x + item_width // item_space + 90, item_y + item_height // 2 - 40))
                    window.blit(item_image, img_rect)
                except FileNotFoundError:
                    pass

                item_name = self.small_font.render(item['name'], True, BLACK)
                item_price = self.small_font.render(f"${item['value']}", True, BLACK)
                window.blit(item_name, (item_x + 30, item_y + item_height - 80))
                window.blit(item_price, (item_x + 30, item_y + item_height - 60))
                
                self.btn_rect = pg.Rect(item_x + item_width // item_space + 40, item_y + item_height // 2 + 67, 100, 25)
                pg.draw.rect(window, BLUE, self.btn_rect, 0, border_radius=5)
                self.btn_text = self.small_font.render("Add to Cart", True, WHITE)
                btn_text_rect = self.btn_text.get_rect(center=self.btn_rect.center)
                window.blit(self.btn_text, btn_text_rect)

            item_x += item_width + item_space
            if (index + 1) % items_per_row == 0:
                item_x = self.frame_motion + 60  # reset x
                item_y += item_height + item_space  # new row
# ===============================================================================================================
    def side_bar(self):
        panel.behavior() == self.frame_motion + 70
        
        if panel.frame_motion > 0:
            panel.behavior()

            # Draw the category buttons
            y_offset = 150
            item_w = 60
            item_h = 60
            x = 5

            for item in self.data_items['categories']:
                category_width = 180  # fixed width for consistency
                category_height = item_h + 20
                category_rect = pg.Rect(x + 10, y_offset, category_width, category_height)
                pg.draw.rect(window, WHITE, category_rect, 0, border_radius=10)

                try:
                    item_image = pg.image.load(item["image"]).convert_alpha()
                    item_image = pg.transform.scale(item_image, (item_w, item_h))
                    item_image_rect = item_image.get_rect(center=(x + 50, y_offset + category_height // 2))
                    window.blit(item_image, item_image_rect)
                except FileNotFoundError:
                    pass

                # Render category name beside image
                text = self.medium_font.render(item['name'], True, BLACK)
                text.set_alpha(self.frame_motion)
                window.blit(text, (x + 100, y_offset + 20))

                if category_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
                    self.selected_category = item['category']

                y_offset += 90

        panel.toggle_button = pg.Rect(8, 90, 50, 40)
        pg.draw.rect(window, WHITE, panel.toggle_button, 0, border_radius=3)
        pg.draw.line( window, BLACK, (10, 100), (50, 100), 3)
        pg.draw.line( window, BLACK, (10, 110), (50, 110), 3)
        pg.draw.line( window, BLACK, (10, 120), (50, 120), 3)
        panel.draw_items(self.selected_category)

panel = left_panel(x, y, width, height)
#===============================================================================================================
#=============================== ****RIGHT PANEL ****===========================================================
#===============================================================================================================
class RightPanel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = BLACK
        self.txt_color = WHITE
        self.font = pg.font.SysFont('Arial', 20)
        self.bold_font = pg.font.SysFont('Arial', 22, bold=True)
        
        with open('item-data.json', 'r') as f:
            self.cart_data = json.load(f)
        
        self.selected_category=None
        self.current_index = 0
        self.load_cart()

    def load_cart(self):
        try:
            with open("user_data.json", "r") as f:
                self.cart_data = json.load(f)
        except FileNotFoundError:
            self.cart_data = []

    def draw_right_pnl(self):
        
        right_panel_rect = pg.Rect(self.x + 725, self.y, self.width + 100, self.height)
        pg.draw.rect(window, BLACK, right_panel_rect, 0, border_top_left_radius=25)

        order_box = pg.Rect(self.x + 780, self.y + 100, self.width, self.height - 300)
        pg.draw.rect(window, WHITE, order_box, 0, border_radius=25)
        
        pay_btn = pg.Rect(self.x + 780, self.y + order_box.bottom + 50, self.width, 40)
        pg.draw.rect(window, BLUE, pay_btn, 0, border_radius=30)
        pay_txt = medium_font.render("Pay", True, WHITE)
        window.blit(pay_txt, (self.x + 860, self.y + 455))
        
        view_cart = pg.Rect(self.x + 780, self.y + order_box.bottom + 115, self.width, 40)
        pg.draw.rect(window, BLUE, view_cart, 0, border_radius=30)
        txt = medium_font.render("View Cart", True, WHITE,)
        window.blit(txt, (self.x + 840, self.y + 520))

    def items_order(self):
        
        coloumn = 1
        height = 50
        width = 200
        
        for txt_box in txt_surf:
            txt_surf = pg.Surface((self.width, self.height - 550))
            txt_surf.fill(WHITE)
            txt_rect = txt_surf.get_rect(topleft=(self.x + 780, self.y + 120))
        
        # item_txt = medium_font.render("items", True, BLACK)
        # item_txt_rect = item_txt.get_rect(center=(txt_surf, txt_surf.get_height))
        # txt_surf.blit(item_txt, item_txt_rect)
        
        window.blit(txt_surf, txt_rect)
        
        
        




r_panel = RightPanel(x, y, width, height)
#===============================================================================================================
#=============================== ****EVENTS HANDLER ****========================================================  
#===============================================================================================================
def event_handler():
    
    window.fill("#545454")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            with open('user_data.json', 'w') as file:  
                json.dump([], file, indent=0)

            pg.quit()
            exit()
            
        panel.handle_event(event)
#===============================================================================================================
#=============================== **** MAIN LOOP ****============================================================
#===============================================================================================================
while True:
    dt = clock.tick(60) / 1000.0  # Frame rate control
    event_handler()
# ===============================================================================================================
    # Draw the header panel
    header.draw_header()
    # Update the sidebar behavior (width animation and drawing)
    panel.behavior()
    # Draw the left panel including the toggle button (should be after behavior)
    panel.draw_left_pnl()
    panel.side_bar()
# ===============================================================================================================
    r_panel.draw_right_pnl()
    r_panel.items_order()
    
    # Update the display
    pg.display.update()
