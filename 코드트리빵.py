from heapq import heappush
from collections import deque

n, m = [int(x) for x in input().strip().split()]

grid = [
    [int(x) for x in input().strip().split()] for _ in range(n)
]

store_position = [
    [int(x) - 1 for x in input().strip().split()] for _ in range(m)
]

base_position = []
base_cnt = 0
visited_store_cnt = 0

for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            base_position.append([i, j])
            base_cnt += 1

dxs = [-1, 0, 0, 1]  # 상, 좌, 우, 하
dys = [0, -1, 1, 0]

people_in_grid = dict()

is_visited = [
    [False] * n for _ in range(n)
]  # 베이스와 편의점의 방문 여부를 is_visited를 통해 관리할 것.


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def bfs(start, destination):
    dest_x, dest_y = destination
    if is_visited[dest_x][dest_y]:
        return

    # 이전까지의 방문 정보 + 이번에 BFS를 돌면서의 방문 정보까지 함께 사용하고자 함
    is_visited_for_stage = [
        [False] * n for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):
            if is_visited[i][j]:
                is_visited_for_stage[i][j] = True

    start_x, start_y = start

    q = deque([[start_x, start_y, 0, []]])
    is_visited_for_stage[start_x][start_y] = True

    while q:

        x, y, cnt, idx_list = q.popleft()

        for idx, (dx, dy) in enumerate(zip(dxs, dys)):
            next_dx, next_dy = x + dx, y + dy
            if in_range(next_dx, next_dy):
                if not is_visited_for_stage[next_dx][next_dy]:
                    is_visited_for_stage[next_dx][next_dy] = True
                    cnt_update = cnt + 1
                    if [next_dx, next_dy] == destination:
                        return (cnt_update, start_x, start_y, idx_list + [idx])
                    q.append([next_dx, next_dy, cnt_update, idx_list + [idx]])


def stage1():
    global people_in_grid

    people_in_grid_next = dict()

    for key, value in people_in_grid.items():
        # key: 사람의 index
        # value: 현재 서 있는 위치
        output = bfs(value, store_position[key])
        chosen = output[-1][0]
        people_in_grid_next[key] = [value[0] + dxs[chosen], value[1] + dys[chosen]]

    people_in_grid = people_in_grid_next


def stage2():
    global people_in_grid, is_visited, visited_store_cnt

    temp_grid = dict()

    for key, value in people_in_grid.items():
        dest = store_position[key]
        x, y = value
        if value == dest:
            is_visited[x][y] = True
            visited_store_cnt += 1
            continue
        temp_grid[key] = value

    people_in_grid = temp_grid


def stage3(time):
    global is_visited

    base_heap = []

    # time: 현재 시각이자, time번인 사람이 grid에 들어오기 시작함.
    destination = store_position[time - 1]  # time-1: 인덱스 보정

    for bp in base_position:
        bp_x, bp_y = bp
        if is_visited[bp_x][bp_y]:
            continue
        output = bfs(bp, destination)
        if output is not None:  # 막혀있는 경우 (ex. 가장 우하단에서 출발하는데, 상좌가 막힌 경우)
            heappush(base_heap, output)

    start_base = list(base_heap[0][1:-1])
    start_x, start_y = start_base

    people_in_grid[time - 1] = start_base

    is_visited[start_x][start_y] = True


time = 0
while visited_store_cnt != len(store_position):

    time += 1

    stage1()

    stage2()

    if time <= m:
        stage3(time)

print(time)