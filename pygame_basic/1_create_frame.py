import pygame

pygame.init() # 초기화

# 화면 크기 설정
screenSize = (480, 640)
screen = pygame.display.set_mode(screenSize)

# 화면 타이틀 설정
pygame.display.set_caption("PyGame")

# 이벤트 루프
running = True # 게임이 진행 중인가?
while running:
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임 진행 중이 아님.

# pygame 종료
pygame.quit()