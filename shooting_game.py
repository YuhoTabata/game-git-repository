import pygame
import sys
import random
import math

# 初期化
pygame.init()

# 画面設定
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("宇宙船シューティングゲーム")

# サウンドの初期化
pygame.mixer.init()
explosion_sound = pygame.mixer.Sound('c9aly-8hbqc.wav')

# 色の定義
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 宇宙船の設定
ship_width = 50
ship_height = 50
ship_x = width // 2 - ship_width // 2
ship_y = height - 2 * ship_height
ship_speed = 30

# 弾の設定
bullet_width = 5
bullet_height = 15
bullet_speed = 50
bullets = []

# 敵の設定
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# スコアの初期化
score = 0
font = pygame.font.Font(None, 36)

def draw_star(surface, color, x, y, size):
    outer_radius = size
    inner_radius = size // 2
    num_points = 5

    star_points = []
    for i in range(2 * num_points):
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle = i * math.pi / num_points
        star_x = x + radius * math.cos(angle)
        star_y = y + radius * math.sin(angle)
        star_points.append((star_x, star_y))

    pygame.draw.polygon(surface, color, star_points)

# タイトル画面の設定
title_font = pygame.font.Font(None, 60)
start_font = pygame.font.Font(None, 36)

title_text = title_font.render("Spacecraft Shooting Game", True, red)
title_rect = title_text.get_rect(center=(width // 2, height // 2))

start_instructions = start_font.render("Press SPACE or ENTER to start", True, white)
instructions_rect = start_instructions.get_rect(center=(width // 2, height // 2 + 100))

# ゲームステート
game_active = False

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # スペースキーかエンターキーが押されたときにゲームを開始
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                game_active = True

    # タイトル画面
    if not game_active:
        screen.fill(black)
        screen.blit(title_text, title_rect)
        screen.blit(start_instructions, instructions_rect)
        pygame.display.flip()
        continue

    if game_active:
        # ゲーム中の処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 宇宙船の移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < width - ship_width:
            ship_x += ship_speed

        # 弾の発射
        if keys[pygame.K_SPACE]:
            bullet_x = ship_x + ship_width // 2 - bullet_width // 2
            bullet_y = ship_y
            bullets.append([bullet_x, bullet_y])

        # 弾の移動
        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        # 敵の生成
        if random.randint(0, 100) < 10:
            enemy_x = random.randint(0, width - enemy_width)
            enemy_y = 0
            # ランダムな色を生成
            enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # ランダムな形を生成
            enemy_shape = random.choice(["rectangle", "circle", "ellipse", "star"])

            enemies.append([enemy_x, enemy_y, enemy_color, enemy_shape])


        # 敵の移動
        enemies_to_remove = []  # 一時的なリスト
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > height:
                enemies_to_remove.append(enemy)  # 一時的なリストに追加
                score += 1

        # 一時的なリストに含まれる敵をenemiesリストから削除
        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        # 衝突判定
        for enemy in enemies:
            for bullet in bullets:
                if (
                    bullet[0] < enemy[0] + enemy_width
                    and bullet[0] + bullet_width > enemy[0]
                    and bullet[1] < enemy[1] + enemy_height
                    and bullet[1] + bullet_height > enemy[1]
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    explosion_sound.play()  # 敵に当たった時に音を再生

    # 画面のクリア
    screen.fill(black)

    # 宇宙船の描画
    pygame.draw.rect(screen, white, [ship_x, ship_y, ship_width, ship_height])

    # 弾の描画
    for bullet in bullets:
        pygame.draw.rect(screen, red, [bullet[0], bullet[1], bullet_width, bullet_height])

    # 敵の描画
    for enemy in enemies:
        enemy_x, enemy_y, enemy_color, enemy_shape = enemy
        if enemy_shape == "rectangle":
            pygame.draw.rect(screen, enemy_color, [enemy_x, enemy_y, enemy_width, enemy_height])
        elif enemy_shape == "circle":
            pygame.draw.circle(screen, enemy_color, (enemy_x + enemy_width // 2, enemy_y + enemy_height // 2), enemy_width // 2)
        elif enemy_shape == "ellipse":
            pygame.draw.ellipse(screen, enemy_color, [enemy_x, enemy_y, enemy_width, 2 * enemy_height])
        elif enemy_shape == "star":
            draw_star(screen, enemy_color, enemy_x, enemy_y, enemy_width)

    # スコア表示
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, [10, 10])

    # 画面の更新
    pygame.display.flip()

    # フレームレートの制御
    pygame.time.Clock().tick(30)
