import pygame
import random
pygame.mixer.pre_init(44100, -16, 1, 512) #used to fix sound delay
pygame.init()
pygame.display.set_caption('Snake')
icon = pygame.image.load('images/snakeicon.png')
pygame.display.set_icon(icon)
fruit_sound = pygame.mixer.Sound("sounds/ding.wav")
gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
screen_height = 400
screen_width = 400
grid_width= 40
grid_height = 40
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0,0,0))
clock = pygame.time.Clock()
game_running = True
snake = [[0,0], [0, 1], [0,2]]
fruit = [[random.randint(0, 39), random.randint(0, 39)]] 
direction = 'Right'
score = 0
gameover = False

#draws grid
def drawgrid():
    screen.fill((0,0,0))
    grid = [[(0,0,0) for x in range(grid_width)] for y in range(grid_height)]
    for x in snake:
        grid[x[0]][x[1]] = (255,0,0)
    for x in fruit:
        grid[x[0]][x[1]] = (0,255,0)
    x_axis = 0
    y_axis = -10
    for x in grid:
        x_axis = 0
        y_axis += 10
        for y in x:
            pygame.draw.rect(screen, y, (x_axis, y_axis, 10, 10), 0)
            x_axis += 10
    pygame.display.update()
    return grid

#moves snakes
def move():
    if direction == 'Right':
        column = snake[len(snake)-1][1]+1
        if column == grid_width:
            column = 0
        snake.insert(len(snake),[snake[len(snake)-1][0], column])
        snake.remove(snake[0])
    elif direction == 'Left':
        column = snake[len(snake)-1][1]-1
        if column < 0:
            column = grid_width-1
        snake.insert(len(snake),[snake[len(snake)-1][0], column])
        snake.remove(snake[0])
    elif direction == 'Down':
        row = snake[len(snake)-1][0]+1
        if row == grid_height:
            row = 0
        snake.insert(len(snake),[row, snake[len(snake)-1][1]])
        snake.remove(snake[0])
    elif direction == 'Up':
        row = snake[len(snake)-1][0]-1
        if row < 0:
            row = grid_height-1
        snake.insert(len(snake),[row, snake[len(snake)-1][1]])
        snake.remove(snake[0])

#checks if there is fruit to eat
def eat(grid, score):
    x = snake[len(snake)-1][0]
    y = snake[len(snake)-1][1]
    if grid[x][y] == (0,255,0):
        score += 1
        pygame.mixer.Sound.play(fruit_sound)
        fruit.remove([x,y])
        fruit.append([random.randint(0, 39), random.randint(0, 39)])
        snake.insert(0, [x, y])
    return score

#checks for collisions
def collision(grid, gameover):
    x = snake[len(snake)-1][0]
    y = snake[len(snake)-1][1]
    if grid[x][y] == (255,0,0):
        gameover = True
        pygame.mixer.Sound.play(gameover_sound)
    return gameover

def gameover_screen():
    screen.fill((0,0,0))
    font1 = pygame.font.Font(pygame.font.get_default_font(), 36)
    text1 = font1.render("Score: "+str(score), True, (255,255,255))
    screen.blit(text1, (screen_height/2-text1.get_width()/2, screen_height/2-text1.get_height()/2))
    font2 = pygame.font.Font(pygame.font.get_default_font(), 16)
    text2 = font2.render("(Press Enter to Play Again)", True, (255,255,255))
    screen.blit(text2, (screen_height/2-text2.get_width()/2, (screen_height/2-text1.get_height()/2)+45)) 
    pygame.display.update()

while game_running:
    #frames per second
    clock.tick(10)
    #key strokes
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            game_running = False
    if game_running == False:
        break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        direction = 'Down'
    if keys[pygame.K_UP]:
        direction = 'Up'
    if keys[pygame.K_RIGHT]:
        direction = 'Right'
    if keys[pygame.K_LEFT]:
        direction = 'Left'
    if keys[pygame.K_RETURN] and gameover == True:
        snake = [[0,0], [0, 1], [0,2]]
        fruit = [[random.randint(0, 39), random.randint(0, 39)]] 
        direction = 'Right'
        score = 0
        gameover = False
        continue
    
    if gameover == False:
        grid = drawgrid()
        move()
        score = eat(grid, score)
        gameover = collision(grid, gameover)
    else:
        gameover_screen()
