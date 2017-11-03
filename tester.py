import numpy as np
import cv2
import pickle
import pyautogui as pg

grid = np.full((10, 10), 9, dtype=np.int)
# -1 = not open
# 0 = open
# 1 = 1
# 2 = 2
# 3 = 3
# 4 = 4
# 9 = unknown
# 11 = flag
# 22 = mine
# 99 = game over

cost = np.full((8, 8), 0, dtype=np.int)
# 0 = 0. Not opened, not surrounded by any numbers.
# 1 = 1 cost
# 2 = 2 cost
# 3 = 3 cost
# 4 = 4 cost
# 5 = 5 cost
# 6 = 6 cost
# 7 = 7 cost
# 8 = 8 cost
# 9 = flag/open

midLayer = np.full((10, 10), 0, dtype=np.int)
# 10x10 because cost update takes 3x3 neighbourhood into account, thus for edges we have to add padding
# 0 = not opened, opened, flag
# 1 = 1, 2, 3, 4

queue = []

f = open('model.txt', 'rb')
s = f.read()
classifier = pickle.loads(s)

snap = cv2.imread("mines_1.png")


def updateSnap():
    # updates the screen shot after a move has been made

    global snap
    snap = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)


def updateGrid():
    # updates the grid matrix, a digital representation of the 8x8 minesweeper grid

    global grid, queue
    for i in range(1, 9, 1):
        startX = 76 + ((i - 1) * 86)
        for j in range(1, 9, 1):
            startY = 366 + ((j - 1) * 86)
            if grid[i][j] == 9:
                part = snap[startX:startX + 86, startY:startY + 86, :]
                prediction = classifier.predict(part.ravel())[0]
                if prediction == '1':
                    grid[i][j] = 1
                    queue.append((i, j))
                elif prediction == '2':
                    grid[i][j] = 2
                    queue.append((i, j))
                elif prediction == '3':
                    grid[i][j] = 3
                    queue.append((i, j))
                elif prediction == '4':
                    grid[i][j] = 4
                    queue.append((i, j))
                elif prediction == 'open':
                    grid[i][j] = 0
                elif prediction == 'notopen':
                    grid[i][j] = -1
                elif prediction == 'flag':
                    grid[i][j] = 11
                elif prediction == 'mine':
                    grid[i][j] = 22
                elif prediction == 'dead':
                    # end game
                    grid[i][j] = 99
                    print grid
                    print '\n\n ----------------- GAME OVER -----------------\n\n'
                    exit(1)
                else:
                    print prediction
                cv2.imshow("window", part)
                cv2.waitKey(1)


def updateMidLayer():
    # updates the midLayer matrix which makes the calculation of cost matrix easier and faster

    global midLayer, grid
    updateGrid()
    for i in range(1, 9):
        for j in range(1, 9):
            if grid[i][j] == -1 or grid[i][j] == 11 or grid[i][j] == 0:
                midLayer[i][j] = 0
            else:
                midLayer[i][j] = 1


def updateCost():
    # updates the cost matrix, based on which a decision will be taken

    global cost
    updateMidLayer()
    for i in range(0, 8):
        for j in range(0, 8):
            if grid[i][j] == -1:
                cost[i][j] = midLayer[i][j] \
                             + midLayer[i][j + 1] \
                             + midLayer[i][j + 2] \
                             + midLayer[i + 1][j + 2] \
                             + midLayer[i + 2][j + 2] \
                             + midLayer[i + 2][j + 1] \
                             + midLayer[i + 2][j] \
                             + midLayer[i + 1][j]
            else:
                cost[i][j] = 9


def nextMove():
    global queue, grid

    for i, j in queue:
        notOpenCount = 0
        flagCount = 0
        neighbours = [(i - 1, j - 1, grid[i - 1][j - 1], 0), (i - 1, j, grid[i - 1][j], 0),
                      (i - 1, j + 1, grid[i - 1][j + 1], 0), (i, j + 1, grid[i][j + 1], 0),
                      (i + 1, j + 1, grid[i + 1][j + 1], 0), (i + 1, j, grid[i + 1][j], 0),
                      (i + 1, j - 1, grid[i + 1][j - 1], 0), (i, j - 1, grid[i][j - 1], 0)]

        for k in range(0, neighbours.__len__()):
            i1, j1, val, flag = neighbours[k]
            if val == -1:
                notOpenCount += 1
                neighbours[k] = (i1, j1, val, 1)
            elif val == 11:
                flagCount += 1

        if notOpenCount + flagCount == grid[i][j]:
            for i1, j1, val, flag in neighbours:
                if flag == 1:
                    print "marking " + str(i1-1) + ", " + str(j1-1) + " as flag"
                    grid[i1][j1] = 11
        elif flagCount == grid[i][j]:
            for i1, j1, val, flag in neighbours:
                if flag == 1 and grid[i1][j1] == -1:
                    print "opening " + str(i1 - 1) + ", " + str(j1 - 1)
                    grid[i1][j1] = 9


updateCost()
print grid
print '\n\n'
print midLayer
print '\n\n'
print cost
nextMove()

# square is 86 x 86
# grid is 688 x 688
# start = (76, 366), end = (764, 1054)
