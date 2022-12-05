import pygame
import sys

screenSize = (400, 300)
gameScreen = pygame.display.set_mode(screenSize)
pygame.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            print(event)

pygame.quit()
sys.exit()
