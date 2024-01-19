from collections import defaultdict, deque

n, m, k = [int(x) for x in input().strip().split()]

grid = [
    [int(x) for x in input().strip().split()] for _ in range(n)
]

walls = [
    [int(x) - 1 for x in input().strip().split()] for _ in range(m)
]
wall_dict = defaultdict(list)

for wall_row, wall_col, wall_dir in walls:
    wall_dict[f'{wall_row},{wall_col}'].append(wall_dir + 1)

ac_position = []
office_position = []

for i in range(n):
    for j in range(n):
        if grid[i][j] > 1:
            ac_position.append([i, j, grid[i][j]])  # row, col, 에어컨 방향
        if grid[i][j] == 1:
            office_position.append([i, j])

total_wind_num = [
    [0] * n for _ in range(n)
]

dxs_info = {
    2: [[0], [-1, 0], [1, 0]],  # 왼
    3: [[-1], [0, -1], [0, -1]],  # 위
    4: [[0], [-1, 0], [1, 0]],  # 오른
    5: [[1], [0, 1], [0, 1]]  # 아래
}  # 직진, 위 -> 내 방향, 아래 -> 내 방향

dys_info = {
    2: [[-1], [0, -1], [0, -1]],
    3: [[0], [-1, 0], [1, 0]],
    4: [[1], [0, 1], [0, 1]],
    5: [[0], [-1, 0], [1, 0]]
}

is_visited = [
    [False] * n for _ in range(n)
]

"""
n: 격자 크기
m: 벽의 개수
k: 원하는 시원함의 정도 
"""

"""
0: 빈 공간
1: 사무실 구역
2: 에어컨 방향: 왼쪽 
3: 에어컨 방향: 위쪽 
4: 에어컨 방향: 오른쪽 
5: 에어컨 방향: 아래쪽
"""

"""
ex) 에어컨 Type 4 인 경우
위측 45도: 위 -> 우측 순서
아래쪽 45도: 아래 -> 우측 순서 

즉 대각선 이동은 ⭐️
- 내 진행방향 -> 위/아래 (X)
- 위/아래 -> 내 진행방향 (O)
"""


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def init():
    global is_visited, total_wind_num

    is_visited = [
        [False] * n for _ in range(n)
    ]


def wall_blocked(sub_dx, sub_dy, next_x, next_y):
    if [sub_dx, sub_dy] == [1, 0]:  # down
        if 0 in wall_dict[f'{next_x},{next_y}']:
            return False

    elif [sub_dx, sub_dy] == [0, 1]:  # right
        if 1 in wall_dict[f'{next_x},{next_y}']:
            return False

    elif [sub_dx, sub_dy] == [-1, 0]:  # up
        if 0 in wall_dict[f'{next_x + 1},{next_y}']:
            return False

    else:  # left
        if 1 in wall_dict[f'{next_x},{next_y + 1}']:
            return False

    return True


def dfs(row, col, dx_info, dy_info, score):
    if not in_range(row, col):
        return

    if is_visited[row][col]:
        return

    if score == 0:
        return

    is_visited[row][col] = True
    total_wind_num[row][col] += score

    row_o, col_o = row, col

    for i in range(3):
        row, col = row_o, col_o
        dxs = dx_info[i]
        dys = dy_info[i]
        for j in range(len(dxs)):
            dx, dy = dxs[j], dys[j]
            next_dx = row + dx
            next_dy = col + dy
            wall_tf = wall_blocked(dx, dy, next_dx, next_dy)
            if not wall_tf:
                break
            if in_range(next_dx, next_dy) and not is_visited[next_dx][next_dy]:
                if j != len(dxs) - 1:
                    row, col = next_dx, next_dy
                else:
                    dfs(next_dx, next_dy, dx_info, dy_info, score - 1)


def wind_blow():
    global is_visited

    for row, col, ac_direction in ac_position:  # 모든 케이스들을 여기서 한 번에 처리

        init()

        dx_info = dxs_info[ac_direction]
        dy_info = dys_info[ac_direction]

        # 일단 한 칸 간 후 시작.
        start_row = row + dx_info[0][0]
        start_col = col + dy_info[0][0]

        if not in_range(start_row, start_col):
            continue

        dfs(start_row, start_col, dx_info, dy_info, 5)


def wind_mix():
    total_wind_num_temp = [
        [0] * n for _ in range(n)
    ]

    # 내 아래, 오른쪽과만 비교하면 됨
    for i in range(n):

        for j in range(n):

            me = total_wind_num[i][j]

            # 내 아래
            if (in_range(i + 1, j)) and (0 not in wall_dict[f'{i + 1},{j}']):
                neighbor = total_wind_num[i + 1][j]
                to_add = me - neighbor
                if to_add > 0:
                    total_wind_num_temp[i + 1][j] += to_add // 4
                    total_wind_num_temp[i][j] -= to_add // 4
                elif to_add < 0:
                    total_wind_num_temp[i][j] += -to_add // 4
                    total_wind_num_temp[i + 1][j] -= -to_add // 4

            # 내 오른쪽
            if (in_range(i, j + 1)) and (1 not in wall_dict[f'{i},{j + 1}']):
                neighbor = total_wind_num[i][j + 1]
                to_add = (me - neighbor)
                if to_add > 0:
                    total_wind_num_temp[i][j + 1] += to_add // 4
                    total_wind_num_temp[i][j] -= to_add // 4
                elif to_add < 0:
                    total_wind_num_temp[i][j] += -to_add // 4
                    total_wind_num_temp[i][j + 1] -= -to_add // 4

    for i in range(n):
        for j in range(n):
            total_wind_num[i][j] += total_wind_num_temp[i][j]


def decrease_one():
    for i in [0, n - 1]:
        for j in range(1, n - 1):
            if total_wind_num[i][j] != 0:
                total_wind_num[i][j] -= 1

    for j in [0, n - 1]:
        for i in range(1, n - 1):
            if total_wind_num[i][j] != 0:
                total_wind_num[i][j] -= 1

    for i in [0, n - 1]:
        for j in [0, n - 1]:
            if total_wind_num[i][j] != 0:
                total_wind_num[i][j] -= 1


def judge():
    cnt = 0
    for i, j in office_position:
        if total_wind_num[i][j] >= k:
            cnt += 1

    return cnt


t = 0
while True:

    wind_blow()

    wind_mix()

    decrease_one()

    cnt = judge()

    t += 1

    if len(office_position) == cnt:
        break

    if t > 100:
        break

t = -1 if t > 100 else t

print(t)
