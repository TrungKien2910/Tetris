import pygame
from tetris import Tetris
from config import *
from ui import *

pygame.init()

# Loop until the user clicks the close button.
done = False
fps = 30  # Giảm tốc độ game
level = choose_level()
game = Tetris(20, 10,level)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10,level)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Kiểm tra nếu nhấn vào nút "Back to Menu"
            if back_button_rect.collidepoint(mouse_x, mouse_y):
                level = choose_level()
                game = Tetris(20, 10, level)  # Khởi tạo lại game

    screen.fill(BACKGROUND_COLOR)

    # Vẽ lưới   
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, DARK_GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 2])
                # Thêm hiệu ứng bóng đổ
                pygame.draw.rect(screen, BLACK,
                                 [game.x + game.zoom * j + 2, game.y + game.zoom * i + 2, game.zoom - 2, game.zoom - 2], 1)

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
                    # Thêm hiệu ứng bóng đổ
                    pygame.draw.rect(screen, BLACK,
                                     [game.x + game.zoom * (j + game.figure.x) + 2,
                                      game.y + game.zoom * (i + game.figure.y) + 2,
                                      game.zoom - 2, game.zoom - 2], 1)

    # Vẽ khối hình tiếp theo bên phải màn hình
    next_fig_x = game.x + game.zoom * game.width + 50
    next_fig_y = game.y + 50
    pygame.draw.rect(screen, DARK_GRAY, [next_fig_x - 10, next_fig_y - 10, 120, 120], 3)  # Khung viền
    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in game.next_figure.image():
                pygame.draw.rect(screen, colors[game.next_figure.color],
                                 [next_fig_x + game.zoom * j + 1,
                                  next_fig_y + game.zoom * i + 1,
                                  game.zoom - 2, game.zoom - 2])
                # Thêm hiệu ứng bóng đổ
                pygame.draw.rect(screen, BLACK,
                                 [next_fig_x + game.zoom * j + 2,
                                  next_fig_y + game.zoom * i + 2,
                                  game.zoom - 2, game.zoom - 2], 1)
    

        # Vẽ nút "Back to Menu"
    font3 = pygame.font.SysFont('Arial', 20, bold=True)
    color = BUTTON_HOVER if back_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, color, back_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, back_button_rect, 2, border_radius=10)
    back_text = font3.render("Back to Menu", True, WHITE)
    screen.blit(back_text, (back_button_rect.x + 10, back_button_rect.y + 10))
    font_level = pygame.font.SysFont('Arial', 25, True, False)
    text_level = font_level.render(f"Level: {level}", True, WHITE)  
    screen.blit(text_level, (370, 60))  # Hiển thị góc trên bên phải



    font = pygame.font.SysFont('Arial', 25, True, False)
    font1 = pygame.font.SysFont('Arial', 65, True, False)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [20, 20])
    if game.state == "gameover":
        screen.blit(text_game_over, [50, 200])
        screen.blit(text_game_over1, [70, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()