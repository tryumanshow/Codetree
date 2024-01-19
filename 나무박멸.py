import sys
from copy import deepcopy

dead_cnt = 0

# n: 격자의 크기
# m: 박멸 진행 년수
# k: 제초제 확산범위
# c: 제초나 남아있는 년 수
n, m, k, c = [int(x) for x in input().strip().split(' ')]

trees_grid = [
    [int(x) for x in input().strip().split(' ')] for _ in range(n)
]

# 제초제 관련 정보 업데이트 할 곳
drug_duration = [
    [0] * n for _ in range(n)
]

# 상우하좌
dxs = [-1, 0, 1, 0]
dys = [0, 1, 0, -1]

# 좌상, 우상, 좌하, 우하
diag_dxs = [-1, -1, 1, 1]
diag_dys = [-1, 1, -1, 1]


# 나무의 성장
def growth():
    for x in range(n):
        for y in range(n):

            temp = 0
            for dx, dy in zip(dxs, dys):
                next_x = x + dx
                next_y = y + dy
                if trees_grid[x][y] > 0:
                    if (next_x >= 0) and (next_x < n) and (next_y >= 0) and (next_y < n) and \
                            trees_grid[next_x][next_y] > 0:  # -1, 0  모두 제외
                        temp += 1
            trees_grid[x][y] += temp


# 나무의 번식
def flourish():
    global trees_grid

    trees_grid_cp = deepcopy(trees_grid)

    for x in range(n):
        for y in range(n):

            if trees_grid[x][y] > 0:
                index_list = []
                for dx, dy in zip(dxs, dys):
                    next_x = x + dx
                    next_y = y + dy
                    if (next_x >= 0) and (next_x < n) and (next_y >= 0) and (next_y < n):
                        if trees_grid[next_x][next_y] == 0:
                            index_list.append([next_x, next_y])

                if len(index_list) >= 1:
                    to_add = trees_grid[x][y] // len(index_list)
                    for il in index_list:
                        trees_grid_cp[il[0]][il[1]] += to_add

    trees_grid = trees_grid_cp


def drug_duration_update():
    for x in range(n):
        for y in range(n):
            if drug_duration[x][y] != 0:
                drug_duration[x][y] = max(0, drug_duration[x][y] - 1)
                if drug_duration[x][y] == 0 and trees_grid[x][y] != -1:  # 벽은 제외
                    trees_grid[x][y] = 0


# 제초제 위치 선정
def drug_emit():
    global dead_cnt

    drug_effect = [
        [0] * n for _ in range(n)
    ]
    temp_idx, temp_min = [], -1 * sys.maxsize

    for x in range(n):
        for y in range(n):

            if trees_grid[x][y] > 0:

                temp = 0
                kill_idx = [[x, y]]  # 나 자신
                for dx, dy in zip(diag_dxs, diag_dys):
                    for z in range(1, k + 1):
                        next_dx = x + dx * z
                        next_dy = y + dy * z
                        if (next_dx >= 0) and (next_dx < n) and (next_dy >= 0) and (next_dy < n):
                            kill_idx.append([next_dx, next_dy])
                            if trees_grid[next_dx][next_dy] > 0:  # 나무가 존재하는
                                temp += trees_grid[next_dx][next_dy]
                            if trees_grid[next_dx][next_dy] <= 0:  # 벽이 있거나, 나무 아예 없거나, 제초제가 뿌려진
                                break
                        else:
                            break

                drug_effect[x][y] = temp
                drug_effect[x][y] += trees_grid[x][y]
                if drug_effect[x][y] > temp_min:
                    temp_min = drug_effect[x][y]
                    temp_idx = kill_idx

    if len(temp_idx) >= 1:
        for ti_x, ti_y in temp_idx:
            if trees_grid[ti_x][ti_y] > 0:
                dead_cnt += trees_grid[ti_x][ti_y]
            if trees_grid[ti_x][ti_y] != -1:
                trees_grid[ti_x][ti_y] = -100  # dead
                drug_duration[ti_x][ti_y] = c

    del drug_effect, temp_idx


year = 1

while year <= m:
    growth()

    flourish()

    drug_duration_update()

    drug_emit()

    year += 1

print(dead_cnt)