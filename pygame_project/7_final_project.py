import os.path
import pygame

################################################################
pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Pang Game")

# FPS (Frame Per Second)
clock = pygame.time.Clock()
################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "image")  # 이미지 폴더의 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지 위에 캐릭터를 놓기 위해

# 점수판 만들기
scoreboard = pygame.image.load(os.path.join(image_path, "scoreboard.png"))
scoreboard_size = scoreboard.get_rect().size
scoreboard_height = scoreboard_size[1]  # 점수판 위에 스테이지를 놓기 위해

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - scoreboard_height - stage_height - character_height

# 캐릭터의 위치 변화량
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 1

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 생성된 무기들을 모두 저장하는 배열
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공 크기에 따른 초기 이동 속도
ball_speed_y = [-18, -15, -12, -9]

# 공 객체의 배열
balls = []

# balloon1 초기화
balls.append({
    "pos_x": 50,  # 공의 x 좌표
    "pos_y": 50,  # 공의 y 좌표
    "img_idx": 0,
    "to_x": 3,
    "to_y": -6,
    "init_speed_y": ball_speed_y[0]
})

# 사라질 무기와 공의 인덱스 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 35)

# 남은 시간 측정
total_time = 100
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

# 게임 종료 문구
# Time Over, Mission Completed, Game Over
game_result = "Game Over"

# 점수
score = 0

##############################################################
running = True
while running:  # 게임 루프 진행
    dt = clock.tick(30)  # FPS 설정

    # 2. 키 입력에 따라 위치 변화량 조절
    ###############################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_pos_x = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_pos_y = character_y_pos
                weapons.append([weapon_pos_x, weapon_pos_y])  # 무기 생성

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    ###############################################

    # 3. 요소들의 위치 정의 (for문 바깥)
    # 3-1. 캐릭터의 위치
    character_x_pos += character_to_x * dt
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 3-2. 무기의 위치
    # 키 입력에 따라 생성된 무기들을 위쪽으로 발사 (y 좌표 감소)
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    # y 좌표가 0보다 작아서 스크린을 벗어난 무기들은 배열에 추가 X
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 3-3. 공의 위치
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]

        ball_img_idx = ball_val["img_idx"]
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 좌우 벽에 닿았을 때 튕기는 방향 전환
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * (-1)

        # 공이 스테이지에 닿으면, 위쪽으로 튕기도록
        if ball_pos_y >= screen_height - scoreboard_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]  # -18 -15 -12 -9
        else:
            # -6에서 0까지: 올라가는 간격이 줄어들다가
            # 0 이상: 내려오는 간격은 점점 커진다.
            ball_val["to_y"] += 0.5

        # 공의 위치 업데이트
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    ###############################################
    # 4. 충돌 처리
    # 캐릭터의 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # for 바깥조건:
    #     바깥동작
    #     for 안쪽조건:
    #         안쪽동작
    #         if 충돌하면:
    #             break
    #     else:
    #         continue
    #     break

    # 4.1 캐릭터와 공의 충돌 (공 여러 개)
    for ball_idx, ball_val in enumerate(balls):
        # 현재 공의 위치 정보
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공의 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 캐릭터와 공이 충돌하면 게임 종료 (실패)
        if character_rect.colliderect(ball_rect):
            running = False
            break  # 외부 루프 탈출

        # 4.2 공과 무기의 충돌 (무기 여러 개)
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if ball_rect.colliderect(weapon_rect):
                # 충돌된 공과 무기는 없앤다.
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # 작은 공일수록 점수를 크게 증가시킨다.
                if ball_img_idx == 0:
                    score += 10
                elif ball_img_idx == 1:
                    score += 30
                elif ball_img_idx == 2:
                    score += 50
                else:
                    score += 100

                # 가장 작은 공이 아니면 절반 크기로 쪼개진다.
                if ball_img_idx < 3:
                    # 현재 공의 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 쪼개진 공의 크기 정보 (이미지의 인덱스가 클수록 작은 공)
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_speed_y": ball_speed_y[ball_img_idx + 1]
                    })

                    # 오른쪽으로 튕겨 나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_speed_y": ball_speed_y[ball_img_idx + 1]
                    })

                # 공과 무기가 충돌한 경우, 내부 & 외부 루프 모두 탈출
                break
        else:
            # 공과 무기가 충돌하지 않은 경우, 외부 루프에서 다음 로테이션 진행
            continue
        break  # 외부 루프 탈출

    # 충돌한 공과 무기는 배열에서 제거
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) == 0:
        game_result = "Mission Completed"
        running = False
    ###############################################

    # 5. 화면에 그리기
    # 배경 그리기
    screen.blit(background, (0, 0))

    # 무기 그리기
    for weapon_pos_x, weapon_pos_y in weapons:
        screen.blit(weapon, (weapon_pos_x, weapon_pos_y))

    # 공 그리기
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    # 점수판 그리기
    screen.blit(scoreboard, (0, screen_height - scoreboard_height))
    score_text = game_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, screen_height - scoreboard_height + 10))

    # 스테이지와 캐릭터 그리기
    screen.blit(stage, (0, screen_height - scoreboard_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 타이머 그리기
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(f'Time: {int(total_time - elapsed_time)}', True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과 시 게임 종료 (실패)
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()  # 필수

# 게임 종료 문구 그리기
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

# pygame 종료
pygame.quit()
