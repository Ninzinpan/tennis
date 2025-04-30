import pygame
import sys

# 初期化
pygame.init()

# 画面設定
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# パドルの設定
paddle_width = 100
paddle_height = 20
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 40
paddle_speed = 5

# ボールの設定
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 3
ball_dy = -3

# ブロックの設定
block_width = 60
block_height = 20
block_rows = 5
block_cols = 10
blocks = []

for row in range(block_rows):
    for col in range(block_cols):
        block = pygame.Rect(col * (block_width + 5) + 50, row * (block_height + 5) + 50, block_width, block_height)
        blocks.append(block)

# ゲームループ
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # ボールの移動
    ball_x += ball_dx
    ball_y += ball_dy

    # 壁との衝突
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_dx *= -1
    if ball_y <= ball_radius:
        ball_dy *= -1

    # パドルとの衝突
    if ball_y >= paddle_y - ball_radius and paddle_x < ball_x < paddle_x + paddle_width:
        ball_dy *= -1

    # ブロックとの衝突
    for block in blocks[:]:
        if block.collidepoint(ball_x, ball_y):
            blocks.remove(block)
            ball_dy *= -1
            break

    # 画面の描画
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
    
    for block in blocks:
        pygame.draw.rect(screen, RED, block)

    pygame.display.flip()
    clock.tick(60)
