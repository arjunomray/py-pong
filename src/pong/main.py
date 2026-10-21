import pygame

# Config
BALL_SIZE = 5
PADDLE_WIDTH = BALL_SIZE * 2
PADDLE_HEIGHT = PADDLE_WIDTH * 5
SCREEN_PADDING = 20
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NET_WIDTH = 5
NET_SEGMENTS = 51
SEGMENT_SIZE = SCREEN_HEIGHT / NET_SEGMENTS

PADDLE_COLLIDE_SOUND = './assets/paddle_collide.mp3'
SCORED_SOUND = './assets/scored.mp3'
WALL_COLLIDE_SOUND = './assets/wall_collide.mp3'


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
font = pygame.Font(pygame.font.get_default_font(), 100)
dt = 0

# State
paddle_speed = 300
ball_speed_x = 400
ball_speed_y = 400
score = { 'a': 0, 'b': 0 }

paddle_a = pygame.Rect(SCREEN_PADDING, 0 ,PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(SCREEN_WIDTH - SCREEN_PADDING - PADDLE_WIDTH, 0 ,PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Vector2([SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2])

wall_collide = pygame.mixer.Sound(WALL_COLLIDE_SOUND)
scored = pygame.mixer.Sound(SCORED_SOUND)
paddle_collide = pygame.mixer.Sound(PADDLE_COLLIDE_SOUND)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    score_surface = font.render(f"{score['a']}  {score['b']}", False, "white" )
    screen.blit(score_surface, (SCREEN_WIDTH / 2 - score_surface.width / 2, SCREEN_PADDING))

    pygame.draw.rect(screen, "white", paddle_a)
    pygame.draw.rect(screen, "white", paddle_b)
    pygame.draw.circle(screen, "white", ball, BALL_SIZE )

    for i in range(NET_SEGMENTS):
        if i%2:
            continue
        net = pygame.Rect(SCREEN_WIDTH / 2 - NET_WIDTH / 2, i*SEGMENT_SIZE, NET_WIDTH, SCREEN_HEIGHT / 50)
        pygame.draw.rect(screen, "white", net)



    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.y >= 0:
        paddle_a.y -= paddle_speed * dt
    if keys[pygame.K_s] and paddle_a.y <= SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle_a.y += paddle_speed * dt
    if keys[pygame.K_UP] and paddle_b.y >= 0:
        paddle_b.y -= paddle_speed * dt
    if keys[pygame.K_DOWN] and paddle_b.y <= SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle_b.y += paddle_speed * dt

    if  (
            ball_speed_x < 0 and
            ball.x - BALL_SIZE <= paddle_a.x + PADDLE_WIDTH and
            ball.x + BALL_SIZE >= paddle_a.x and
            ball.y + BALL_SIZE >= paddle_a.y and
            ball.y - BALL_SIZE <= paddle_a.y + PADDLE_HEIGHT
        ):
        ball_speed_x = - ball_speed_x
        ball.x = paddle_a.x + PADDLE_WIDTH + BALL_SIZE
        paddle_collide.play()

    if  (
            ball_speed_x > 0 and
            ball.x + BALL_SIZE >= paddle_b.x and
            ball.x - BALL_SIZE <= paddle_b.x + PADDLE_WIDTH and
            ball.y + BALL_SIZE >= paddle_b.y and
            ball.y - BALL_SIZE <= paddle_b.y + PADDLE_HEIGHT
        ):
        ball_speed_x = - ball_speed_x
        ball.x = paddle_b.x - BALL_SIZE
        paddle_collide.play()

    if ball.x < 0:
        score["b"] += 1
        ball.x = SCREEN_WIDTH / 2
        ball.y = SCREEN_HEIGHT / 2
        ball_speed_x = - ball_speed_x
        ball_speed_y = abs(ball_speed_y)
        scored.play()

    if ball.x > SCREEN_WIDTH - BALL_SIZE:
        score["a"] += 1
        ball.x = SCREEN_WIDTH / 2
        ball.y = SCREEN_HEIGHT / 2
        ball_speed_x = - ball_speed_x
        ball_speed_y = abs(ball_speed_y)
        scored.play()

    if ball.y < 0 or ball.y > SCREEN_HEIGHT - BALL_SIZE:
        ball_speed_y = - ball_speed_y
        wall_collide.play()

    # flip() the display to put your work on screen
    ball.x += int(dt * ball_speed_x)
    ball.y += int(dt * ball_speed_y)
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
