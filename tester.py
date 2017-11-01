import numpy as np
import cv2
import pickle
import pyautogui as pg

grid = np.full((8, 8), 0, dtype=np.int)
# -1 = not open
# 0 = open
# 1 = 1
# 2 = 2
# 3 = 3
# 4 = 4
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
# 10 = opened
# 99 = flag

midLayer = np.full((10, 10), 0, dtype=np.int)
# 10x10 because cost update takes 3x3 neighbourhood into account, thus for edges we have to add padding
# 0 = not opened, opened, flag
# 1 = 1, 2, 3, 4

f = open('model.txt', 'rb')
s = f.read()
classifier = pickle.loads(s)

snap = cv2.imread("1-2-3.png")


def updateSnap():
    # updates the screen shot after a move has been made

    global snap
    snap = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)


def updateGrid():
    # updates the grid matrix, a digital representation of the 8x8 minesweeper grid

    global grid
    for i in range(0, 8, 1):
        startX = 76 + (i * 86)
        for j in range(0, 8, 1):
            startY = 366 + (j * 86)
            part = snap[startX:startX + 86, startY:startY + 86, :]
            prediction = classifier.predict(part.ravel())[0]
            if prediction == '1':
                grid[i][j] = 1
            elif prediction == '2':
                grid[i][j] = 2
            elif prediction == '3':
                grid[i][j] = 3
            elif prediction == '4':
                grid[i][j] = 4
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
            # print prediction
            cv2.waitKey(1)


def updateMidLayer():
    # updates the midLayer matrix which makes the calculation of cost matrix easier and faster

    global midLayer, grid
    updateGrid()
    for i in range(0, 8):
        for j in range(0, 8):
            if grid[i][j] == -1 or grid[i][j] == 11 or grid[i][j] == 0:
                midLayer[i + 1][j + 1] = 0
            else:
                midLayer[i + 1][j + 1] = 1


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


updateCost()
print grid
print '\n\n'
print midLayer
print '\n\n'
print cost

# square is 86 x 86
# grid is 688 x 688
# start = (76, 366), end = (764, 1054)
