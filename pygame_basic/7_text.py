import pygame

pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("PyGame")

# FPS
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load('./background.png')

# 캐릭터 불러오기
character = pygame.image.load('./character.png')
character_size = character.get_rect().size  # 이미지의 크기 구하기
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.6

# enemy 캐릭터
enemy = pygame.image.load('./enemy.png')
enemy_size = enemy.get_rect().size  # 이미지의 크기 구하기
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = screen_width / 2 - enemy_width / 2
enemy_y_pos = screen_height / 2 - enemy_height / 2

# 폰트 정의
game_font = pygame.font.Font(None, 40)  # 폰트 객체 생성

# 총 시간
total_time = 10

# 시작 시간
start_ticks = pygame.time.get_ticks()

# 이벤트 루프
running = True  # 게임이 진행 중인가?
while running:
    dt = clock.tick(60)  # 게임 화면의 초당 프레임 수 설정

    # 키 입력에 따라 변화율 조정
    #######################################################################
    for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
            running = False  # 게임 진행 중이 아님.

        if event.type == pygame.KEYDOWN:  # 키가 눌렸는가?
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed

        if event.type == pygame.KEYUP:  # 키에서 손을 뗐는가?
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
    #######################################################################

    # to_x, to_y 값에 따라 캐릭터의 위치 조정
    # FPS는 달라져도 캐릭터의 이동 속도는 동일하도록
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌 발생")
        running = False

    screen.blit(background, (0, 0))  # 배경 그리기
    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))  # 적 그리기

    # 타이머 집어 넣기
    # 경과 시간 측정 (s)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(str(int(total_time - elapsed_time)),
                             True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과
    if total_time - elapsed_time <= 0:
        print("타임 아웃")
        running = False

    pygame.display.update()  # 게임 화면 다시 그리기

# 잠시 대기
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
