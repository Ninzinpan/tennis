import sys  # システム関連の動作(終了処理など)を導入
import pygame  # 2Dゲーム開発のためのPygameを導入
from pygame.locals import *  # Pygame内の定数を直接使えるようにする

# パーのスプライト(描写)クラス
class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha=0):  # バーの初期位置(x, y)と大きさを調整するalpha値
        super().__init__()  # 親クラスSpriteの初期化
        pygame.sprite.Sprite.__init__(self,self.container)
        # バー描画用のSurfaceを作成。幅10、高さは50 + 50*alpha
        self.image = pygame.Surface((10, 50 + 50*alpha))
        self.image.fill((255, 255, 255))  # 白色で塗りつぶし
        self.rect = self.image.get_rect()  # バーの位置や範囲を管理するためのRect
        self.rect.topleft = (x, y)  # バーの左上座標を設定

    def update(self, dy):  # dyの値（上下方向の移動量）でバーを動かす
        self.rect.y += dy  # バーの現在位置にdyを加算して移動
        # 画面の上端より上に行きすぎないように、位置を制限する
        if self.rect.y < 10:
            self.rect.y = 10
        # 画面の下端より下に行きすぎないように、位置を制限する
        elif self.rect.y > 420:
            self.rect.y = 420

# ボールのスプライトクラス
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()  # 親クラスSpriteの初期化
        pygame.sprite.Sprite.__init__(self,self.container)

        # 半透明をサポートしたSurface(幅20 高さ20)を作り、白色の円を描いてボールを表現
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 10)
        self.rect = self.image.get_rect()  # ボールの位置や範囲を管理するRect
        self.rect.center = (x, y)  # ボールの初期位置
        self.vx = vx  # ボールの水平方向の速度
        self.vy = vy  # ボールの垂直方向の速度

    def update(self):
        # ボールをvx, vy分だけ移動
        self.rect.x += self.vx
        self.rect.y += self.vy
        # 画面上端・下端に当たったらバウンドするように、速度を反転させる
        if self.rect.y <= 10 or self.rect.y >= 457.5:
            self.vy = -self.vy

#壁のスプライトクラス
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width=20,height=100,vx=0, vy=0): #壁の初期x座標y座標,（幅、高さ、x方向への速度、y方向への速度(任意))
        super().__init__() # 親クラスSpriteの初期化
        pygame.sprite.Sprite.__init__(self,self.container)# #あとでclassをグループに追加するための処理
        

        self.image = pygame.Surface((width,height))#幅width、高さheightのSurfaceを作成
        self.image.fill((255, 255, 255))  # 白色で塗りつぶし
        self.rect = self.image.get_rect()  # 壁の位置や範囲を管理するRect
        self.rect.center = (x, y)  # 壁の初期位置
        self.vx = vx  # 壁の水平方向の速度
        self.vy = vy  # 壁の垂直方向の速度

    def update(self):
        # 壁をvx, vy分だけ移動
        self.rect.x += self.vx
        self.rect.y += self.vy
        # 画面上端・下端に当たったらバウンドするように、速度を反転させる
        if self.rect.top <= 10 or self.rect.bottom >= 457.5:
            self.vy = -self.vy

        if self.rect.left <= 5 or self.rect.right >= 620:
            self.vx = -self.vx

def main():
    pygame.init()  # Pygameで必要なモジュールや機能を初期化
    # ゲーム画面の解像度を設定(640x480)、0フラグでウィンドウ表示、32ビットカラーを指定
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption("Tennis for Two")  # ウィンドウタイトルを設定

    a_group = pygame.sprite.RenderUpdates()# 全てのスプライトを管理するグループを作成
    walls = pygame.sprite.Group()# 壁のスプライトを管理するグループを作成
    Bar.container = a_group # バーのスプライトをグループに追加
    Ball.container = a_group # ボールのスプライトをグループに追加
    Wall.container = a_group, walls # 壁のスプライトをグループに追加
    
    clock = pygame.time.Clock()  # フレームレート制御用の時計を作成
    font = pygame.font.SysFont(None, 40)  # フォント（サイズ40）を用意
    winner_text = ""


    # スコアの初期値(左側のプレイヤーがscore1、右側がscore2)
    score1, score2 = 0, 0
    setpoint = 100


    # ゲームレベルが上がるほど、ボールが早く動きバーのサイズが大きくなる
    game_level = 3

    # ボールスピード。後ろのspeed + game_levelで実際の速度が決まる
    ball_speed = 5

    # バーとボールのスプライトを作成
    bar1 = Bar(10, 215, game_level*0.2)  # 左側のバー
    bar2 = Bar(620, 215, game_level*0.2)  # 右側のバー
    # ボールは画面中央に配置(x=320, y=240)、速度は初期値で(5+1, 5+1)=6,6となる
    ball = Ball(320, 240, ball_speed + game_level, ball_speed + game_level)

    wall1 = Wall(320,100,100,20,1,0) 




    # 各バーの移動量(最初は0で動かない)
    bar1_dy = 0
    bar2_dy = 0

    running = True  # ゲームループを続けるかどうかのフラグ
    gameset = False


    while running:
        # イベント(キー入力やマウス入力など)を取得して処理

        for event in pygame.event.get():
            if event.type == QUIT:  # ウィンドウの閉じるボタンが押されたら終了
                running = False
       

            # キーが押されたとき
            if event.type == KEYDOWN:
                # 1P側：WまたはSが押されると、それぞれ上-10px、下+10px移動
                if event.key == K_w:
                    bar1_dy = -10
                elif event.key == K_s:
                    bar1_dy = 10
                # 2P側：UPまたはDOWNが押されると、それぞれ上-10px、下+10px移動
                elif event.key == K_UP:
                    bar2_dy = -10
                elif event.key == K_DOWN:
                    bar2_dy = 10

            # キーが離されたとき、動きを止める(0に戻す)
            if event.type == KEYUP:
                if event.key in (K_w, K_s):
                    bar1_dy = 0
                if event.key in (K_UP, K_DOWN):
                    bar2_dy = 0
        if score1 >= setpoint or score2 >= setpoint:
            gameset = True  # ゲームセット
            winner_text = "Player 1 Win" if score1 >= setpoint else "Player 2 Win"
        if not gameset:

            # バーとボールの位置を更新
            bar1.update(bar1_dy)
            bar2.update(bar2_dy)
            ball.update()
            walls.update()


        # バーとボールが衝突したらボールの水平方向ベクトルを反転
        if pygame.sprite.collide_rect(ball, bar1) or pygame.sprite.collide_rect(ball, bar2):
            ball.vx = -ball.vx 
      
        
        objects_collided = pygame.sprite.spritecollide(ball, walls,False)
        if objects_collided:  # 衝突ブロックがある場合

            oldrect = ball.rect
 
            for object in objects_collided:
                if oldrect.left < object.rect.left and oldrect.right < object.rect.right:
                    ball.rect.right = object.rect.left
                    ball.vx = -ball.vx

                # ボールが右からブロックへ衝突した場合
                elif object.rect.left < oldrect.left and object.rect.right < oldrect.right:
                    ball.rect.left = object.rect.right
                    ball.vx = -ball.vx

                # ボールが上からブロックへ衝突した場合
                elif oldrect.top < object.rect.top and oldrect.bottom < object.rect.bottom:
                    ball.rect.bottom = object.rect.top
                    ball.vy = -ball.vy

                # ボールが下からブロックへ衝突した場合
                elif object.rect.top < oldrect.top and object.rect.bottom < oldrect.bottom:
                    ball.rect.top = object.rect.bottom
                    ball.vy = -ball.vy
 

  
        # ボールが画面左端から出てしまったら右側プレイヤーに1点追加、ボール位置をリセット
        if ball.rect.x < 5:
            score2 += 1
            ball.rect.center = (320, 240)

        # ボールが画面右端から出てしまったら左側プレイヤーに1点追加、ボール位置をリセット
        elif ball.rect.x > 620:
            score1 += 1
            ball.rect.center = (320, 240)

        # 背景色を塗りつぶし(緑っぽい色)
        screen.fill((0, 50, 0))

        # 中央に白線を引く
        pygame.draw.aaline(screen, (255, 255, 255), (330, 5), (330, 475))

        # 全スプライト(バーとボール)を描画
        a_group.draw(screen)

        # スコアを画面に表示(スコア1は左、スコア2は右)
        screen.blit(font.render(str(score1), True, (255, 255, 255)), (250, 10))
        screen.blit(font.render(str(score2), True, (255, 255, 255)), (400, 10))
        screen.blit(font.render(winner_text, True, (255, 255, 0)), (250, 200))


        # 画面を更新して描画結果を反映
        pygame.display.update()

        # 毎フレームの処理スピード(ここでは1秒間に30回実行)を調整
        clock.tick(30)

    # ループを抜けたらPygameを終了し、Pythonのシステムも終了
    pygame.quit()
    sys.exit()

# メイン関数として実行された場合、main()を呼び出す
if __name__ == "__main__":
    main()