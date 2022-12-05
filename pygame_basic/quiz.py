import pygame
import random

################################################################
pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Quiz")

# FPS (Frame Per Second)
clock = pygame.time.Clock()
################################################################

# 똥 피하기 게임
# 캐릭터의 위치가 하단에 고정, 좌우로만 움직일 수 있음.
# 똥은 계속 아래로 떨어지는데, 좌우 위치는 랜덤으로 결정됨.

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

# 배경 만들기
background = pygame.image.load('./background.png')

# 캐릭터 만들기
character = pygame.image.load('./character.png')
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

# 캐릭터의 좌우 위치 변경
to_x = 0
character_speed = 0.6

# 적 만들기
enemy = pygame.image.load('./enemy.png')
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0

# 똥이 떨어지는 속도
enemy_speed = 0.6

running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키 입력에 따라 좌우 이동
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        # 키에서 손을 떼면 위치가 변하지 않도록
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

        # 3. 게임 캐릭터들의 위치 정의
        # 3-1. 캐릭터의 위치
        character_x_pos += to_x * dt
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 3-2. 적의 위치
        enemy_y_pos += enemy_speed * dt
        if enemy_y_pos > screen_height:
            enemy_y_pos = 0
            enemy_x_pos = random.randint(0, screen_width - enemy_width)

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        print("충돌 발생")
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    pygame.display.update()

# pygame 종료
pygame.quit()
