from heapq import heapify, heappush, heappop
from itertools import product
from collections import deque

# K: 탐사 반복 횟수, M: 벽면에 적힌 유물 조각의 개수 
K, M = [int(x) for x in input().strip().split(' ')]
# 유물 조각에 적혀있는 숫자들
NUMBERS_ON_WALL = [
    [int(x) for x in input().strip().split(' ')] for _ in range(5)
]
# 유물 조각 번호

NUMBERS_PIECES = [int(x) for x in input().strip().split(' ')]

rotation_heap = []

iteration = 1

dxs = [1, -1, 0, 0]
dys = [0, 0, 1, -1]

OUTPUT = 0
ACQUISITION_TEMP = 0

#%% 

def board_init():

    # 매 iteration 돌면서 '덮어쓰기 + 변화'할 부분 
    NUMBERS_ON_WALL_TEMP = [
        [0] * 5 for _ in range(5)
    ]
    for i in range(5):
        for j in range(5):
            NUMBERS_ON_WALL_TEMP[i][j] = NUMBERS_ON_WALL[i][j]

    return NUMBERS_ON_WALL_TEMP
    

def in_range(x, y):
    return 0 <= x < 5 and 0 <= y < 5


def get_acquisition_value(board):

    is_visited = [
        [False] * 5 for _ in range(5)
    ]

    total_cnt = 0
    passthrough_list = []

    # 모든 지점을 돌아다님 
    for i in range(5):
        for j in range(5):
            if not is_visited[i][j]:

                q = deque([(i, j)])    # [x, y, count]
                is_visited[i][j] = True
                cnt = 1
                passthrough_tmp = [(i, j)]

                while q:
                    x, y = q.popleft()
                    for dx, dy in zip(dxs, dys):
                        next_x, next_y = x + dx, y + dy
                        if in_range(next_x, next_y) and not is_visited[next_x][next_y]: 
                            if board[x][y] == board[next_x][next_y]:
                                passthrough_tmp.append((next_x, next_y))
                                is_visited[next_x][next_y] = True
                                q.append([next_x, next_y])
                                cnt += 1

                if cnt >= 3:
                    total_cnt += cnt
                    passthrough_list.extend(passthrough_tmp)

    return total_cnt, passthrough_list


def board_update(row, col, angle, overwrite=False):

    global NUMBERS_ON_WALL

    BOARD_TEMP = board_init()    
    x_ul, y_ul = row-1, col-1

    # 회전 좌표의 중심 ( row, col의 좌표: 이미 fixed )
    # 2: Fixed 된 3x3 정사각형 변의 길이 
    for x_idx, i in enumerate(list(range(x_ul, row+2))):
        for y_idx, j in enumerate(list(range(y_ul, col+2))):
            current_val = NUMBERS_ON_WALL[i][j]
            if angle == 90:
                BOARD_TEMP[x_ul + y_idx][y_ul + 2 - x_idx] = current_val
            elif angle == 180: 
                BOARD_TEMP[x_ul + 2 - x_idx][y_ul + 2 - y_idx] = current_val
            else:
                BOARD_TEMP[x_ul + 2 - y_idx][y_ul + x_idx] = current_val
    
    if overwrite:
        NUMBERS_ON_WALL = BOARD_TEMP

    return BOARD_TEMP
    

def rotation(row, col, angle):
    global rotation_heap
    BOARD_TEMP = board_update(row, col, angle, False)
    acquisition_value, passthrough_index = get_acquisition_value(BOARD_TEMP)
    heappush(rotation_heap, (-1 * acquisition_value, angle, col, row, acquisition_value, passthrough_index))
    

def update_board(acquisition_value, passthrough_index):

    global NUMBERS_ON_WALL, NUMBERS_PIECES, ACQUISITION_TEMP

    if acquisition_value == 0:
        return 
    else:
        ACQUISITION_TEMP += acquisition_value

    coord_heap = []

    for i, j in passthrough_index:
        NUMBERS_ON_WALL[i][j] = 0
        heappush(coord_heap, (j, -i))
    
    cnt = 0
    while coord_heap:
        j, minus_i = heappop(coord_heap)
        NUMBERS_ON_WALL[-1*minus_i][j] = NUMBERS_PIECES[cnt]
        cnt += 1 

    NUMBERS_PIECES = NUMBERS_PIECES[cnt:]

    acquisition_value, passthrough_index = get_acquisition_value(NUMBERS_ON_WALL)
    update_board(acquisition_value, passthrough_index)


# 탐사 진행
def exploration():

    global rotation_heap, ACQUISITION_TEMP, OUTPUT

    # 회전의 중심: [row, col]
    for row in range(1, 4):
        for col in range(1, 4):
            rotation(row, col, 90)
            rotation(row, col, 180)
            rotation(row, col, 270)
    
    rotation_popped = heappop(rotation_heap)

    if rotation_popped[-2] == 0: # acquisition value 
        return True
    
    board_update(*rotation_popped[1:4][::-1], overwrite=True)
    update_board(*rotation_popped[-2:])
    OUTPUT += ACQUISITION_TEMP
    ACQUISITION_TEMP = 0
    
    return False

answer = ''
while iteration <= K:

    rotation_heap = []
    is_ended = exploration()

    if OUTPUT != 0:
        answer += str(OUTPUT) + ' '
    if is_ended:
        break

    iteration += 1
    OUTPUT = 0
    
print(answer.strip())