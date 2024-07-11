import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    width = 500
    
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start
        # the snake starts moving immediately upon starting the game
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        distance = self.width // self.rows
        # i = row, j = column
        i = self.pos[0]
        j = self.pos[1]

        # +1 and -2 are so that the grid is still visible when the rectangle is built
        pygame.draw.rect(surface, self.color, (i*distance + 1, j*distance + 1, distance - 2, distance - 2))

        # eyes are added to the head of the snake
        if eyes:
            centre = distance // 2
            radius = 3
            circleMiddle = (i*distance + centre - radius, j*distance + 8)
            circleMiddle2 = (i*distance + distance - radius*2, j*distance + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        

class snake(object):
    # list of cubes = snake body
    # list is in order so each square is added to the end (like a queue)
    body = []
    # holds the point on the grid at which the whole snake body needs to turn
    # the key is the current position of the snake's head
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        # head of the snake (position needs to be known in order to know where the snake currently is
        # it is one of the squares on the grid
        self.head = cube(pos)
        # put the head on the body (start of the list)
        self.body.append(self.head)
        # changes the direction of the snake
        # only one direction will be non-zero at a time so the snake does not move diagonally
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # gets a list of all the key values and whether they were pressed or not
            keys = pygame.key.get_pressed()

            # top-left corner is the origin
            # use elifs becuase the player should only be able to use one key at a time
            if keys[pygame.K_LEFT]:
                # moving left means x coordinate must be negative (to move closer to 0)
                self.dirnx = -1
                self.dirny = 0
                # set the key to be the position where the snake just turned
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                # set the key to be the position where the snake just turned
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                   
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                # set the key to be the position where the snake just turned
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                # set the key to be the position where the snake just turned
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # look through the list of positions of the snake (each index and cube)
            # decide where to move the snake

        for i, c in enumerate(self.body):
            # each cube object has a position
            # get the position of a cube object
            p = c.pos[:]
            # see if the position is in the list of turns
            if p in self.turns:
                # position where the turn will move
                turn = self.turns[p]
                # give x- and y-directions
                c.move(turn[0], turn[1])
                # if the last cube has been reached, remove the turn
                # this has to be removed because otherwise
                # any time that position is reached there would be a turn,
                # whether there is supposed to be one or not
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                ## check if the edges of the screen have been reached
                if c.dirnx == -1 and c.pos[0] <= 0:
                    # left edge means go to the right side of the screen
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    # right edge means go to the left side of the screen
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    # bottom means go to the top of the screen
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    # top means go to the bottom of the screen
                    c.pos = (c.pos[0], c.rows-1)
                # not at the edge of the screen, so the snake does not need to change position
                else:
                    c.move(c.dirnx, c.dirny)      
                        
    def reset(self, pos):
        # creating a new head
        self.head = cube(pos)
        # clear the data structures
        self.body = []
        self.turns = {}
        # add the new head to the body
        self.body.append(self.head)
        # set the directions for the snake to start travelling in
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        # last element of the list
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny

        # check the direction the tail is currently moving in
        # append a new cube object to the body of the snake
        if dx == 1 and dy == 0:
            # moving to the right, so add a cube to the left of the tail
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            # moving to the left, so add a cube to the right of the tail
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            # moving down, so add a cube at the top of the tail
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            # moving up, so add a cube at the bottom of the tail
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                # when the first snake object is drawn, it has eyes (done with True)
                # helps to recognise the head of the snake
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(width, rows, surface):
    # floor (integer) division in Python is done using //
    # drawLine cannot use decimal numbers
    # determines the gap between each line i.e. the size of each square
    sizeBetween = width // rows

    x = 0
    y = 0

    for line in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        # first vertical line is drawn, then horizontal line
        pygame.draw.line(surface, (255,255,255), (x,0), (x, width))
        pygame.draw.line(surface, (255,255,255), (0,y), (width, y))

def redrawWindow(surface):
    global width, rows, s, snack
    surface.fill((70,150,85))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    # update the display
    pygame.display.update()

# what the snake eats to make it bigger
def randomSnack(rows, item):    

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # list of filtered list
        # checks if a snack appears on the snake
        # i.e. has the same "coordinates" as any of the snake body
        # if this is the case, run the next while loop to try again
        if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x, y)
        
def endMessage(subject, content):
    # create a new tkinter window
    root = tk.Tk()
    # make this window go above anything else that is currently being displayed on the screen
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    # square grid so width = height, therefore no need for extra height variable
    width = 500
    # rows and columns for the game (grid)
    # smaller grid means harder game as less room for the snake to move
    rows = 20
    # creates a surface for the game
    win = pygame.display.set_mode((width, width))
    # create snake object
    s = snake((100,50,200), (10,10))
    snack = cube(randomSnack(rows, s), color = (120,0,0))
    flag = True
    # sets the speed of the movement of the game (in general)
    clock = pygame.time.Clock()
    while flag:
        # delays the game so that it does not run too fast
        pygame.time.delay(50)
        # the game will not run at more than 10 frames per second
        clock.tick(10)
        s.move()
        # if the snake has eaten a snack, add another cube to the end of the snake 
        if s.body[0].pos == snack.pos:
            s.addCube()
            # generates a new snack
            snack = cube(randomSnack(rows, s), color = (120,0,0))

        # looping through every cube in the snake's body
        for x in range(len(s.body)):
            # if the position of the current snake cube already exists in the body list
            # it means the snake has crashed into itself
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print("Score: " + str(len(s.body)))
                endMessage("Game over", "Play again?")
                s.reset((10,10))
                # break out of the loop because once one collision has been found,
                # it does not matter if any others have been found
                break
            
        # draw the window for the game again
        redrawWindow(win)

main()
