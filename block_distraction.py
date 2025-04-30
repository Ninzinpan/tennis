# -*- coding: utf-8 -*-
import math
import sys
import pygame
from pygame.locals import *
import random
import pygame.mixer

# 画面サイズ
SCREEN = Rect(0, 0, 400, 400)

# 画像ファイルのパス
PADDLE_IMG_PATH = "paddle.png"
BLOCK_IMG_PATH = "block.png"
BALL_IMG_PATH = "ball.png"
ITEM1_IMG_PATH ="apple.png"
ITEM2_IMG_PATH ="banana.png"

BACKGROUND_PATH = "background.png"

# 音声ファイルのパス
PADDLE_SOUND_PATH = "paddle_sound.mp3"
BLOCK_SOUND_PATH = "block_sound.mp3"
GAMEOVER_SOUND_PATH = "gameover_sound.mp3"
ITEM1_SOUND_PATH = "apple_sound.mp3"
ITEM2_SOUND_PATH = "banana_sound.mp3"
BACKGROUND_MUSIC_PATH = "canon.mp3"

# バドルのスプライトクラス
class Paddle(pygame.sprite.Sprite):
    # コンストラクタ（初期化メソッド）
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.width = x
        self.height = y
        #self.image = pygame.image.load(filename).convert()
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill((255, 255, 255))  # 白色で塗りつぶし
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN.bottom - 20          # パドルのy座標
        
    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]  # マウスのx座標をパドルのx座標に
        self.rect.clamp_ip(SCREEN)      
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill((255, 255, 255))  # 白色で塗りつぶし

               # ゲーム画面内のみで移動

# ボールのスプライトクラス
class Ball(pygame.sprite.Sprite):
    # コンストラクタ（初期化メソッド）
    def __init__(self, filename, paddle, blocks, score, speed, angle_left, angle_right):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.dx = self.dy = 0  # ボールの速度
        self.paddle = paddle  # パドルへの参照
        self.blocks = blocks  # ブロックグループへの参照
        self.update = self.start # ゲーム開始状態に更新
        self.score = score
        self.hit = 0  # 連続でブロックを壊した回数
        self.speed = speed # ボールの初期速度
        self.angle_left = angle_left # パドルの反射方向(左端:135度）
        self.angle_right = angle_right # パドルの反射方向(右端:45度）

    # ゲーム開始状態（マウスを左クリック時するとボール射出）
    def start(self):
        # ボールの初期位置(パドルの上)
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top

        # 左クリックでボール射出
        if pygame.mouse.get_pressed()[0] == 1:
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move

    # ボールの挙動
    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        # 壁との反射
        if self.rect.left < SCREEN.left:    # 左側
            self.rect.left = SCREEN.left
            self.dx = -self.dx              # 速度を反転
        if self.rect.right > SCREEN.right:  # 右側
            self.rect.right = SCREEN.right
            self.dx = -self.dx
        if self.rect.top < SCREEN.top:      # 上側
            self.rect.top = SCREEN.top
            self.dy = -self.dy

        # パドルとの反射(左端:135度方向, 右端:45度方向, それ以外:線形補間)
        # 2つのspriteが接触しているかどうかの判定
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            self.hit = 0                                # 連続ヒットを0に戻す
            (x1, y1) = (self.paddle.rect.left - self.rect.width, self.angle_left)
            (x2, y2) = (self.paddle.rect.right, self.angle_right)
            x = self.rect.left                          # ボールが当たった位置
            y = (float(y2-y1)/(x2-x1)) * (x - x1) + y1  # 線形補間
            angle = math.radians(y)                     # 反射角度
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)
            self.paddle_sound.play()                    # 反射音

        # ボールを落とした場合
        if self.rect.top > SCREEN.bottom:
            self.update = self.start                    # ボールを初期状態に
            self.gameover_sound.play()
            self.hit = 0
            self.score.set_score(0)                               # スコアを0点にする
            #self.score.add_score(-100)                  # スコア減点-100点

        # ボールと衝突したブロックリストを取得（Groupが格納しているSprite中から、指定したSpriteと接触しているものを探索）
        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:  # 衝突ブロックがある場合
            oldrect = self.rect
            for block in blocks_collided:
                # ボールが左からブロックへ衝突した場合
                if oldrect.left < block.rect.left and oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx
                    
                # ボールが右からブロックへ衝突した場合
                if block.rect.left < oldrect.left and block.rect.right < oldrect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx

                # ボールが上からブロックへ衝突した場合
                if oldrect.top < block.rect.top and oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy

                # ボールが下からブロックへ衝突した場合
                if block.rect.top < oldrect.top and block.rect.bottom < oldrect.bottom:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy
                self.block_sound.play()     # 効果音を鳴らす
                self.hit += 1               # 衝突回数をカウント
                self.score.add_score(self.hit * 10)   # 衝突回数に応じてスコア加点

                # アイテムを生成    
                if random.random() < 0.5:  # 20%の確率
                    item = random.choice(item_list)[0]  # item_listからランダムに1つ選択
                    new_item = Item(item.filename, item.rect.width, item.rect.height, 1, self.rect.centerx, self.rect.centery,self.paddle)
                    new_item.start = True  # アイテムを落下開始状態にする

# ブロック
class Block(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        # ブロックの左上座標
        self.rect.left = SCREEN.left + x * self.rect.width
        self.rect.top = SCREEN.top + y * self.rect.height


# アイテムのスプライトクラス
class Item(pygame.sprite.Sprite):
    def __init__(self,filename, width, height,fall_speed,x=0,y=0,paddle=None):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.paddle = paddle
        self.filename = filename
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.fall_speed = fall_speed
        self.start = False
    def draw(self, screen):
        # アイテムの画像を描画
        screen.blit(self.image, self.rect.topleft)


    def update(self,screen):

        if self.start ==True:
            self.draw(screen)
            # アイテムを落下させる
            self.rect.y += self.fall_speed
            if self.rect.top > SCREEN.bottom:  # 画面外に出たら削除
                self.kill()

            if self.rect.colliderect(self.paddle.rect):  # アイテムがパドルに衝突した場合
                # アイテムの種類に応じてパドルの幅を変更
                if self.filename == "apple.png":
                    self.item1_sound.play()
                    self.paddle.width += 10  # パドルの幅を10px増やす
                elif self.filename == "banana.png":
                    self.item2_sound.play()
                    self.paddle.width -= 10
                if self.paddle.width < 10:  # パドルの幅が10px未満になったら
                    self.paddle.width = 10
                
                self.paddle.rect = self.paddle.image.get_rect(center=(self.paddle.rect.center))
                self.kill()

                    
# スコア
class Score():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 20)
        self.score = 0
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        img = self.sysfont.render("SCORE:" + str(self.score), True, (255,255,250))
        screen.blit(img, (self.x, self.y))
    def add_score(self, x):
        self.score += x
    def set_score(self, score):
        self.score = score


item_list = []

def main():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    Ball.paddle_sound = pygame.mixer.Sound(PADDLE_SOUND_PATH)    # パドルにボールが衝突した時の効果音取得
    Ball.block_sound = pygame.mixer.Sound(BLOCK_SOUND_PATH)    # ブロックにボールが衝突した時の効果音取得
    Ball.gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND_PATH)    # ゲームオーバー時の効果音取得
    Item.item1_sound = pygame.mixer.Sound(ITEM1_SOUND_PATH) 
    Item.item2_sound = pygame.mixer.Sound(ITEM2_SOUND_PATH) # アイテム取得時の効果音取得
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)  # 背景音楽の読み込み

       # アイテム取得時の効果音取得
    # 描画用のスプライトグループ
    group = pygame.sprite.RenderUpdates()  

    # 衝突判定用のスプライトグループ
    blocks = pygame.sprite.Group()   
    items = pygame.sprite.Group()   


    # スプライトグループに追加    
    Paddle.containers = group
    Ball.containers = group
    Block.containers = group, blocks
    Item.containers = items


    # パドルの作成
    paddle = Paddle(80,15)

    # ブロックの作成(14*10)
    for x in range(1, 15):
        for y in range(1, 11):
            Block(BLOCK_IMG_PATH, x, y)

    # スコアを画面(10, 10)に表示
    score = Score(10, 10)    

   
    item_list.append([Item(ITEM1_IMG_PATH, 20, 20, 0, 0, 2)]) # アイテムの初期位置は(0,0)で、落下速度は2
    item_list.append([Item(ITEM2_IMG_PATH, 20, 20, 0, 0, 2)]) # アイテムの初期位置は(0,0)で、落下速度は2

    # ボールを作成
    Ball(BALL_IMG_PATH, paddle, blocks, score, 5, 135, 45)
    
    # アイテムを作成


    
    clock = pygame.time.Clock()

    running = True  # ループ処理の実行を継続するフラグ

    while running:
        clock.tick(60)      # フレームレート(60fps)
        screen.fill((0,20,0))


        # 背景画像の描画（画面サイズに合わせてリサイズ）
        background = pygame.image.load(BACKGROUND_PATH).convert()
        bg_width, bg_height = background.get_size()
        screen_width, screen_height = SCREEN.size[0], SCREEN.size[1]
        scale = max(screen_width / bg_width, screen_height / bg_height)
        new_width = int(bg_width * scale)
        new_height = int(bg_height * scale)
        background = pygame.transform.smoothscale(background, (new_width, new_height))
        # 背景画像を中央に配置
        bg_x = (screen_width - new_width) // 2
        bg_y = (screen_height - new_height) // 2
        screen.blit(background, (bg_x, bg_y))
        #screen.blit(background, (0, 0))

        # 背景音楽を再生（ループ再生）
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # -1は無限ループ




        # 全てのスプライトグループを更新
        group.update()
        items.update(screen)
        # 全てのスプライトグループを描画       
        group.draw(screen)

        # スコアを描画  
        score.draw(screen) 
        # 画面更新 
        pygame.display.update()

        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == QUIT: 
                running = False
            # キーイベント
            if event.type == KEYDOWN:
                # Escキーが押されたら終了
                if event.key == K_ESCAPE:   
                    running = False
    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()