from collections import defaultdict
import sys
import math

n, k = [int(x) for x in input().strip().split()]

flour = [int(x) for x in input().strip().split()]

MAX = sys.maxsize

dxs = [-1, 0, 1, 0]  # 상 -> 우 -> 하 -> 좌 -> 상 ...
dys = [0, 1, 0, -1]

flour_after_turn = []

"""
n: 밀가루 양이 담긴 배열 크기 
k: 최대값 , 최소값 차이 
flour: 밀가루의 양 
"""


def in_range(x, y, max_row, max_col):
    return 0 <= x < max_row and 0 <= y < max_col


# 밀가루 양이 가장 작은 위치에 밀가루 1만큼 더 넣어주기
def stage1():
    global flour

    minimum = min(flour)

    for idx, f in enumerate(flour):
        if f == minimum:
            flour[idx] += 1


def find_combination(num):
    min_diff = MAX
    output = [-1, -1]
    for row in range(1, math.floor(num ** 0.5) + 1):
        col, r = divmod(num, row)
        if row > col:
            break
        if r == 0 and col >= row:
            diff = col - row
            if min_diff > diff:
                min_diff = diff
                output[0] = row
                output[1] = col

    return output


def stage2_turn_dfs(row, col, max_row, max_col, cnt, predefined_dir):
    global flour_after_turn

    flour_after_turn[row][col] = flour[cnt]

    if cnt == 0:
        return

    x_, y_ = -100, -100  # next step
    direction = 0

    for dir_idx in range(predefined_dir, predefined_dir + 4):
        dir_idx_corrected = dir_idx % 4
        x_dx, y_dy = dxs[dir_idx_corrected], dys[dir_idx_corrected]
        next_dx, next_dy = row + x_dx, col + y_dy
        if in_range(next_dx, next_dy, max_row, max_col):
            if flour_after_turn[next_dx][next_dy] == -100:
                x_, y_ = next_dx, next_dy
                direction = dir_idx_corrected
                break

    stage2_turn_dfs(x_, y_, max_row, max_col, cnt - 1, direction)


# 도우 말아주기
def stage2():
    global flour_after_turn

    num_flour = len(flour)
    front_iter = sorted(list(range(1, num_flour)) * 2)
    back_iter = sorted(list(range(0, num_flour - 1)) * 2)[1:]

    step = 0
    front = 0
    while True:
        front += front_iter[step]
        back = front + back_iter[step]
        if num_flour - 1 < back:
            front -= front_iter[step]
            break
        step += 1

    row, col = find_combination(front)

    flour_after_turn = [[-100] * n for _ in range(row + 1)]

    # 맨 아래에 깔려있는 줄의 숫자부터 채움.
    for idx, i in enumerate(range(front, len(flour))):
        flour_after_turn[row][idx] = flour[i]

    stage2_turn_dfs(row - 1, 0, row, col, front - 1, 0)  # 항상 윗방향으로 가는 것부터 시작

    for col in range(len(flour_after_turn)):
        flour_after_turn[col] = flour_after_turn[col][:len(flour) - front]


# 도우 눌러주기
def stage3():
    global flour

    nrow, ncol = len(flour_after_turn), len(flour_after_turn[0])

    flour_push_temp = [[0] * ncol for _ in range(nrow)]

    # 내 오른쪽과 아래와만 비교. (그럼 겹치는 경우가 없어짐)

    for i in range(nrow):
        for j in range(ncol):
            if flour_after_turn[i][j] == -100:
                continue
            # 오른쪽, 아래쪽 순서
            for next_dx, next_dy in [[i, j + 1], [i + 1, j]]:
                if in_range(next_dx, next_dy, nrow, ncol):
                    if flour_after_turn[next_dx][next_dy] != -100:
                        me = flour_after_turn[i][j]
                        neighbor = flour_after_turn[next_dx][next_dy]

                        d = abs(me - neighbor) // 5

                        if me >= neighbor:
                            flour_push_temp[i][j] -= d
                            flour_push_temp[next_dx][next_dy] += d
                        else:
                            flour_push_temp[i][j] += d
                            flour_push_temp[next_dx][next_dy] -= d

    for i in range(nrow):
        for j in range(ncol):
            flour_push_temp[i][j] += flour_after_turn[i][j]

    flour = []
    for j in range(ncol):
        for i in range(nrow - 1, -1, -1):
            value = flour_push_temp[i][j]
            if value != -100:
                flour.append(value)


# 도우 두 번 접어주기
def stage4():
    global flour, flour_after_turn

    # 한 번 접기
    mid = len(flour) // 2
    first_half = flour[:mid]
    second_half = flour[mid:]
    first_one = [first_half[::-1], second_half]

    # 두 번 접기
    mid = len(second_half) // 2

    to_rotate = []  # 180도 돌리기
    not_to_rotate = []
    for i in range(2):
        tr = first_one[i][:mid]
        ntr = first_one[i][mid:]
        to_rotate.append(tr)
        not_to_rotate.append(ntr)

    to_rotate_update = []
    for tr in to_rotate[::-1]:
        to_rotate_update.append(tr[::-1])

    final = []

    for tru in to_rotate_update:
        final.append(tru)
    for ntr in not_to_rotate:
        final.append(ntr)

    flour = final
    flour_after_turn = final


t = 0
while True:
    stage1()

    stage2()

    stage3()

    stage4()

    stage3()

    t += 1

    if max(flour) - min(flour) <= k:
        break

print(t)