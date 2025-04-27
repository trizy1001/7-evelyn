import pygame as pg
import json
from sys import exit

pg.init()
clock = pg.time.Clock()
pg.font.init()

window = pg.display.set_mode((1024, 600), pg.RESIZABLE)
pg.display.set_caption("Evelyn")

x, y = 0, 0
width, height = 200, 600

class ui_panels:
    def __init__(self):
        # Colors
        self.color = "#000000"
        self.container_color = "#f5f5f5"
        self.button_color = "#87aee3"
        self.text_color = "#0d13c2"
        self.btn_color = "#737373"

        # mga Panels
        self.header_pnl = pg.Surface((width + 615, 60), pg.RESIZABLE)
        self.header_pnl.fill(self.color)
        self.header_pnl_rect = self.header_pnl.get_rect(topleft=(x, y))

        self.left_pnl = pg.Surface((width - 150, height), pg.RESIZABLE)
        self.left_pnl.fill(self.color)
        self.left_pnl_rect = self.left_pnl.get_rect(topleft=(x, y + 65))
        
        self.menu = pg.image.load("menu_icon.png").convert_alpha()
        self.menu = pg.transform.scale(self.menu, (100, 100))
        

        self.right_pnl = pg.Surface((width + 795, height), pg.RESIZABLE)
        self.right_pnl.fill(self.color)
        

        # dto nmn i-desiplay yubg Product 
        self.products_container = pg.Surface((width - 70, height - 500))  
        self.products_container.fill(self.container_color)

        # for Buttons nmn to
        self.order_btn = pg.image.load("buttons/cart_button.png").convert_alpha()
        
        self.pay_btn = pg.image.load("buttons/pay_btn.png").convert_alpha()
        self.pay_btn = pg.transform.scale(self.pay_btn, (190, 40))
        self.pay_rect = self.pay_btn.get_rect(topleft=(x, 460))
        
        
        self.view_cart_btn = pg.image.load("buttons/view_cart_btn.png").convert_alpha()
        self.view_cart_btn = pg.transform.scale(self.view_cart_btn, (190, 50))
        self.view_cart_btn_rect = self.view_cart_btn.get_rect(topleft=(x, 500))
        
        
        
        
        # mga Icons 
        self.settings = pg.image.load("icons/settings_icon.png").convert_alpha()
        self.user = pg.image.load("icons/user_icon.png").convert_alpha()

        # mga Fonts
        self.title_font = pg.font.SysFont("Arial", 32)
        self.pro_font = pg.font.SysFont("Arial", 50)
        self.small_font = pg.font.SysFont("Arial", 16)
        self.medium_font = pg.font.SysFont("Arial", 20)

        # sa left panel behavior
        self.trigger_exp = False
        self.animation = 50
        self.frame_motion = 0
        self.item_motion = 0
        self.select_item = None
        self.mouse_pressed = False
        self.scroll_y = 0

        # variable para sa search bar
        self.search_active = False
        self.input_rect = pg.Rect(50, 50, 300, 40)
        self.input_rect.width = 250
        self.input_rect.height = 40
        self.search_text = ""
        self.color_active = pg.Color("#87aee3")
        self.color_passive = pg.Color("#737373")
        self.s_color = self.color_passive
        self.search_bar_text = self.medium_font
        
        
        self.cart_visible = False
        self.click = False
        self.selected_category = None
        
        self.order_summ = pg.Surface((width - 20, height - 200))
        self.order_summ.fill(self.container_color)

        with open('item-data.json', 'r') as file:
            self.data_items = json.load(file)

        self.selected_category = None 
        
#=====================================================================================================================

#=====================================================================================================================
#===================== **TITLE LANG TO NG SYSTEM HAHAHHHAHAAHAAH** =======================================
    def draw_header(self):
        pg.draw.rect(window, self.color, self.header_pnl_rect, border_bottom_right_radius=20)
        self.header_pnl_rect = self.header_pnl.get_rect(topleft=(x, y))
        self.header_pnl.fill(self.color)
        
        self.title = self.title_font.render("7-EVELYN", True, "#ffffff")
        self.title_rect = self.title.get_rect(center=(x + 150, y + 30))

        self.logo = pg.image.load("new_logo.png")
        self.logo = pg.transform.scale(self.logo, (70, 65))
        self.logo_rect = self.logo.get_rect(center=(x + 35, y + 33))

        pro_text = self.pro_font.render("PRODUCTS", True, "#ffffff")
        pro_text_rect = pro_text.get_rect(center=(x + 380, y + 120))

        
        window.blit(self.title, self.title_rect)
        window.blit(self.logo, self.logo_rect)
        window.blit(pro_text, pro_text_rect)

#=====================================================================================================================
#===================== **DTO YUNG BEHAVIOR NI LEFT PANEL** ===========================================================
    def left_panel(self):
        self.left_pnl_rect = self.left_pnl.get_rect(topleft=(x, y + 65))
        mouse_pos = pg.mouse.get_pos()
        if self.left_pnl_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            if not self.trigger_exp:
                self.trigger_exp = True
        elif not self.left_pnl_rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            if self.trigger_exp:
                self.trigger_exp = False
                
        if not self.trigger_exp:
            self.frame_motion -= self.animation
            if self.frame_motion <= 0:
                self.frame_motion = 0
        
        else:
            self.frame_motion += self.animation
            if self.frame_motion >= 130:
                self.frame_motion = 130
#===================== **NILIGAY KO LANG YUNG MENU BUTTON SA LEFT PANEL TAS NILGAY KO LANG DIN YUNG MOVEMENT NI LEFT PANEL** =============                
    def menu_btn(self):
        mx, my = pg.mouse.get_pos()
        menu_rect = self.menu.get_rect(topleft=(x - 5, y + 55))
        if menu_rect.collidepoint(mx, my):
            if pg.mouse.get_pressed()[0]:
                if not self.trigger_exp:
                    self.trigger_exp = True
                    
        elif menu_rect.collidepoint(mx, my) and pg.mouse.get_pressed()[0]:
            if self.trigger_exp:
                self.trigger_exp = False
                
        if not self.trigger_exp:
            self.frame_motion -= self.animation
            if self.frame_motion <= 0:
                self.frame_motion = 0
        
        else:
            self.frame_motion += self.animation
            if self.frame_motion >= 130:
                self.frame_motion = 130

        self.left_pnl = pg.Surface((self.frame_motion + 100, height))
        pg.draw.rect(window, self.color, self.left_pnl_rect, border_top_right_radius=20)
        
        self.left_pnl.fill(self.color)
        window.blit(self.menu, menu_rect) 

#=====================================================================================================================
#=====================**DTO MAG LO-LLOAD NG MGA IMAGE FOR ITEMS**=====================================================
    def items(self, category=None):
        items_to_display = self.data_items['items']
        if category:
            items_to_display = [item for item in items_to_display if item['category'] == category]
        if self.search_text.strip():
            items_to_display = [item for item in items_to_display if self.search_text.lower() in item['name'].lower()]

        x_offset, y_offset = 230, 200
        card_width, card_height = 150, 250
        max_cards_per_row, card_spacing = 3, 30

        for index, item in enumerate(items_to_display):
            if index % max_cards_per_row == 0 and index != 0:
                x_offset = 230
                y_offset += card_height + card_spacing

            item_card = pg.Surface((card_width, card_height))
            item_card.fill(self.container_color)
            item_card_rect = item_card.get_rect(topleft=(x_offset + 50, y_offset + self.scroll_y))
            pg.draw.rect(window, self.container_color, item_card_rect, border_radius=10)
            # window.blit(item_card, (x_offset + 50, y_offset + self.scroll_y))

            try:
                item_image = pg.image.load(item["image"]).convert_alpha()
                item_image = pg.transform.scale(item_image, (card_width - 20, card_height - 85))
                img_rect = item_image.get_rect(center=(x_offset + card_width // 2 + 50, y_offset + self.scroll_y + 95))
                window.blit(item_image, img_rect)
            except FileNotFoundError:
                pass

            name_text = self.small_font.render(item['name'], True, self.text_color)
            name_rect = name_text.get_rect(center=(x_offset + card_width // 2 + 50, y_offset + self.scroll_y + 195))
            window.blit(name_text, name_rect)

            add_btn = pg.Surface((card_width - 20, 30))
            add_btn.fill(self.btn_color)
            btn_rect = add_btn.get_rect(topleft=(x_offset + 60, y_offset + self.scroll_y + card_height - 40))
            pg.draw.rect(window, self.btn_color, btn_rect, border_radius=10)
            # window.blit(add_btn, btn_rect.topleft)

            btn_text = self.medium_font.render("Add to Cart", True, self.color)
            window.blit(btn_text, (btn_rect.x + 20, btn_rect.y + 7))

            if btn_rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] and not self.mouse_pressed:
                    self.cart_item(item)
                    self.mouse_pressed = True
                elif not pg.mouse.get_pressed()[0]:
                    self.mouse_pressed = False

            x_offset += card_width + card_spacing

#=====================================================================================================================
#=====================ADD TO CART FUNCTIONS===========================================================================
    def cart_item(self, item):
        try:
            with open('user_data.json', 'r') as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []
        cart_data.append(item)
        with open('user_data.json', 'w') as file:
            json.dump(cart_data, file, indent=4)
            
    def view_cart(self):
        if not self.cart_visible:
            return
        try:
            with open('user_data.json', 'r') as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []

# =====================================================================================================================
    def left_item_category(self):
        y_offset = 150
        item_w = 60
        item_h = 60
        x = 25
        
        
        
        for item in self.data_items['categories']:
            category_box = pg.Surface((item_w, item_h))
            category_box.fill(self.container_color)
            try:
                item_image = pg.image.load(item["image"]).convert_alpha()
                item_image = pg.transform.scale(item_image, (item_w , item_h))
                category_box.blit(item_image, (0, 0))
            except FileNotFoundError:
                pass
            
            window.blit(category_box, (x, y_offset))

            text = self.medium_font.render(item['name'], True, (255, 255, 255))
            text.set_alpha(self.frame_motion)
            window.blit(text, (100, y_offset + 14))

            category_rect = category_box.get_rect(topleft=(20, y_offset))
            if category_rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
                self.selected_category = item['category']

            y_offset += 90

        self.frame_motion += self.animation
        if self.trigger_exp and self.frame_motion >= 255:
            self.frame_motion = 255

#======================================================================================================================
#=====================SEARCH BAR=======================================================================================
    def search_bar(self, event):
        self.input_rect.centerx = 650
        self.input_rect.centery = 130

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
                
#======================================================================================================================               
#=====================SAME LANG DIN TO SAYO VARIABLES LANG TALGA NAG IBA HAHHAHAHHAHA==================================
    def scroll_pad(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_y -= 50
            elif event.button == 5:  # Scroll down
                self.scroll_y += 50

        if self.scroll_y >= 0:
            self.scroll_y = 0
            
#======================================================================================================================
#=====================SO IN CONCLUSION GINAYA KO LANG YUNG SAYO, MAY MGA NA-DAGDAG LANG NA VARIABLES AND NA IBA========
    def draw(self):
        
        # window.blit(self.left_pnl, (x, y + 65))
        window.blit(self.right_pnl, (x + 824, y))

        pg.draw.rect(window, self.s_color, self.input_rect, border_radius=20)
        search_surf = self.small_font.render(self.search_text, True, (255, 255, 255))
        window.blit(search_surf, (self.input_rect.x + 10, self.input_rect.y + 10))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#======================================================================================================================
#===================== **EVENTS** ==================================================================================
panel = ui_panels()

def event_handler():
    window.fill("#545454")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            with open('user_data.json', 'w') as file:  
                json.dump([], file, indent=0)

            pg.quit()
            exit()

        panel.scroll_pad(event)
        panel.search_bar(event)
        
        
#======================================================================================================================
#===================== **MAIN LOOP** ==================================================================================
while True:
    clock.tick(60)
    event_handler() 
    panel.draw()
    panel.draw_header()
    panel.left_panel()
    panel.menu_btn()
    panel.items(panel.selected_category)
    panel.left_item_category()
    # panel.view_cart()
    
    # panel.cart_button()

    pg.display.update()
    
