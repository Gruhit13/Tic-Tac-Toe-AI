import pygame
import numpy as np
import Model
import time
pygame.init()

white = (255, 255, 255)
red = (255,0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#For displaying Message
font_style = pygame.font.SysFont(None, 50)

def message(win, msg, color):
    mesg = font_style.render(msg, True, color)
    win.fill((0, 0, 0))
    win.blit(mesg, (200, 300))
    pygame.display.update()
    time.sleep(2)

def plotXO(win, clicked_pos, line_width, img):
    clicked_pos[0] = (clicked_pos[0] // 200) * 200
    clicked_pos[1] = (clicked_pos[1] // 200) * 200
    win.blit(img, ( clicked_pos[0] + line_width, clicked_pos[1] + line_width))
    pygame.display.update()

def CheckCols(arr):
    for i in range(arr.shape[0]):
        col_sum = np.sum(arr[:, i])
        if col_sum == 3: return 1
        if col_sum == -3: return -1
    return 0

def CheckRows(arr):
    for rows in arr:
        row_sum = np.sum(rows)
        if row_sum == 3: return 1
        if row_sum == -3: return -1
    return 0

def giveXYcoord(table):
    table = np.array(table, dtype='int32')

def CheckDiagonals(arr):
    diagonal = []
    for i in range(3): diagonal.append(arr[i, i])
    if np.sum(diagonal) == 3: return 1
    elif np.sum(diagonal) == -3: return -1
    else:
        diagonal = []
        for i in range(3):
            diagonal.append(arr[i, 2-i])
        if np.sum(diagonal) == 3: return 1
        if np.sum(diagonal) == -3: return -1
    return 0

def CheckResult(arr):
    arr = np.array(arr, dtype='int32').reshape(3, 3)
    val = CheckCols(arr)
    if val == 0:
        val = CheckRows(arr)
        if val == 0:
            val = CheckDiagonals(arr)
            return val
    return val

def CheckValidMove(table, index):
    if table[index] == 0: return True
    else: return False

def PlotLine(win, sPnt, ePnt):
    pygame.draw.line(win, (255, 0, 0), (sPnt[0], sPnt[1]), (ePnt[0], ePnt[1]), 5)
    pygame.display.update()

#Plotting line for the winner
def CheckWinner(win, table):
    #Checking Columns

    start_point = np.zeros(2, dtype='int32')
    end_point = np.zeros(2, dtype='int32')
    table = np.array(table, dtype='int32').reshape(3, 3)

    for i in range(3):
        cols = np.sum(table[:, i])
        if np.abs(cols) == 3:
            start_point = [(2*i+1)*100, 50 ]
            end_point = [(2*i+1)*100, 550 ]
            PlotLine(win, start_point, end_point)
            return 0

    #cheking Rows
    for i in range(3):
        row = np.abs(np.sum(table[i, :]))
        if row == 3:
            start_point = [50, (2*i+1)*100]
            end_point = [550, (2*i+1)*100]
            PlotLine(win, start_point, end_point)
            return 0

    #cheking Diagonals
    sum_dig = 0
    main_dig = np.diagonal(table)
    if np.abs(np.sum(main_dig)) == 3:
        start_point = [50, 50]
        end_point = [550, 550]
        PlotLine(win, start_point, end_point)
        return 0
    other_dig = np.fliplr(table).diagonal()
    if np.sum(np.sum(other_dig)) == 3:
        start_point = [150, 550]
        end_point = [550, 50]
        PlotLine(win, start_point, end_point)
        return 0

def GetBestMove(y_val, table):
    if CheckValidMove(table, 4): return 4

    oneVal = []
    for i in range(len(y_val)):
        if y_val[i] == 1:
            oneVal.append(i)

    for value in oneVal:
        temp_y_val = y_val
        temp_y_val[value] = 1
        getResult = CheckResult(temp_y_val)
        if getResult == 1:
            if CheckValidMove(table, value):
                return value

    #Checking if User has no Trio to be completing
    #Checking columns
    arr = np.array(table).reshape(3,3)
    count_col = 6
    for i in range(3):
        col = arr[:, i]
        cols_sum = np.sum(col)
        if abs(cols_sum) == 2:
            for j in range(3):
                if col[j] == 0: break
            return count_col - 3 * (2 - j)
        count_col += 1

    #checking for rows
    zero_val = 0
    countRowEndInd = 2
    for row in arr:
        row_sum = np.sum(row)
        if abs(row_sum) == 2:
            for i in range(3):
                if row[i] == 0: break
            return countRowEndInd - (2-i)
        countRowEndInd += 3

    #Checking diagonals
    dia_sum = 0
    zero_val = 0
    for i in range(3):
        dia_sum += arr[i, i]
        if arr[i, i] == 0: zero_val = i
    if dia_sum == -2: return zero_val*4
    else:
        dia_sum = 0
        zero_val = 0
        for i in range(3):
            dia_sum += arr[i, 2-i]
            if arr[i, 2-i] == 0: zero_val = i
        if dia_sum == -2: return 2+ (2*zero_val)

    return oneVal[0]

def CheckZero(table):
    counter = 0
    for i in table:
        if i == 0: return True
    return False

def createWindow():
    screen_width = 600
    screen_height = 600
    line_width = 5
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Screen")

    # Loading x and setting resolution
    X_img = pygame.image.load("x.png")
    X_img = pygame.transform.scale(X_img, (200 - line_width, 200 - line_width))

    # loading o and setting resolution
    O_img = pygame.image.load("o.png")
    O_img = pygame.transform.scale(O_img, (200 - line_width, 200 - line_width))

    # Drawing 2 horizontal lines
    pygame.draw.rect(win,blue,(0, 1, screen_width, line_width))
    pygame.draw.rect(win,blue,(0, 200,screen_width, line_width))
    pygame.draw.rect(win, blue, (0, 400, screen_width, line_width))
    pygame.draw.rect(win, blue,(0, 595, screen_width, line_width))

    # Drawing vertical lines
    pygame.draw.rect(win, blue, ( 1, 0, line_width, screen_height))
    pygame.draw.rect(win, blue, (200, 0, line_width, screen_height))
    pygame.draw.rect(win, blue, (400, 0, line_width, screen_height))
    pygame.draw.rect(win, blue, (595,0, line_width, screen_height))
    pygame.display.update()
    return win, X_img, O_img, line_width

def playGame():
    win, X_img, O_img, line_width = createWindow()
    tableCoOrdinateArray = []
    tableArray = []
    for i in range(3):
        for j in range(3):
            tableCoOrdinateArray.append([j*200, i*200])
            tableArray.append(0)

    print(tableCoOrdinateArray)
    clicked_pos = [0, 0]
    obj = Model.model()
    gameOver = False

    while CheckZero(tableArray) and not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = np.array(pygame.mouse.get_pos())
                get_ind = tableCoOrdinateArray.index([(clicked_pos[0] // 200) * 200, (clicked_pos[1] // 200) * 200])
                if CheckValidMove(tableArray, get_ind):
                    tableArray[get_ind] = -1
                    plotXO(win, clicked_pos, line_width, X_img)
                else: continue

                result = CheckResult(tableArray)
                if result != 0:
                    CheckWinner(win, tableArray)
                    pygame.display.update()
                    time.sleep(1)
                    message(win, "You WON!!!", red)

                    gameOver = True
                    break;
                else:
                    #feeding value in model and getting value
                    y_pred = obj.getPredValue(tableArray)

                    index = GetBestMove(y_pred, tableArray)
                    if CheckValidMove(tableArray, index):
                        tableArray[index] = 1
                        clicked_pos = tableCoOrdinateArray[index]
                        plotXO(win, clicked_pos, line_width, O_img)

                        result = CheckResult(tableArray)
                        if result != 0:
                            CheckWinner(win, tableArray)

                            time.sleep(5)
                            message(win, "AI WON!!!", red)
                            gameOver = True

    if CheckResult(tableArray) == 0: message(win, "It's DRAW", red)
    print("Enter q to exit")

    GameMsg = "Want another game(y/n)?"
    message(win, GameMsg, red)

    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    pygame.quit()
                if event.key == pygame.K_y:
                    playGame()
                    tableArray = [0 for _ in range(9)]
playGame()