objects_collided = pygame.sprite.spritecollide(ball, ball.objects, True)
if objects_collided:  # 衝突ブロックがある場合
    oldrect = ball.rect
    for object in objects_collided:
        # ボールが左からブロックへ衝突した場合
        if oldrect.left < object.rect.left and oldrect.right < object.rect.right:
            ball.rect.right = object.rect.left
            ball.dx = -ball.dx

        # ボールが右からブロックへ衝突した場合
        if object.rect.left < oldrect.left and object.rect.right < oldrect.right:
            ball.rect.left = object.rect.right
            ball.dx = -ball.dx

        # ボールが上からブロックへ衝突した場合
        if oldrect.top < object.rect.top and oldrect.bottom < object.rect.bottom:
            ball.rect.bottom = object.rect.top
            ball.dy = -ball.dy

        # ボールが下からブロックへ衝突した場合
        if object.rect.top < oldrect.top and object.rect.bottom < oldrect.bottom:
            ball.rect.top = object.rect.bottom
            ball.dy = -ball.dy
