from mazegenerator import MazeGenerator
import pygame
from typing import Tuple
maze = [[9, 5, 3, 9, 1, 1, 5, 1, 3, 9, 1, 1, 5, 5, 5, 5, 1, 5, 1, 1, 5, 5, 5, 3, 9, 5, 3, 9, 1, 3], [8, 5, 4, 2, 12, 4, 3, 8, 0, 4, 2, 8, 1, 5, 1, 1, 4, 3, 8, 4, 3, 9, 1, 4, 4, 1, 4, 4, 2, 10], [12, 1, 1, 4, 5, 3, 12, 4, 4, 5, 6, 10, 12, 1, 4, 2, 9, 2, 10, 9, 4, 6, 12, 1, 1, 4, 5, 5, 4, 6], [9, 6, 8, 5, 5, 4, 1, 3, 9, 5, 5, 0, 3, 8, 5, 4, 4, 4, 2, 12, 1, 1, 1, 0, 0, 5, 1, 1, 5, 3], [8, 5, 4, 1, 1, 1, 2, 10, 10, 9, 3, 8, 4, 2, 9, 3, 9, 5, 4, 3, 10, 8, 2, 10, 8, 5, 2, 10, 9, 2], [12, 1, 1, 2, 12, 0, 2, 10, 8, 0, 6, 8, 3, 8, 2, 12, 0, 5, 3, 12, 6, 12, 2, 12, 4, 3, 12, 6, 10, 10], [9, 2, 10, 8, 3, 8, 4, 0, 4, 2, 9, 2, 8, 2, 12, 1, 2, 9, 2, 9, 5, 1, 4, 5, 3, 8, 1, 3, 12, 2], [12, 4, 6, 8, 2, 8, 5, 4, 1, 6, 10, 10, 12, 0, 5, 6, 8, 4, 2, 8, 3, 10, 9, 1, 4, 6, 8, 4, 5, 2], [9, 1, 3, 12, 2, 12, 5, 5, 4, 1, 6, 8, 5, 2, 9, 1, 4, 3, 10, 8, 6, 12, 2, 8, 5, 5, 0, 3, 9, 2], [8, 2, 12, 3, 12, 1, 1, 1, 5, 4, 1, 4, 5, 2, 8, 4, 5, 6, 8, 6, 9, 1, 2, 12, 1, 5, 2, 12, 2, 10], [10, 8, 1, 0, 5, 2, 8, 2, 9, 5, 4, 5, 1, 2, 10, 9, 1, 5, 6, 9, 2, 8, 4, 5, 0, 3, 8, 3, 8, 2], [8, 2, 8, 4, 5, 4, 2, 12, 2, 9, 1, 5, 6, 8, 4, 4, 4, 5, 3, 10, 8, 2, 9, 3, 10, 8, 4, 2, 10, 10], [8, 2, 10, 9, 5, 1, 4, 3, 10, 10, 10, 15, 9, 4, 3, 15, 15, 15, 12, 6, 8, 4, 2, 8, 2, 8, 3, 8, 2, 10], [10, 12, 2, 10, 9, 4, 1, 4, 6, 12, 2, 15, 12, 5, 0, 5, 7, 15, 9, 3, 8, 1, 2, 8, 4, 6, 8, 2, 10, 10], [8, 3, 8, 2, 12, 1, 4, 5, 1, 3, 10, 15, 15, 15, 10, 15, 15, 15, 8, 6, 10, 10, 12, 2, 9, 1, 2, 10, 12, 2], [10, 12, 2, 12, 5, 2, 9, 5, 4, 2, 8, 1, 3, 15, 10, 15, 13, 5, 0, 1, 2, 8, 1, 4, 6, 10, 10, 10, 9, 2], [8, 1, 6, 9, 5, 4, 2, 9, 3, 10, 10, 8, 6, 15, 10, 15, 15, 15, 8, 4, 6, 10, 12, 3, 9, 2, 8, 2, 8, 2], [10, 10, 9, 4, 5, 1, 2, 10, 8, 0, 2, 8, 1, 1, 4, 1, 1, 3, 10, 9, 1, 4, 1, 2, 10, 10, 8, 6, 8, 2], [10, 8, 6, 9, 1, 4, 2, 12, 2, 12, 6, 8, 2, 8, 5, 2, 12, 4, 6, 10, 10, 9, 2, 12, 6, 8, 4, 1, 6, 10], [8, 4, 5, 6, 10, 9, 4, 5, 2, 9, 5, 6, 8, 4, 1, 2, 9, 5, 1, 4, 6, 8, 4, 5, 5, 0, 1, 6, 9, 2], [8, 5, 1, 1, 6, 8, 3, 9, 2, 10, 9, 3, 8, 5, 4, 2, 8, 1, 6, 9, 5, 0, 5, 1, 1, 2, 8, 1, 4, 2], [10, 9, 4, 4, 5, 4, 0, 6, 8, 4, 6, 10, 8, 3, 9, 6, 12, 2, 9, 4, 3, 8, 5, 2, 8, 6, 10, 8, 3, 10], [10, 10, 9, 5, 3, 9, 0, 3, 12, 1, 1, 6, 10, 10, 8, 1, 1, 4, 6, 9, 4, 6, 9, 2, 8, 5, 6, 10, 10, 10], [10, 12, 4, 3, 10, 8, 6, 8, 5, 6, 12, 5, 2, 8, 4, 2, 12, 5, 1, 4, 1, 1, 2, 8, 6, 9, 1, 2, 8, 2], [12, 5, 3, 10, 12, 4, 1, 4, 1, 1, 1, 3, 8, 4, 1, 4, 5, 1, 4, 3, 8, 2, 8, 4, 5, 6, 8, 0, 2, 10], [9, 1, 6, 8, 5, 3, 8, 5, 2, 10, 12, 2, 8, 1, 4, 1, 1, 4, 3, 10, 10, 12, 4, 3, 9, 1, 2, 12, 4, 2], [8, 2, 9, 0, 3, 8, 6, 9, 2, 10, 9, 4, 6, 8, 5, 2, 8, 5, 6, 10, 8, 1, 5, 4, 2, 12, 4, 5, 3, 10], [10, 8, 6, 10, 10, 12, 1, 0, 6, 12, 2, 9, 3, 8, 5, 6, 8, 5, 5, 4, 0, 2, 9, 3, 8, 5, 3, 9, 4, 6], [8, 4, 5, 2, 8, 3, 8, 4, 5, 1, 4, 6, 10, 8, 1, 3, 8, 3, 9, 3, 10, 8, 2, 8, 4, 5, 6, 12, 5, 3], [12, 5, 5, 4, 4, 4, 4, 5, 5, 4, 5, 5, 6, 12, 4, 4, 4, 4, 4, 4, 4, 6, 12, 4, 5, 5, 5, 5, 5, 6]]



# maze = MazeGenerator(size = (2,3), perfect = False).maze

# maze = [ 
#     [9,1,3],
#     [8,0,2],
#     [12,4,6]
# ]


def mid_maze(): 
    y = len(maze)
    x = len(maze[0])
    mid_y, mid_x = y // 2, x // 2
    # print(maze[mid_y][mid_x])
    return mid_y, mid_x

    


# print(maze[0][0])

"""
# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

"""
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
screen_width = screen.get_width()
screen_height = screen.get_height()
row = len(maze)
col = len(maze[0])

tile_size = 30

maze_width = len(maze) * tile_size
maze_height = len(maze[0]) * tile_size

offset_x = (screen_width - maze_width) // 2
offset_y = (screen_height - maze_height) // 2

player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (20,20)))

# print(player_images.index(player_images[19 // 5]))
# exit()


player_cord_x = len(maze[0]) // 2 - 1 
player_cord_y = len(maze) // 2


player_x = offset_x + player_cord_x * tile_size #  (1920 - maze_width) // 2 
player_y = offset_y + player_cord_y * tile_size


# print(int(player_cord_x), player_cord_y)
# exit()
# def check_collision(player_cord_y, player_cord_x):
#     # up = maze[player_cord_y - 1][player_cord_x]
#     # down = maze[player_cord_y + 1][player_cord_x]
#     # left = maze[player_cord_y][player_cord_x - 1]
#     # right = maze[player_cord_y][player_cord_x + 1]

#     can_move_up    = not (maze[player_cord_y][player_cord_x] & 1)
#     can_move_down  = not (maze[player_cord_y][player_cord_x] & 4)
#     can_move_left  = not (maze[player_cord_y][player_cord_x] & 8)
#     can_move_right = not (maze[player_cord_y][player_cord_x] & 2)

#     return [can_move_up, can_move_down, can_move_left, can_move_right]

def check_collision(player_cord_x, player_cord_y):
    can_move_up = not (maze[player_cord_y - 1][player_cord_x] & 1)
    can_move_down = not (maze[player_cord_y + 1][player_cord_x] & 4)
    can_move_left = not (maze[player_cord_y][player_cord_x - 1] & 8)
    can_move_right = not (maze[player_cord_y][player_cord_x + 1] & 2)

    return can_move_up, can_move_left, can_move_down, can_move_right

direction = 0
counter = 0
wp = False

def cell_to_px(x,y):  # 1920 - 900 = 1020 // 2  = 510
    offset_x = (screen.get_width() - len(maze[0]) * tile_size) // 2
    offset_y = (screen.get_height() - len(maze) * tile_size) // 2

    px = offset_x + (x * tile_size) 
    py = offset_y + (y * tile_size)
    return px, py

def px_to_cell(px, py):
    offset_x = (screen.get_width() - len(maze[0]) * tile_size) // 2
    offset_y = (screen.get_height() - len(maze) * tile_size) // 2
    x = (px - offset_x) // tile_size
    y = (py - offset_y) // tile_size
    return x, y

def draw_player():
    #right, left, up, down
    x, y = mid_maze()
    player_x, player_y = cell_to_px(x,y)

    player_x -= 25
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x , player_y))
    elif direction == 1:
            screen.blit(pygame.transform.flip(player_images[counter // 5], True, False),(player_x , player_y))
    elif direction == 2:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 90),(player_x , player_y))
    elif direction == 3:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 270),(player_x , player_y))
    return player_x, player_y


running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3

    screen.fill("black")

    if counter < 19:
        counter += 1
        if counter > 1:
            wp = False
    else:
        counter = 0
        wp = True
        
    
    for y in range(row):
       for x in range(col):
            cell = maze[y][x]
            
            px = offset_x + (x * tile_size)
            py = offset_y + (y * tile_size)

            if cell & 1: #n
                pygame.draw.rect(screen, "blue", (px, py, tile_size, 2))

            if cell & 2: #e
                pygame.draw.rect(screen, "blue", (px + tile_size - 2, py, 2, tile_size))

            if cell & 4: #s
                pygame.draw.rect(screen, "blue", (px, py + tile_size, tile_size, 2))

            if cell & 8: #w
                pygame.draw.rect(screen, "blue", (px - 2, py, 2, tile_size))

            if not cell == 15:
                if ((x,y) == (0,0) or (x,y) == (0, len(maze) - 1) or (x, y) == (len(maze) - 1, 0) or (x,y) == (len(maze) - 1, len(maze) - 1)) and not wp:
                    pygame.draw.circle(screen, "red", (px + 15, py + 15), 5)
                elif not ((x,y) == (0,0) or (x,y) == (0, len(maze) - 1) or (x, y) == (len(maze) - 1, 0) or (x,y) == (len(maze) - 1, len(maze) - 1)):
                    pygame.draw.circle(screen, "yellow", (px + 15, py + 15), 2)
                 
    player_px, player_py = draw_player()
    # print(player_x, player_y)
    # exit()
    player_x, player_y = px_to_cell(player_px, player_py)
    # print(player_x, player_y)
    # exit()
    can_move_up, can_move_left, can_move_down, can_move_right = check_collision(player_x, player_y) 
    print(can_move_up, can_move_left, can_move_down, can_move_right)

    # check_collision()

    # for x in range(ke)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

