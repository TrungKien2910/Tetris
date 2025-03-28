import pygame
from config import *
# Cài đặt kích thước cửa sổ
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Các biến dropdown
levels = [1, 2, 3, 4, 5]
selected_level = levels[0]
dropdown_open = False

# Vị trí của dropdown và nút start (cạnh nhau)
dropdown_rect = pygame.Rect(100, 100, 180, 50)
start_button_rect = pygame.Rect(300, 100, 100, 50)  # Đặt bên phải dropdown


back_button_rect = pygame.Rect(350, 20, 120, 40)


# Vị trí các cấp độ trong dropdown
options_rects = [pygame.Rect(100, 160 + i * 50, 180, 50) for i in range(len(levels))]

game_started = False

def draw_dropdown():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont('Arial', 30, bold=True)

    # Vẽ hộp chọn cấp độ
    pygame.draw.rect(screen, LIGHT_GRAY, dropdown_rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, dropdown_rect, 2, border_radius=8)
    
    text = font.render(f"Level: {selected_level}", True, BLACK)
    screen.blit(text, (dropdown_rect.x + 15, dropdown_rect.y + 10))
    
    # Vẽ danh sách cấp độ nếu dropdown mở
    if dropdown_open:
        for i, rect in enumerate(options_rects):
            color = HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else GRAY
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
            level_text = font.render(str(levels[i]), True, BLACK)
            screen.blit(level_text, (rect.x + 15, rect.y + 10))

    # Nếu đã chọn cấp độ, hiển thị nút "Start" bên phải dropdown
    color = BUTTON_HOVER if start_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, color, start_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, start_button_rect, 3, border_radius=10)
    
    start_text = font.render("Start", True, WHITE)
    screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 10))

    pygame.display.flip()

def choose_level():
    global dropdown_open, selected_level, game_started
    running = True

    while running:
        draw_dropdown()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Nhấn vào dropdown để mở danh sách
                if dropdown_rect.collidepoint(mouse_x, mouse_y):
                    dropdown_open = not dropdown_open
                
                # Nhấn vào danh sách cấp độ để chọn
                if dropdown_open:
                    for i, rect in enumerate(options_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_level = levels[i]
                            dropdown_open = False

                # Nếu nhấn vào nút "Start" sau khi chọn cấp độ
                if not dropdown_open and start_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                    running = False

        clock.tick(30)

    return selected_level