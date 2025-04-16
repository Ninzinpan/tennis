import sys  
import pygame  
from pygame.locals import *  

class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha=0):  
        super().__init__()  
        pygame.sprite.Sprite.__init__(self,self.container)

        self.image = pygame.Surface((10, 50 + 50*alpha))
        self.image.fill((255, 255, 255))  
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)  

    def update(self, dy): 
        self.rect.y += dy  
        if self.rect.y < 10:
            self.rect.y = 10

        elif self.rect.y > 420:
            self.rect.y = 420

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()  
        pygame.sprite.Sprite.__init__(self,self.container)

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 10)
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y)  
        self.vx = vx  
        self.vy = vy  
    def update(self):

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.y <= 10 or self.rect.y >= 457.5:
            self.vy = -self.vy


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10,height=100,vx=0, vy=0):
        super().__init__() 
        pygame.sprite.Sprite.__init__(self,self.container)
        

        self.image = pygame.Surface((width,height))
        self.image.fill((255, 255, 255))  # 白色で塗りつぶし
        self.rect = self.image.get_rect()  # ボールの位置や範囲を管理するRect
        self.rect.center = (x, y)  # ボールの初期位置
        self.vx = vx  # ボールの水平方向の速度
        self.vy = vy  # ボールの垂直方向の速度
    def update(self):
        # ボールをvx, vy分だけ移動
        self.rect.x += self.vx
        self.rect.y += self.vy
        # 画面上端・下端に当たったらバウンドするように、速度を反転させる
        if self.rect.top <= 10 or self.rect.bottom >= 457.5:
            self.vy = -self.vy

        if self.rect.left <= 5 or self.rect.right >= 620:
            self.vx = -self.vx


def main():
    pygame.init()  
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption("Tennis for Two")  


    a_group = pygame.sprite.RenderUpdates()
    walls = pygame.sprite.Group()
    Bar.container = a_group
    Ball.container = a_group
    Wall.container = a_group, walls
    
    clock = pygame.time.Clock()  
    font = pygame.font.SysFont(None, 40)  
    winner_text = ""


##################################################################

    #久保田:ここから下をメインにいじってもらうイメージです

    #勝利のために必要なポイント
    setpoint = 5

    # スコアの初期値(左側のプレイヤーがscore1、右側がscore2)
    score1, score2 = 0, 0
    
    # ゲームレベルが上がるほど、ボールが早く動きバーのサイズが大きくなる
    game_level = 1

    # ボールスピード。後ろのspeed + game_levelで実際の速度が決まる
    ball_speed = 5

    # バーとボールのスプライトを作成
    bar1 = Bar(10, 215)  # 左側のバー
    bar2 = Bar(620, 215, game_level*0.2)  # 右側のバー
    # ボールは画面中央に配置(x=320, y=240)、速度は初期値で(5+1, 5+1)=6,6となる
    ball = Ball(320, 240, ball_speed + game_level, ball_speed + game_level)
    
    #wallスプライトを作成します。引数は、順番にWall(x座標,y座標,幅,高さ,x方向への速度,y方向への速度)です。座標以外初期値があるので設定しなくても動きます。
 
    #wall1 = Wall(500,100,100,50,1,1)
    
    wall1 = Wall(100,300,500,20,1,2)

    wall2 = Wall(300,100,20,500,2,1)

    
    #wall2 = Wall(320,100,20,100,0,0)
    #wall2 = Wall(20,100,20,50,1,0)









    # スプライトグループを作成し、バー2本とボールを登録
    #all_sprites = pygame.sprite.Group()
    #all_sprites.add(bar1, bar2, ball)

    # 各バーの移動量(最初は0で動かない)
    bar1_dy = 0
    running = True  # ゲームループを続けるかどうかのフラグ
    gameset = False
    while running:
        # イベント(キー入力やマウス入力など)を取得して処理
        for event in pygame.event.get():
            if event.type == QUIT:  # ウィンドウの閉じるボタンが押されたら終了
                running = False

            # キーが押されたとき
            if event.type == KEYDOWN:

                # プレイヤー側：UPまたはDOWNが押されると、それぞれ上-10px、下+10px移動
                if event.key == K_UP:
                    bar1_dy = -10
                elif event.key == K_DOWN:
                    bar1_dy = 10

            # キーが離されたとき、動きを止める(0に戻す)
            if event.type == KEYUP:

                if event.key in (K_UP, K_DOWN):
                    bar1_dy = 0

        # バーとボールの位置を更新
                # スコア勝敗判定
        if score1 >= setpoint or score2 >= setpoint:
            gameset = True  # ゲームセット
            winner_text = "Player 1 Win" if score1 >= setpoint else "Player 2 Win"

        if not gameset:
            # バーとボールの位置を更新（ゲームセット後は更新しない）
            bar1.update(bar1_dy)
            bar2.update((ball.rect.y - bar2.rect.y) * 0.1 * game_level)
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