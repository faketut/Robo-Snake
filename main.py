import pygame, sys, time, random
from pygame.locals import *
from random import randint

redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
tailColour = pygame.Color(0,255,0)
headColour = pygame.Color(0,119,255)
# The length and width of the field where the snake moves
HEIGHT = 15
WIDTH = 15
FIELD_SIZE = HEIGHT*WIDTH
# The snake head is located in the first element of the snake array
HEAD = 0

# each grid on the matrix is processed into the length of the path to reach the food
# there needs to be a sufficiently large interval between these three variables (> HELIGHT * WIDTH)
FOOD = 0
UNDEFINED = (HEIGHT+1)*(WIDTH+1)
SNAKE = 2*UNDEFINED

# moves in 4 direction
LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH
mov = [LEFT,RIGHT,UP,DOWN]
ERR = -666

# init 
board = [0]*FIELD_SIZE
snake = [0]*(FIELD_SIZE+1)
snake[HEAD] = 1*WIDTH+1
snake_size = 1
food = 4*WIDTH+7
best_move = ERR
score = 0
# temp
tmpboard = [0]*FIELD_SIZE
tmpsnake = [0]*(FIELD_SIZE+1)
tmpsnake[HEAD] = 1*WIDTH+1
tmpsnake_size = 1

# Check if a cell is covered by the snake body. If not, it is free and returns true
def is_cell_free(idx,size,snake):
    return not(idx in snake[:size])

# Check if a certain position idx can move in the move direction
def is_move_possible(idx,move):
    flag = False
    if move == LEFT: 
        flag = True if idx%WIDTH > 1 else False
    elif move == RIGHT:
        flag = True if idx%WIDTH < (WIDTH-2) else False
    elif move == UP:
        flag = True if idx > (2*WIDTH-1) else False
    elif move == DOWN:
        flag = True if idx < (FIELD_SIZE-2*WIDTH) else False
    return flag

# reset board, after board_BFS, the UNDEFINED value becomes the length of the path to reach the food
# if it needs to be restored, it needs to be reset
def board_reset(snake,size,board):
    for i in range(FIELD_SIZE):
        if i == food:
            board[i] = FOOD
        elif is_cell_free(i,size,snake):
            board[i] = UNDEFINED
        else: 
            board[i] = SNAKE

# BFS the board, calc the length of path to food for each non-snake elts in board
def board_refresh(food,snake,board):
    queue = []
    queue.append(food)
    inqueue = [0]*FIELD_SIZE
    found = False
    # after the while loop ends, except for the snake body, the numbers in each grid represent
    # the Manhattan distance from it to the food
    while len(queue) != 0:
        idx = queue.pop(0) # the initial idx is the coordinate of the food
        if inqueue[idx] == 1: continue
        inqueue[idx] = 1
        for i in range(4): 
            if is_move_possible(idx,mov[i]):
                if idx+mov[i] == snake[HEAD]:
                    found = True 
                if board[idx+mov[i]] < SNAKE: # if this point is not snake body
                    if board[idx+mov[i]] > board[idx]+1: # only deal with the bigger case, otherwise overlap existed path data
                        board[idx+mov[i]] = board[idx]+1
                    if inqueue[idx+mov[i]] == 0:
                        queue.append(idx+mov[i])
    return found

# start from the snake head, based on the elt values in the board, choose the shortest path from the
# four neigbour points around the snake head
def choose_shortest_safe_move(snake,board):
    best_move = ERR
    min = SNAKE
    for i in range(4):
        if is_move_possible(snake[HEAD],mov[i]) and board[snake[HEAD]+mov[i]] < min:
            
            min = board[snake[HEAD]+mov[i]]
            best_move = mov[i]
    return best_move
# choose the longest path from the four neigbour points around the snake head
def choose_longest_safe_move(snake,board):
    best_move = ERR
    max = -1
    for i in range(4):
        if is_move_possible(snake[HEAD],mov[i]) and board[snake[HEAD]+mov[i]] > max and board[snake[HEAD]+mov[i]] < UNDEFINED:
            max = board[snake[HEAD]+mov[i]]
            best_move = mov[i]
    return best_move

# check if it's possible to follow the snake's tail, that is, there is a path between the snake head and
# its tail. To avoid the snake head getting stuck in a dead end, do operation virtually in tmpboard with tmpsnake
def is_tail_inside():
    global tmpboard,tmpsnake,food,tmpsnake_size
    tmpboard[tmpsnake[tmpsnake_size-1]] = 0 # virtually set snake tail as food
    tmpboard[food] = SNAKE # set where the food located as snake body
    result = board_refresh(tmpsnake[tmpsnake_size-1],tmpsnake,tmpboard) 
    for i in range(4):
        # if snake head and snake tail are next to each other, then return False. 
        if is_move_possible(tmpsnake[HEAD],mov[i]) and tmpsnake[HEAD]+mov[i] == tmpsnake[tmpsnake_size-1] and tmpsnake_size > 3:
            result = False
    return result

# let snake head run one step towards snake tail. regardless of snake body, run in the direction of snake tail
def follow_tail():
    global tmpboard,tmpsnake,food,tmpsnake_size
    tmpsnake_size = snake_size
    tmpsnake = snake[:]
    board_reset(tmpsnake,tmpsnake_size,tmpboard)
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD # set snake tail as food
    tmpboard[food] = SNAKE # set where the food is into snake body
    board_refresh(tmpsnake[tmpsnake_size-1],tmpsnake,tmpboard)
    tmpboard[tmpsnake[tmpsnake_size-1]] = SNAKE # restore snake tail
    return choose_longest_safe_move(tmpsnake,tmpboard)

# when all kinds of solutions fail, find a feasible direction to go (1 step)
def any_possible_move():
    global food,snake,snake_size,board
    best_move = ERR
    board_reset(snake,snake_size,board)
    board_refresh(food,snake,board)
    min = SNAKE
    for i in range(4):
        if is_move_possible(snake[HEAD],mov[i]) and board[snake[HEAD]+mov[i]] < min:
            min = board[snake[HEAD]+mov[i]]
            best_move = mov[i]
    return best_move

def shift_array(arr,size):
    for i in range(size,0,-1):
        arr[i] = arr[i-1]

def new_food():
    global food,snake_size
    cell_free = False
    while not cell_free:
        w = randint(1,WIDTH-2)
        h = randint(1,HEIGHT-2)
        food = WIDTH*h+w
        cell_free = is_cell_free(food,snake_size,snake)
    pygame.draw.rect(playSurface,redColour,Rect(18*(food//WIDTH),18*(food%WIDTH),18,18))

def make_move(best_move):
    global snake,board,snake_size,score
    shift_array(snake,snake_size)
    snake[HEAD] += best_move
    p = snake[HEAD]
    for body in snake: 
        pygame.draw.rect(playSurface,whiteColour,Rect(18*(body//WIDTH),18*(body%WIDTH),18,18))
    pygame.draw.rect(playSurface,tailColour,Rect(18*(snake[snake_size-1]//WIDTH),18*(snake[snake_size-1]%WIDTH),18,18))
    pygame.draw.rect(playSurface,headColour,Rect(18*(p//WIDTH), 18*(p%WIDTH),18,18))
    # cope with the first white block in the initial situation
    pygame.draw.rect(playSurface,(255,255,0),Rect(0,0,18,18))
    pygame.display.flip()

    if snake[HEAD] == food:
        board[snake[HEAD]] = SNAKE 
        snake_size += 1
        score += 1
        if snake_size < FIELD_SIZE: new_food()
    else: 
        board[snake[HEAD]] = SNAKE
        board[snake[snake_size]] = UNDEFINED 
        pygame.draw.rect(playSurface,blackColour,Rect(18*(snake[snake_size]//WIDTH),18*(snake[snake_size]%WIDTH),18,18))
        pygame.display.flip()

# check it it's feasible at the call before it actually works. After eating the food in the virtual run, 
# get the position of the virtual snake on the board        
def virtual_shortest_move():
    global snake,board,snake_size,tmpsnake,tmpboard,tmpsnake_size,food
    tmpsnake_size = snake_size
    tmpsnake = snake[:] # if tempsnake = snake directly, then both point to the same memory
    tmpoard = board[:]
    board_reset(tmpsnake,tmpsnake_size,tmpboard)
    food_eated = False
    while not food_eated:
        board_refresh(food,tmpsnake,tmpboard)
        move = choose_shortest_safe_move(tmpsnake,tmpboard)
        shift_array(tmpsnake,tmpsnake_size)
        tmpsnake[HEAD] += move

        if tmpsnake[HEAD] == food:
            tmpsnake_size += 1
            board_reset(tmpsnake,tmpsnake_size,tmpboard)
            tmpboard[food] = SNAKE
            food_eated = True
        else: 
            tmpboard[tmpsnake[HEAD]] = SNAKE
            tmpboard[tmpsnake[tmpsnake_size]] = UNDEFINED

# if there is a path between the snake and the food, this function is called
def find_safe_ways():
    global snake,board
    safe_move = ERR
    virtual_shortest_move()
    if is_tail_inside():
        return choose_shortest_safe_move(snake,board)
    safe_move = follow_tail()
    return safe_move

# init pygame
pygame.init()
fpsClock = pygame.time.Clock()
playSurface = pygame.display.set_mode((270,270))
pygame.display.set_caption('Robo-snake')
playSurface.fill(blackColour)
pygame.draw.rect(playSurface,redColour,Rect(18*(food//WIDTH),18*(food%WIDTH),18,18))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            print(score)
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print(score)
                pygame.quit()
                sys.exit()
    pygame.display.flip()
    pygame.draw.rect(playSurface,(255,255,0),Rect(0,0,270,270),18)
    board_reset(snake,snake_size,board)
    if board_refresh(food,snake,board):
        best_move = find_safe_ways() 
    else: 
        best_move = follow_tail()
    if best_move == ERR:
        best_move = any_possible_move()
    
    if best_move != ERR: make_move(best_move)
    else: 
        print(score)
        break
    fpsClock.tick(50)

        


            

            

