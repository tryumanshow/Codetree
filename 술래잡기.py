from itertools import chain

# n: 홀수


"""
n: 홀수  (n x n 크기의 격자)
"""

n, m, h, k = [int(x) for x in input().split(' ')]

chaser_grid = [n // 2, n // 2]

domang_grid = [
    [int(x) - 1 for x in input().split(' ')] for _ in range(m)
]  # -1 : 인덱스 보정

tree_grid = [
    [int(x) - 1 for x in input().split(' ')] for _ in range(h)
]

dxdy_list = {
    # 우
    0: [0, 1],
    # 하
    1: [1, 0],
    # 좌
    2: [0, -1],
    # 상
    3: [-1, 0],
}

dxdy_mapper = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}

"""
사용할 변수
n
chaser_grid
domang_grid
tree_grid
"""

def distance(domang_info):
    domang_x, domang_y = domang_info
    distance = abs(domang_x - chaser_grid[0]) + abs(domang_y - chaser_grid[1])
    return True if distance <= 3 else False


def domang_move():
    global domang_grid

    domang_grid_cp = []

    for dg in domang_grid:
        whether2move = distance(dg[:2])
        if whether2move:
            next_dir = dg[-1]
            dx, dy = dxdy_list[next_dir]  # 좌우선택
            next_dx, next_dy = dg[0] + dx, dg[1] + dy

            # 격자를 벗어나는 경우
            if (next_dx < 0) or (next_dx >= n) or (next_dy < 0) or (next_dy >= n):
                next_dir = dxdy_mapper[next_dir]
                dx, dy = dxdy_list[next_dir]

            next_dx, next_dy = dg[0] + dx, dg[1] + dy
            # 움직이려는 칸에 술래가 있는 경우 : 움직이지 않음.
            if [next_dx, next_dy] == chaser_grid:
                domang_grid_cp.append([dg[0], dg[1], next_dir])
            # 움직이려는 칸에 술래가 있지 않은 경우
            else:
                domang_grid_cp.append([next_dx, next_dy, next_dir])
        else:
            domang_grid_cp.append(dg)

    domang_grid = domang_grid_cp

    del domang_grid_cp


def chaser_move(time):
    global chaser_grid

    time_idx = time - 1  # 인덱스 보정

    dxdy = chaser_directions[chaser_pattern[time_idx % cp_len]]

    for i in range(2):  # x-axis, y-axis
        chaser_grid[i] = chaser_grid[i] + dxdy[i]


def chaser_catch(time):
    global score, domang_grid

    cnt = 0

    # 일단 시선은 다음 시선으로 옮겨두어야.
    next_dir = chaser_pattern[time % cp_len]

    dxdy = chaser_directions[next_dir]

    for i in range(3):  # 바라보고 있는 방향 기준, 현재 칸 포함 3칸

        next_dx = chaser_grid[0] + i * dxdy[0]
        next_dy = chaser_grid[1] + i * dxdy[1]

        if (0 <= next_dx < n) and (0 <= next_dy < n):
            if [next_dx, next_dy] not in tree_grid:
                for idx, dg in enumerate(domang_grid):
                    if [next_dx, next_dy] == dg[:-1]:
                        domang_grid_cp = [x for i, x in enumerate(domang_grid) if x != dg]
                        cnt += (len(domang_grid) - len(domang_grid_cp))
                        domang_grid = domang_grid_cp

    score += cnt * time


"""
# Pattern
# 1, 1, 2, 2, 3, 3, 4, 4, 4 // 4, 4, 4, 3, 3, 2, 2, 1, 1
# 결국, n-1을 세 번 거치는 것 말고는, 나머지는 두 번씩 거치게 됨. 
# ['상', '우', '하', '좌'] 반복 + 상 // 대칭으로 정반대.
"""

chaser_directions = {
    # 순서: 상 우 하 좌
    0: [-1, 0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}
opposite_direction = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}

num_pattern = [
    list(chain(*([idx] * 2 for idx in range(1, n))))
][0]
num_pattern += [num_pattern[-1]]

chaser_keys = list(chaser_directions.keys())
chaser_pattern = []

for idx, np in enumerate(num_pattern):
    chosen = chaser_keys[idx % 4]
    chaser_pattern.extend([chosen] * np)

chaser_pattern = chaser_pattern + list(map(lambda x: opposite_direction[x], chaser_pattern[::-1]))
cp_len = len(chaser_pattern)

del num_pattern

time = 1
score = 0

while time <= k:

    domang_move()

    chaser_move(time)

    chaser_catch(time)

    time += 1

    if len(domang_grid) == 0:
        break

print(score)