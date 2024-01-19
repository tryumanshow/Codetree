import sys
from heapq import heapify, heappush, heappop
from collections import deque
from itertools import chain

N, M, K = [int(x) for x in input().strip().split(' ')]

grid = [
    [int(x) for x in input().strip().split(' ')] for _ in range(N)
]

attack_time = [
    [0] * M for _ in range(N)
]

attack_defense_idx = [[], []]

# 우 / 하 / 좌 / 상
dxs = [0, 1, 0, -1]
dys = [1, 0, -1, 0]

p_dxs = [-1, -1, -1, 0, 0, 1, 1, 1]
p_dys = [-1, 0, 1, -1, 1, -1, 0, 1]

is_visited = [
    [False] * M for _ in range(N)
]

back_x = [
    [0] * M for _ in range(N)
]  # 지나온 길에서 바로 이전의 좌표를 기록할 것.

back_y = [
    [0] * M for _ in range(N)
]

recovery = [
    [1] * M for _ in range(N)
]


def choose_object(identity='weakest'):
    heap = []
    heapify(heap)

    for i in range(N):
        for j in range(M):
            power = grid[i][j]
            if power != 0:
                if identity == 'weakest':
                    item = (power, -attack_time[i][j], -(i + j), -j, i, j)  # i, j는 임의대로 넣음.
                    heappush(heap, item)
                else:
                    item = (-power, attack_time[i][j], i + j, j, i, j)
                    heappush(heap, item)

    info = heappop(heap)
    i, j = info[-2:]

    del heap

    if identity == 'weakest':
        attack_defense_idx[0] = [i, j]
    else:
        attack_defense_idx[1] = [i, j]
        weak_i, weak_j = attack_defense_idx[0]
        grid[weak_i][weak_j] += (N + M)  # 공격자 선정 시 (weakest) 먼저 더하면 값이 변해서, 의사결정에 영향을주게 되므로.


def consider_broken():
    for i in range(N):
        for j in range(M):
            if grid[i][j] == 0:
                recovery[i][j] -= 1


def is_razor_possible():  # BFS

    x, y = attack_defense_idx[0]

    q = deque([[x, y]])
    is_visited[x][y] = True

    while q:
        x, y = q.popleft()

        for dx, dy in zip(dxs, dys):
            next_x, next_y = x + dx, y + dy
            next_x = (next_x + N) % N
            next_y = (next_y + M) % M
            if grid[next_x][next_y] != 0:
                if not is_visited[next_x][next_y]:
                    is_visited[next_x][next_y] = True
                    back_x[next_x][next_y] = x
                    back_y[next_x][next_y] = y
                    if [next_x, next_y] == attack_defense_idx[1]:
                        return True
                    q.append([next_x, next_y])

    return False


def attack_directly(time):
    first_x, first_y = attack_defense_idx[0]
    last_x, last_y = attack_defense_idx[1]
    damage = grid[first_x][first_y]
    grid[last_x][last_y] -= damage

    if grid[last_x][last_y] < 0:
        grid[last_x][last_y] = 0

    recovery[first_x][first_y] -= 1
    recovery[last_x][last_y] -= 1

    attack_time[first_x][first_y] = time + 1

    return last_x, last_y, damage


def do_razor_attack(time):
    next_x, next_y, damage = attack_directly(time)

    while True:

        prev_x = back_x[next_x][next_y]
        prev_y = back_y[next_x][next_y]

        if [prev_x, prev_y] == attack_defense_idx[0]:
            break

        recovery[prev_x][prev_y] -= 1

        grid[prev_x][prev_y] -= damage // 2

        if grid[prev_x][prev_y] < 0:  # 포탑 부서짐
            grid[prev_x][prev_y] = 0

        next_x, next_y = prev_x, prev_y


def do_potab_attack(time):
    next_x, next_y, damage = attack_directly(time)

    for dx, dy in zip(p_dxs, p_dys):
        neighbor_dx, neighbor_dy = next_x + dx, next_y + dy
        neighbor_dx = (neighbor_dx + N) % N
        neighbor_dy = (neighbor_dy + M) % M

        if grid[neighbor_dx][neighbor_dy] != 0:
            if [neighbor_dx, neighbor_dy] != attack_defense_idx[0]:
                grid[neighbor_dx][neighbor_dy] -= damage // 2
                if grid[neighbor_dx][neighbor_dy] < 0:
                    grid[neighbor_dx][neighbor_dy] = 0
                recovery[neighbor_dx][neighbor_dy] -= 1  # 공격과 유관


def potab_repair():
    for i in range(N):
        for j in range(M):
            grid[i][j] += recovery[i][j]


def init():
    attack_defense_idx[0] = []
    attack_defense_idx[1] = []

    for i in range(N):
        for j in range(M):
            recovery[i][j] = 1
            back_x[i][j] = 0
            back_y[i][j] = 0
            is_visited[i][j] = False


def quit_condition():
    grid_cat = list(chain(*grid))
    grid_cat = [x for x in grid_cat if x != 0]
    return len(grid_cat) == 1


turn = 0

while turn != K:

    init()

    # 공격자 선택
    choose_object()

    # 피공격자 선택
    choose_object('strongest')

    # 이미 부서져있는 애들은 다시 더하지 않도록 전처리
    consider_broken()

    # 레이저 공격 가능 여부 판단
    if is_razor_possible():
        do_razor_attack(turn)
    else:
        do_potab_attack(turn)

    potab_repair()

    if quit_condition():
        break

    turn += 1

result = list(chain(*grid))
print(max(result))