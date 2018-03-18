# -----------------------------------------------------------------------------
#
# A-star Path Finding Algorithm
#
# Language - Python
# Modules - pygame, sys, random, math
#
# By - Jatin Kumar Mandav
#
# Website - https://jatinmandav.wordpress.com
#
# YouTube Channel - https://www.youtube.com/mandav
# GitHub - github.com/jatinmandav
# Twitter - @jatinmandav
#
# -----------------------------------------------------------------------------

import pygame
import sys
import math
import random

pygame.init()

width = 500
height = 500
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("A-Star Path Finding Algorithm")

display.set_alpha(None)
clock = pygame.time.Clock()

background = (179, 182, 183)
dark_gray = (23, 32, 42)
white = (236, 240, 241)
red = (203, 67, 53)
green = (35, 155, 86)
blue = (52, 152, 219)

loop = True
limit = 30

# The Map
class Spot:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.i = w
        self.j = h
        self.g = float('inf')
        self.f = float('inf')
        self.h = float('inf')
        self.neighbors = []
        self.previous = 0
        self.wall = False

    def add_neighbors(self):
        i = self.x*cols/width
        j = self.y*rows/height

        if i > 0:
            self.neighbors.append(grid[i-1][j])
        if j > 0:
            self.neighbors.append(grid[i][j-1])
        if i < cols-1:
            self.neighbors.append(grid[i+1][j])
        if j < rows-1:
            self.neighbors.append(grid[i][j+1])
        if i > 0 and j > 0:
            self.neighbors.append(grid[i-1][j-1])
        if i > 0 and j < rows-1:
            self.neighbors.append(grid[i-1][j+1])
        if i < cols-1 and j > 0:
            self.neighbors.append(grid[i+1][j-1])
        if i < cols-1 and j < rows-1:
            self.neighbors.append(grid[i+1][j+1])

    def draw(self, color):
        pygame.draw.rect(display, color, (self.x, self.y, self.i, self.j))

# Heuristic Distance
def heuristics(a, b):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

cols = 50
rows = cols

grid = [[]for _ in range(cols)]

for i in range(cols):
    for j in range(rows):
        newObj = Spot(i*(width/cols), j*(height/rows), width/cols, height/rows)
        prob = random.randrange(0, 100)
        if prob < limit:
            newObj.wall = True

        grid[i].append(newObj)


for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors()


start = grid[0][0]
end = grid[cols-1][rows-1]

start.wall = False
end.wall = False

closedSet = []
openSet = [start]
path = []

grid[0][0].g = 0
grid[0][0].h = heuristics(start, end)
grid[0][0].f = start.h


def text_objects(text, font_text, color=red):
    textsurface = font_text.render(text, True, color)
    return textsurface, textsurface.get_rect()


def button(text, x, y, w, h, action=None, font_color_active=red, font_color_inactive=red):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    font_text = pygame.font.SysFont('Stencil', 70)
    if (x < mouse_pos[0] and x + w > mouse_pos[0]) and y < mouse_pos[1] and y + h >mouse_pos[1]:
        TextSurf, TextRect = text_objects(text, font_text, font_color_active)
        TextRect.center = (x+w/2, y+h/2)
        display.blit(TextSurf, TextRect)
        if click[0] == 1 and action != None:
            action()
    else:
        TextSurf, TextRect = text_objects(text, font_text, font_color_inactive)
        TextRect.center = (x+w/2, y+h/2)
        display.blit(TextSurf, TextRect)

# Reset the Window or Create a new Map
def reset():
    global loop
    loop = False
    global grid
    grid = [[] for _ in range(cols)]

    for i in range(cols):
        for j in range(rows):
            newObj = Spot(i * (width / cols), j * (height / rows), width / cols, height / rows)
            prob = random.randrange(0, 100)
            if prob < limit:
                newObj.wall = True

            grid[i].append(newObj)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors()
    global start, end
    start = grid[0][0]
    end = grid[cols - 1][rows - 1]

    start.wall = False
    end.wall = False
    global closedSet, openSet, path
    closedSet = []
    openSet = [start]
    path = []

    grid[0][0].g = 0
    grid[0][0].h = heuristics(start, end)
    grid[0][0].f = start.h

    algorithm()

# Show if solved or unsolved
def solvedUnsolved(Text):
    global loop
    loop = True

    font = pygame.font.SysFont("Stencil", 70)
    TextSurf, TextRect = text_objects(Text, font, (249, 231, 159))
    TextRect.center = (width/2, height/2-150)
    display.blit(TextSurf, TextRect)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    reset()
        button("Reset", width/2-100, height/2+50, 200, 70,  reset, (249, 231, 159))
        pygame.display.update()
        clock.tick(60)

# Implementing the A* Algorithm
def algorithm():

    while True:
        if len(openSet) < 1:
            solvedUnsolved("No Solution!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    reset()
        display.fill(background)
        shortf = 0
        for i in range(len(openSet)):
            if openSet[shortf].f > openSet[i].f:
                shortf = i
            if openSet[shortf] == openSet[i]:
                if openSet[i].g > openSet[shortf].g:
                    shortf = i

        current = openSet[shortf]

        if current == end:
            draw(current)
            pygame.display.update()
            solvedUnsolved("Solved!")

        openSet.remove(current)
        closedSet.append(current)

        draw(current)
        neighbors = current.neighbors

        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if not (neighbor in closedSet):
                if not neighbor.wall:
                    tempg = current.g + heuristics(current, neighbor)
                    if neighbor not in openSet:
                        openSet.append(neighbor)
                    elif tempg >= neighbor.g:
                            continue

                    neighbor.g = tempg
                    neighbor.h = heuristics(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current

# Draw Everything on the Pygame Window
def draw(current):
    for i in range(cols):
        for j in range(rows):
            if grid[i][j].wall:
                pygame.draw.rect(display, dark_gray, (grid[i][j].x, grid[i][j].y, grid[i][j].i-2, grid[i][j].j-2))
            elif grid[i][j] == start:
                pygame.draw.rect(display, green, (grid[i][j].x, grid[i][j].y, grid[i][j].i, grid[i][j].j))
            elif grid[i][j] == end:
                pygame.draw.rect(display, red, (grid[i][j].x, grid[i][j].y, grid[i][j].i, grid[i][j].j))
    path = []
    while current.previous:
        path.append(current)
        current = current.previous
    path.append(start)
    for i in range(len(path)-1):
        pygame.draw.line(display, (136, 78, 160), (path[i].x + path[i].i/2, path[i].y+path[i].j/2), (path[i+1].x+path[i+1].i/2, path[i+1].y+path[i+1].j/2), path[i+1].j/2)
    pygame.display.update()

algorithm()
