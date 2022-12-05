import os.path
import pygame

# 1. 모든 공을 없애면 게임 종료 (성공)
# 2. 캐릭터가 공에 닿으면 게임 종료 (실패)
# 3. 시간 제한 99초 초과 시 게임 종료 (실패)

################################################################
pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("PangPang")

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

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 1

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러번 발사 가능
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

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공의 객체 배열 (balloon1으로 초기화)
balls = []

balls.append({
    "pos_x": 50,  # 공의 x 좌표
    "pos_y": 50,  # 공의 y 좌표
    "img_idx": 0,
    "to_x": 3,
    "to_y": -6,
    "init_speed_y": ball_speed_y[0]
})

# 사라질 무기와 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 40)
total_time = 10
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

# 게임 종료 문구
# TimeOut (시간 초과로 실패)
# Mission Completed (성공)
# Game Over (캐릭터가 공에 맞은 경우, 실패)
game_result = "Game Over"

##############################################################
running = True
while running:
    dt = clock.tick(30)

    # 2. 키 입력에 따라 위치 변화율 조정
    ###############################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # 무기 발사
                weapon_pos_x = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_pos_y = character_y_pos
                weapons.append([weapon_pos_x, weapon_pos_y])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    ###############################################

    # 3. 위치 변화율에 따라 캐릭터의 위치 조정 (for문 바깥에서)
    character_x_pos += character_to_x * dt
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 발사 (위쪽으로 발사하므로 y 좌표 감소)
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # 무기가 스크린 상에 존재할 때만 그린다. (y 좌표가 0보다 작으면 사라짐.)
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공의 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]

        ball_img_idx = ball_val["img_idx"]
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로 벽에 닿았을 때 튕기는 방향 전환
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * (-1)

        # 공이 스테이지에 닿으면, 위쪽으로 튕기도록
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]  # -18 -15 -12 -9
        else:
            # -6에서 0까지: 올라가는 간격이 줄어들다가
            # 0 이상: 내려오는 간격은 점점 커진다.
            ball_val["to_y"] += 0.5

        # 공의 위치 업데이트
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리
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

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공의 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 4-1. 공과 캐릭터의 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break  # 외부 루프 탈출

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 4-2. 공과 무기들의 충돌 처리
            if ball_rect.colliderect(weapon_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # 가장 작은 공이 아니면 절반 크기로 쪼개진다.
                if ball_img_idx < 3:
                    # 현재 공의 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보 (이미지의 인덱스가 클수록 작은 공)
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
                        "pos_x": ball_pos_x + (ball_width / 2) + (small_ball_width / 2),
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

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_pos_x, weapon_pos_y in weapons:
        screen.blit(weapon, (weapon_pos_x, weapon_pos_y))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(int(total_time - elapsed_time)),
                             True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과 시 게임 종료 (실패)
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()

# 게임 종료 메시지 출력
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

# pygame 종료
pygame.quit()
