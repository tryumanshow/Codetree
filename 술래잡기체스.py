from copy import deepcopy

infos = [
    [int(x) for x in input().strip().split()] for _ in range(4)
]

grid = [
    [] for _ in range(4)
]  # (번호, 방향) 정보를 함께 담을 것.

for i in range(4):
    for j in range(4):
        num = infos[i][2 * j]
        direction = infos[i][2 * j + 1] - 1  # 인덱스 보정
        grid[i].append([num, direction])

#       ↑,  ↖,  ←, ↙,  ↓, ↘, →,  ↗
dxs = [-1, -1, 0, 1, 1, 1, 0, -1]
dys = [0, -1, -1, -1, 0, 1, 1, 1]

CHASER = [-100, -100]
NOBODY = [-99, -99]
max_score = 0


def in_range(x, y):
    return (0 <= x < 4) and (0 <= y < 4)


def thieves_move():
    for i in range(1, 17):
        theif_move(i)


def theif_move(i):

    for x in range(4):

        for y in range(4):

            if grid[x][y][0] != i:
                continue

            dir_idx = grid[x][y][1]

            while True:
                dir_reidx = dir_idx % 8
                dx, dy = dxs[dir_reidx], dys[dir_reidx]
                next_x, next_y = x + dx, y + dy

                # 도둑이 이동할 수 없는 경우
                # if (grid[next_x][next_y] == CHASER) or (not in_range(next_x, next_y)):
                if not (in_range(next_x, next_y) and grid[next_x][next_y] != CHASER):
                    dir_idx += 1
                    continue

                grid[x][y] = [i, dir_reidx]
                grid[next_x][next_y], grid[x][y] = grid[x][y], grid[next_x][next_y]

                return


# dfs
def catcher_move(x, y, direction, score):
    global max_score

    dx, dy = dxs[direction], dys[direction]

    # 종료조건
    for i in range(1, 4):
        next_x = x + i * dx
        next_y = y + i * dy

        if in_range(next_x, next_y) and grid[next_x][next_y] != NOBODY:
            break
        else:  # 술래가 더 이상 이동할 수 없는 경우
            if i == 3:
                max_score = max(max_score, score)
                return

    for i in range(1, 4):
        next_x = x + i * dx
        next_y = y + i * dy

        if not (in_range(next_x, next_y) and grid[next_x][next_y] != NOBODY):
            continue

        grid_cp = [
            [grid[i][j] for j in range(4)] for i in range(4)
        ]

        # 술래가 말 잡기
        next_score, next_dir = grid[next_x][next_y]
        grid[next_x][next_y], grid[x][y] = CHASER, NOBODY

        # 도둑들 움직이기
        thieves_move()

        catcher_move(next_x, next_y, next_dir, score + next_score)

        for i in range(4):
            for j in range(4):
                grid[i][j] = grid_cp[i][j]


init_num, init_dir = grid[0][0]
grid[0][0] = CHASER

thieves_move()

catcher_move(0, 0, init_dir, init_num)

print(max_score)