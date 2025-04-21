import pygame as pg
import json
from sys import exit 

pg.init()
clock = pg.time.Clock()
pg.font.init()

window = pg.display.set_mode((1024, 600), pg.RESIZABLE)
pg.display.set_caption("Evelyn")

# Panel Position and Size
x, y = 0, 0
width, height = 200, 600

class ui_panels:
    def __init__(self):
        # Panel Colors
        self.color = "#000000"
        self.container_color = "#f5f5f5"
        self.button_color = "#87aee3"
        self.text_color = "#0d13c2"

        # Panels
        self.header_pnl = pg.Surface((width + 615, 60))
        self.header_pnl.fill(self.color)
        
        self.left_pnl = pg.Surface((width, height))
        self.left_pnl.fill(self.color)
        
        self.menu = pg.image.load("menu_icon.png")
        self.menu = pg.transform.scale(self.menu, (100, 100))
        
        self.right_pnl = pg.Surface((width + 795, height))
        self.right_pnl.fill(self.color)

        # Product container
        self.products_container = pg.Surface((width - 70, height - 500))  
        self.products_container.fill(self.container_color)

        

        # Buttons
        self.order_btn = pg.image.load("buttons/cart_button.png")
        self.pay_btn = pg.image.load("buttons/pay_btn.png")
        self.view_cart_btn = pg.image.load("buttons/button.png")
        
        # Icons 
        self.settings = pg.image.load("icons/settings_icon.png")
        self.user = pg.image.load("icons/user_icon.png")
        
        
        # Fonts
        self.title_font = pg.font.SysFont("Arial", 32)
        self.small_font = pg.font.SysFont("Arial", 16)
        self.medium_font = pg.font.SysFont("Arial", 20)

        # Other UI State
        self.trigger_exp = False
        self.animation = 20
        self.frame_motion = 0
        self.item_motion = 0
        self.select_item = None
        self.mouse_pressed = False
        self.scroll_y = 0

        # for search bar
        self.search_active = False
        self.input_rect = pg.Rect(50, 50, 300, 40)
        self.input_rect.width = 300
        self.input_rect.height = 40
        self.search_text = ""
        self.color_active = pg.Color("#87aee3")
        self.color_passive = pg.Color("#737373")
        self.s_color = self.color_passive
        self.search_bar_text = self.medium_font







        # Load item data
        with open('item-data.json', 'r') as file:
            self.data_items = json.load(file)
#=====================================================================================================================


    def draw_header(self):
        self.title = self.title_font.render("7-EVELYN", True, "#ffffff")
        self.title_rect = self.title.get_rect(center=(x + 150, y + 30))

        self.logo = pg.image.load("new_logo.png")
        self.logo = pg.transform.scale(self.logo, (70, 65))
        self.logo_rect = self.logo.get_rect(center=(x + 35, y + 33))

        window.blit(self.title, self.title_rect)
        window.blit(self.logo, self.logo_rect)
#=====================================================================================================================


    def left_panel(self):
        self.left_pnl_rect = self.left_pnl.get_rect(topleft=(x, y))
        mouse_pos = pg.mouse.get_pos()
        if self.left_pnl_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            self.trigger_exp = True
        elif not self.left_pnl_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            self.trigger_exp = False

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
        
        self.left_pnl.blit(self.menu, (x - 10, y - 20))
        
        
        
#=====================================================================================================================



    def scroll_pad(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_y -= 30
            elif event.button == 5:  # Scroll down
                self.scroll_y += 30

        # Prevent scrolling above the top
        if self.scroll_y >= 0:
            self.scroll_y = 0
#=====================================================================================================================


    
    def items(self, category=None):
        items_to_display = self.data_items['items']
        if category:
            items_to_display = [item for item in items_to_display if item['category'] == category]
            if self.search_text.strip():
                items_to_display = [item for item in items_to_display if self.search_text.lower() in item['name'].lower()]

        
        x_offset, y_offset = 200, 100
        card_width, card_height = 150, 250
        max_cards_per_row, card_spacing = 3, 30

        for index, item in enumerate(items_to_display):
            if index % max_cards_per_row == 0 and index != 0:
                x_offset = 200
                y_offset += card_height + card_spacing

            item_card = pg.Surface((card_width, card_height))
            item_card.fill(self.container_color)
            window.blit(item_card, (x_offset + 50, y_offset + self.scroll_y))
            
# ================================ Item text/Image =====================================================
            try:
                item_image = pg.image.load(item["image"]).convert_alpha()
                item_image = pg.transform.scale(item_image, (card_width - 20, card_height - 85))
                img_rect = item_image.get_rect(center=(x_offset + card_width // 2 + 50, y_offset + self.scroll_y + 95))
                window.blit(item_image, img_rect)
            except FileNotFoundError:
                pass
                # print(f"Image file not found: {item['image']}")

            name_text = self.small_font.render(item['name'], True, self.text_color)
            name_rect = name_text.get_rect(center=(x_offset + card_width // 2 + 50, y_offset + self.scroll_y + 195))
            window.blit(name_text, name_rect)

            add_btn = pg.Surface((card_width - 20, 30))
            add_btn.fill(self.color)
            btn_rect = add_btn.get_rect(topleft=(x_offset + 60, y_offset + self.scroll_y + card_height - 40))
            window.blit(add_btn, btn_rect.topleft)

            btn_text = self.medium_font.render("Add to Cart", True, self.color)
            window.blit(btn_text, (btn_rect.x + 45, btn_rect.y + 7))

            if btn_rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] and not self.mouse_pressed:
                    self.view_cart_btn(item)
                    self.mouse_pressed = True
                elif not pg.mouse.get_pressed()[0]:
                    self.mouse_pressed = False

            x_offset += card_width + card_spacing
            
#=====================================================================================================================
    def cart_item(self, item):
        try:
            with open('user_data.json', 'r') as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []
        cart_data.append(item)
        with open('user_data.json', 'w') as file:
            json.dump(cart_data, file, indent=4)
    
    def item_category(self):
        y_offset = 130
        for item in self.data_items['categories']:
            category_box = pg.Surface((50, 50))
            category_box.fill(self.container_color)
            window.blit(category_box, (25, y_offset))

            text = self.medium_font.render(item['name'], True, self.text_color)
            text.set_alpha(self.frame_motion)
            window.blit(text, (100, y_offset + 14))

            category_rect = category_box.get_rect(topleft=(25, y_offset))
            if category_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
                self.selected_category = item['category']

            y_offset += 90

        self.frame_motion += self.animation
        if self.trigger_exp and self.frame_motion >= 255:
            self.frame_motion = 255
    
    
    
    
#=====================================================================================================================


    def search_bar(self, event):
        self.input_rect.width
        self.input_rect.height 
        
        self.input_rect.centerx = 700
        self.input_rect.centery = 100
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.search_active = True
                self.s_color = self.color_active
            else:
                self.search_active = False
                self.s_color = self.color_passive

        if event.type == pg.KEYDOWN and self.search_active:
            if event.key == pg.K_BACKSPACE:
                self.search_text = self.search_text[:-1]
            elif event.key == pg.K_RETURN:
                print("Search for:", self.search_text)
            else:
                self.search_text += event.unicode

        self.search_bar_text = self.small_font.render(self.search_text, True, (255, 255, 255))
        search_surf = self.small_font.render(self.search_text, True, (255, 255, 255))
        window.blit(
            search_surf,(self.input_rect.x, self.input_rect.y + (self.input_rect.height - search_surf.get_height() // 2))
        )
                
        
    
    
#=====================================================================================================================
    
    def draw(self):
        window.blit(self.header_pnl, (x, y))
        window.blit(self.left_pnl, (x, y + 65))
        window.blit(self.right_pnl, (x + 824, y))
        
        pg.draw.rect(window, self.color, self.input_rect, border_radius=5)



panel = ui_panels()

def event_handler():
    window.fill("#545454")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            with open('data/user_data.json', 'w') as file:
                json.dump([], file, indent=0)

            pg.quit()

        panel.scroll_pad(event)
        panel.search_bar(event)


# main loop
while True:
    
    panel.draw()
    panel.draw_header()
    panel.left_panel()
    panel.items()
    panel.item_category()
    





    pg.display.update()
    clock.tick(90)
