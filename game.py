import pygame
import sys
import random

# Pygameの初期化
pygame.init()

# 画面サイズ
screen_width = 600
screen_height = 400

# ゲーム画面の作成
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avoidance Sphere")

# フォントの指定
font = pygame.font.Font(pygame.font.match_font('arialunicodems'), 36)


def reset_game():
    global obstacle_height, obstacle_width
    ball_radius = 20
    ball_x = screen_width // 2
    ball_y = screen_height - 2 * ball_radius
    obstacle_width = 30
    obstacle_height = 50
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = -obstacle_height
    obstacle_speed = 20
    score = 0
    ball_speed = 15
    return ball_x, ball_y, ball_radius, obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed, ball_speed, score

# ボールの初期位置と速度
ball_x, ball_y, ball_radius, obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed, ball_speed, score = reset_game()

# スコア
score = 0

# ゲームが終了したかどうかを示すフラグ
game_over = False

# ゲームが開始されたかどうかを示すフラグ
game_started = False

# タイトル画面のテキスト
title_text = font.render("Avoidance Sphere", True, (0, 0, 0))
title_text_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

start_text = font.render("Press SPACE to Start", True, (0, 0, 0))
start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))

# ゲームループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # スペースキーが押されたらゲームを開始
            game_started = True

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            # マウスがクリックされたらゲームを開始
            game_started = True

    if game_started:
        if game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # ゲームオーバー時にスペースキーが押されたらゲームをリセット
                ball_x, ball_y, ball_radius, obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed, ball_speed, score = reset_game()
                game_over = False

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and ball_x - ball_radius > 0:
                ball_x -= ball_speed
            if keys[pygame.K_RIGHT] and ball_x + ball_radius < screen_width:
                ball_x += ball_speed

            obstacle_y += obstacle_speed

            if obstacle_y > screen_height:
                obstacle_x = random.randint(0, screen_width - obstacle_width)
                obstacle_y = -obstacle_height
                score += 1

            if (
                ball_x + ball_radius > obstacle_x
                and ball_x - ball_radius < obstacle_x + obstacle_width
                and ball_y + ball_radius > obstacle_y
                and ball_y - ball_radius < obstacle_y + obstacle_height
            ):
                game_over = True

            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            pygame.draw.circle(screen, (0, 0, 255), (int(ball_x), int(ball_y)), ball_radius)
            score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to replay.", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2 - 18))

    else:
        # タイトル画面の描画
        screen.fill((255, 255, 255))
        screen.blit(title_text, title_text_rect)
        screen.blit(start_text, start_text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
