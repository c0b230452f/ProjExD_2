import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
        pg.K_UP:(0, -5),
        pg.K_DOWN:(0, 5),
        pg.K_LEFT:(-5, 0),
        pg.K_RIGHT:(5,0),
        }  # pythonは最後の要素にカンマがあってもエラーにはならない
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん または 爆弾のRect
    戻り値：真理値タプル（横判定結果, 縦判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    w, h = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        w = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        h = False
    return (w, h)

def sleep(n:int):
    """
    引数：表示させたい時間
    戻り値：なし
    こうかとんと爆弾の衝突時、5秒間プログラムを停止させる
    """
    pg.time.wait(n*1000)

def change_tuple(lst:list) -> tuple:
    """
    引数：加速度や拡大爆弾Surfaceのリスト
    戻り値：引数のリストをタプルに変換したもの
    リストをタプルに変換する
    """
    return tuple(lst)

def facing(lst:list) -> dict:
    """
    引数：移動量リスト
    戻り値：kk_imgのSurface
    移動量に応じて向きの違うこうかとんSurfaceを返す
    """
    face_dct = {
        (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (5,-5):pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9),
        (0,-5):pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 0.9),
        (-5,-5):pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9),
        (-5,0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (-5,5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
        (0, 5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9),
        (5, 5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
    }
    return face_dct[tuple(lst)]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # ----- 背景 -----
    bg_img = pg.image.load("fig/pg_bg.jpg")
    # ----- こうかとん -----
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # ----- ブラックアウト -----
    bo_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bo_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bo_img.set_alpha(200)
    # ----- メッセージ -----
    msg = pg.font.Font(None, 80)
    txt = msg.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH//2, HEIGHT//2
    # ----- こうかとん -----
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk2_rct = kk2_img.get_rect()
    kk2_rct.center = WIDTH//3, HEIGHT//2
    kk3_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk3_rct = kk3_img.get_rect()
    kk3_rct.center = (WIDTH//3)*2, HEIGHT//2
    # ----- 爆弾 -----
    bb_img = pg.Surface((20, 20))  # 空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0))  # 爆弾の余白を透過
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.center = random.randint(0, WIDTH),\
                    random.randint(0, HEIGHT)  # 爆弾の初期座標を乱数で設定
    vx, vy = +5, +5 
    # accs= [a for a in range(1, 11)]  # 加速度のリスト
    # imgs = []
    # for r in range(1, 11):
    #     bb_img = pg.Surface((20*r, 20*r))
    #     pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    #     bb_img.set_colorkey((0,0,0))  # 爆弾の余白を透過
    #     bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    #     bb_rct.center = random.randint(0, WIDTH),\
    #                     random.randint(0, HEIGHT)
    #                     # 爆弾の初期座標を乱数で設定
    #     imgs.append(bb_img)
    # bb_accs = change_tuple(accs)
    # bb_imgs = change_tuple(imgs)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        # ----- 衝突判定 -----
        if kk_rct.colliderect(bb_rct):
            # こうかとんと爆弾が重なっていたら終了
            screen.blit(bo_img, [0,0])  # ブラックアウトさせる
            screen.blit(kk2_img, kk2_rct)
            screen.blit(txt, txt_rct)
            screen.blit(kk3_img, kk3_rct)
            pg.display.flip()
            sleep(5)
            return
        # ----- こうかとんの移動 -----
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 横方向, 縦方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        # こうかとんの向きを変える
        kk_img = facing(sum_mv)
        if sum_mv[0] == 5:  # 右側を向いていたら左右反転させる
            kk_img = pg.transform.flip(kk_img, True, False)
        # こうかとんが画面外へ行かないようにする
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            # 直前のmove_ipを打ち消す
        screen.blit(kk_img, kk_rct)
        # ----- 爆弾の移動 -----
        # avx = vx*bb_accs[min(tmr//500, 9)]
        # avy = vy*bb_accs[min(tmr//500, 9)]
        # bb_img = bb_imgs[min(tmr//500, 9)]
        # bb_rct.move_ip(avx, avy)
        bb_rct.move_ip(vx, vy)

        # 爆弾を画面の端でバウンドさせる
        (w, h) = check_bound(bb_rct)
        if not w:
            vx *= -1
        if not h:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
