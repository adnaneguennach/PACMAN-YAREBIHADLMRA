import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

while True:
    player = pygame.image.load("3.png")
    player = pygame.transform.scale(player, (40, 40))
    screen.blit(player, (10, 10))

    pygame.display.update()
