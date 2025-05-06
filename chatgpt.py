import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("7-EVELYN Product UI")

font = pg.font.SysFont("Arial", 30, bold=True)
small_font = pg.font.SysFont("Arial", 24)
clock = pg.time.Clock()

# Load image
donut_img = pg.image.load("donuts/donut_1.png")  # Replace with your donut image
donut_img = pg.transform.scale(donut_img, (200, 130))

# Initial quantity
quantity = 0

# Buttons
def draw_button(rect, text, font, color=(255, 255, 255), bg=(0, 0, 0), border=3):
    pg.draw.rect(screen, bg, rect, border_radius=12)
    pg.draw.rect(screen, color, rect, border, border_radius=12)
    label = font.render(text, True, color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Main box
    box_rect = pg.Rect(250, 200, 300, 200)
    pg.draw.rect(screen, (245, 245, 245), box_rect, border_radius=20)

    # Item image
    screen.blit(donut_img, (box_rect.centerx - donut_img.get_width() // 2, box_rect.top + 10))

    # Item name and price
    name_text = font.render("donut", True, (0, 0, 200))
    price_text = font.render(f"${29}", True, (0, 0, 200))
    screen.blit(name_text, (box_rect.centerx - name_text.get_width() // 2, box_rect.top + 150))
    screen.blit(price_text, (box_rect.centerx - price_text.get_width() // 2, box_rect.top + 180))

    # Arrows
    left_arrow = draw_button(pg.Rect(260, 240, 30, 30), "◀", small_font, color=(100, 150, 255))
    right_arrow = draw_button(pg.Rect(510, 240, 30, 30), "▶", small_font, color=(100, 150, 255))

    # Plus / Minus
    minus_btn = draw_button(pg.Rect(260, 300, 40, 40), "-", font)
    plus_btn = draw_button(pg.Rect(500, 300, 40, 40), "+", font)

    # Quantity Display
    qty_text = font.render(str(quantity), True, (0, 0, 0))
    screen.blit(qty_text, (box_rect.centerx - qty_text.get_width() // 2, 305))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if minus_btn.collidepoint(event.pos):
                if quantity > 0:
                    quantity -= 1
            elif plus_btn.collidepoint(event.pos):
                quantity += 1
            elif left_arrow.collidepoint(event.pos):
                print("Go to previous item")
            elif right_arrow.collidepoint(event.pos):
                print("Go to next item")

    pg.display.flip()
    clock.tick(60)

pg.quit()
