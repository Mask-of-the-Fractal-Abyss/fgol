import pygame, sys
from pygame.locals import *
import time
from random import randint
import random

pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption('CGOL2')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)

boardlength = 30
arenalength = 10
randomamount = int((arenalength * arenalength) / 10)

squarelength = 600 / boardlength
gamespeed = 200

window.fill(WHITE)
pygame.display.update()


class cellclass:
    def __init__(self, x, y, dna):
        self.x = x
        self.y = y
        self.dna = dna

    def canrep(self):
        if countneighbors(self.x, self.y) in self.dna[1]:
            return True
        return False


def grid():
    gridcolor = BLUE
    for i in range(boardlength):
        pygame.draw.rect(window, gridcolor, (i * squarelength, 0, 1, 600))
    for i in range(boardlength):
        pygame.draw.rect(window, gridcolor, (0, i * squarelength, 600, 1))


def drawcells():
    color = int(200 / 9)
    for cell in background:
        pygame.draw.rect(window, (len(cell.dna[0]) * color, (9 - len(cell.dna[1])) * color, len(cell.dna[2]) * color),
                         (squarelength * cell.x, squarelength * cell.y, squarelength, squarelength))
    showdna(DNAs[DNASELECTED])
    pygame.display.update()


def countneighbors(x, y):
    count = -1
    hood = 1
    for cell in cells:
        if cell.x in range(x - hood, x + hood + 1):
            if cell.y in range(y - hood, y + hood + 1):
                count += 1
    return count


def cellexist(x, y):
    for cell in background:
        if cell.x == x and cell.y == y:
            return True
    return False


def neighborhoods():
    output = []
    for cell in cells:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not cellexist(cell.x + x, cell.y + y):
                    output.append([cell.x + x, cell.y + y])
    return output


def neighbors(x, y):
    parentslist = []
    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            xsearch = x1 + x
            ysearch = y1 + y
            if cellexist(xsearch, ysearch):
                cell = cellat(xsearch, ysearch)
                if cell.canrep():
                    if countneighbors(x, y) + 1 in cell.dna[2] and not (cell.dna in parentslist):
                        parentslist.append(cell.dna)
    if len(parentslist) == 1:
        if not cellexist(x, y):
            background.append(cellclass(x, y, parentslist[0]))


def cellat(x, y):
    for cell in background:
        if (cell.y == y) and (cell.x == x):
            return cell


def debug():
    print("FOREGROUND:")
    for cell in cells:
        print(cell.x, cell.y)
    print("BACKGROUND:")
    for cell in background:
        print(cell.x, cell.y)
    print("-")


def keypressed(key):
    return pygame.key.get_pressed()[key]


def TEXT(text, fontsize, bold):
    myfont = pygame.font.SysFont("arial", fontsize, bold)
    return myfont.render(text, 1, BLACK, WHITE)


def showdna(input):
    dna = input
    fontsize = 10
    for i in range(len(dna)):
        bold = False
        if i == chromieselected: bold = True
        window.blit(TEXT(str(dna[i]), fontsize, bold), (10, 5 + 10 * (2.05 * i)))


def percentchance(itemslist, chancelist):
    output = []
    for item in range(len(itemslist)):
        for chance in range(chancelist[item]):
            output.append(item)
    return output


def randomgenome():
    randomDNA = [[], [], []]
    for chromies in randomDNA:
        length = randint(0, 8)
        for _ in range(length):
            num = randint(0, 8)
            if not (num in chromies):
                chromies.append(num)
    return randomDNA


def randomarena():
    global background
    global arenalength
    global DNAs
    uppercorner = int((boardlength - arenalength) / 2)
    for DNA in DNAs:
        background += [
            cellclass(randint(uppercorner, uppercorner + arenalength), randint(uppercorner, uppercorner + arenalength),
                      DNA) for _ in range(randomamount)]

def removedupes():
    global background
    background = list(set(background))

cells = []
background = []

DNAs = [randomgenome(), randomgenome(), randomgenome(), randomgenome(), randomgenome(), randomgenome(), randomgenome(),
        randomgenome(), randomgenome()]

key = None
index = 0
randomarena()
tick = 0
paused = False
DNASELECTED = 0
chromie = []
chromieselected = 3
while True:
    cells = background.copy()
    tick = (tick + 1) % 1000
    window.fill(WHITE)
    grid()
    removedupes()
    if keypressed(K_c):
        del background[:]
        cells = background.copy()
    if keypressed(K_r):
        randomarena()
        time.sleep(0.5)
    if (tick % gamespeed) == 0 and not paused:
        drawcells()
        for cell in cells:
            if countneighbors(cell.x, cell.y) not in cell.dna[0]:
                background.remove(cell)
        for empty in neighborhoods():
            x = empty[0]
            y = empty[1]
            neighbors(x, y)

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            squarex = int(mousex / squarelength)
            squarey = int(mousey / squarelength)
            if not cellexist(squarex, squarey) and not keypressed(K_e):
                background.append(cellclass(squarex, squarey, DNAs[DNASELECTED]))
                drawcells()
            elif keypressed(K_e):
                if cellexist(squarex, squarey):
                    background.remove(cellat(squarex, squarey))
                    drawcells()
            elif keypressed(K_f):
                DNASELECTED = DNAs.index(cellat(squarex, squarey).dna)
            else:
                DNASELECTED = (DNASELECTED + 1) % len(DNAs)
                background.remove(cellat(squarex, squarey))
                background.append(cellclass(squarex, squarey, DNAs[DNASELECTED]))
                drawcells()
        if event.type == KEYDOWN:
            if event.key == K_d:
                if gamespeed > 2:
                    gamespeed = int(gamespeed / 2)
            elif event.key == K_a:
                gamespeed += 50
            elif event.key == K_SPACE:
                drawcells()
                paused = not paused
            elif event.key in [K_q, K_w, K_e]:
                chromieselected = [K_q, K_w, K_e].index(event.key)
            elif event.key in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8]:
                chromie.append(int(event.unicode))
                drawcells()
            elif event.key == K_RETURN:
                if chromieselected <= 2:
                    DNAs[DNASELECTED][chromieselected] = chromie
                    chromieselected += 1
                drawcells()
                chromie = []
            elif event.key == K_BACKSPACE:
                if len(DNAs) > 1:
                    del DNAs[DNASELECTED]
                    print(len(DNAs))
                    DNASELECTED = 0
                    drawcells()
            elif event.key == K_TAB:
                DNAs.append([[], [], []])
                DNASELECTED = len(DNAs)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
