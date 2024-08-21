from collections import deque

# R: Row, C: Col, K: 정령 수 
R, C, K = [int(x) for x in input().strip().split()]

GOLLEM_INFO = [
    # 각 element: [c_i, d_i]
    # c_i : 출발 column #
    # d_i : 방향 (북, 동, 남, 서) = (0, 1, 2, 3)
    [int(x) for x in input().strip().split()] for _ in range(K)
]

MOVING_DXDY = {
    # "변화량"
    # 동
    1: [[1, 2], [2, 1], [-1, 1], [0, 2], [1, 1]],
    # 남
    2: [[2, 0], [1, -1], [1, 1]],
    # 서
    3: [[1, -2], [2, -1], [-1, -1], [0, -2], [1, -1]]
}

MOVING_COORD = {
    0: [-1, 0],     # 북
    1: [0, 1],      # 동
    2: [1, 0],      # 남
    3: [0, -1]      # 서
}

ENTRANCE_DXDY = {
    1: 1, # 동 : 시계방향
    2: 0, # 남: 그대로 
    3: -1, # 서: 반시계방향 
}


DX = [-1, 1, 0, 0]
DY = [0, 0, 1, -1]


door_board = None
gollem_board = None
answer = 0


def in_range(x, y):
    return 0 <= x < R and 0 <= y < C


def board_init():
    global door_board, gollem_board
    door_board = [
        [0] * C for _ in range(R)
    ]
    gollem_board = [
        [0] * C for _ in range(R)
    ]


def is_moving_possible(x, y, direction):

    # 맨 첫 시작점 
    if x == -2:
        if direction == 2:
            if door_board[0][y] == 0:
                return True
            else:
                return False
        else:   # Line 69 - 79 의 로직을 담지 않아서, Case 34번에서 에러. 🌟🌟🌟
            if direction == 3:
                if door_board[0][y-1] == 0:
                    return True
                else:
                    return False
            elif direction == 1:
                if door_board[0][y+1] == 0:
                    return True
                else:
                    return False

    cnt = 0
    for dx, dy in MOVING_DXDY[direction]:   # 2, 3, 1 등장 가능 
        next_x, next_y = x + dx, y + dy
        if in_range(next_x, next_y):
            if door_board[next_x][next_y] == 0:
                cnt += 1
        if direction != 2:
            if x == 0:
                if direction == 3:      # 서
                    if dx == dy == -1:
                        cnt += 1
                elif direction == 1:    # 동
                    if dx == dy == 1:
                        cnt += 1
            elif x == -1:
                if direction == 3:      # 서
                    if dx <= 0 and dy <= 0:
                        cnt += 1
                elif direction == 1:    # 동
                    if dx <= 0 and dy >= 0:
                        cnt += 1

    if direction == 2:
        if cnt == 3:
            return True
    else:
        if cnt == 5:
            return True

    return False


def total_steps_to_escape(start_x, start_y):

    global door_board

    is_visited = [
        [False] * C for _ in range(R)
    ]

    q = deque([[start_x, start_y,]]) # 관심 골렘의 문 위치에 서 있는지. 
    is_visited[start_x][start_y] = True

    bottom_most = start_x

    while q:
        x, y = q.popleft()

        door_current = door_board[x][y]
        gollem_current = gollem_board[x][y]

        for dx, dy in zip(DX, DY):

            next_x, next_y = x + dx, y + dy

            if in_range(next_x, next_y):    

                gollem_next = gollem_board[next_x][next_y]  

                flag = False
                if not is_visited[next_x][next_y] and gollem_next != 0: # 이 아래 부분의 로직을 제대로 못 짜서 16번 에러 🌟🌟🌟

                    if gollem_current != gollem_next:
                        if door_current == 2:
                            flag = True
                            q.append([next_x, next_y])
                    else:  
                        flag = True
                        q.append([next_x, next_y])

                    if flag:
                        bottom_most = max(bottom_most, next_x)
                        is_visited[next_x][next_y] = True

    return bottom_most


def update_door_board(x, y, door, idx):

    global door_board, gollem_board

    # 골렘의 위치 모두를 1로 표기
    for dx, dy in zip(DX, DY):
        next_dx, next_dy = x + dx, y + dy
        door_board[next_dx][next_dy] = 1
        gollem_board[next_dx][next_dy] = idx + 1

    # 정령의 위치도 1로 표기 
    door_board[x][y] = 1
    gollem_board[x][y] = idx + 1

    # 문의 위치는 2로 표기 
    door_x, door_y = MOVING_COORD[door]
    door_board[x+door_x][y+door_y] = 2


#%%

board_init()

for idx, g_info in enumerate(GOLLEM_INFO):
    
    start_r = -2
    start_c, direction = g_info
    start_c -= 1    # index 보정 

    # 더 이상 움직일 수 없으면 탈출 
    while True:
        moving_possible = False
        for mv in [2, 3, 1]:    # 남 -> 서 -> 동 
            moving_possible = is_moving_possible(start_r, start_c, mv)
            if moving_possible:
                dx, dy = MOVING_COORD[mv]
                start_r += dx
                start_c += dy
                # 방향 전환 
                direction = (direction + ENTRANCE_DXDY[mv]) % 4    
                break 

        # 전혀 움직이지 못했을 때 -> table re init
        if start_r <= 0 and (not moving_possible):  # 여기서 0을 -1로 했다가 시간 많이 잡아먹음. 
            board_init()
            break

        elif (not moving_possible) or (start_r == R-2) :   # 움직이는 게 불가능하거나, 최대한 남쪽까지 도달했거나 
            update_door_board(start_r, start_c, direction, idx)
            break

    if start_r >= 1:
        row_cnt = total_steps_to_escape(start_r, start_c)
        answer += (row_cnt + 1) # index는 -1로 취급하기 때문에, 답을 내려면 1 더 추가해줘야 함. 

print(answer)