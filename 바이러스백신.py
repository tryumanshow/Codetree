from collections import deque
import sys

N, M = [int(x) for x in input().strip().split()]  # N x N의 도시, M개의 병원 고르기

grid = [
    [int(x) for x in input().strip().split()] for _ in range(N)
]

dxs = [-1, 1, 0, 0]  # 상, 하, 좌, 우
dys = [0, 0, -1, 1]

hospital_position = dict()

is_visited = []

cnt = 0  # 병원 개수
num_viruses = 0
for i in range(N):
    for j in range(N):
        if grid[i][j] == 2:  # 병원
            hospital_position[cnt] = [i, j]
            cnt += 1
        elif grid[i][j] == 0:  # 바이러스
            num_viruses += 1

total_hospital = list(range(len(hospital_position)))

combinations = []

MIN_TIME = sys.maxsize


def in_range(x, y):
    return 0 <= x < N and 0 <= y < N


def make_combi(combi_list, temp_cnt):
    global combinations

    if len(combi_list) == M:
        combinations.append(combi_list)
        return

    for i in total_hospital[temp_cnt:]:
        make_combi(combi_list + [i], i + 1)


def init():
    global is_visited, score_board

    is_visited = [
        [False] * N for _ in range(N)
    ]

    score_board = [
        [0] * N for _ in range(N)
    ]


def vaccinate(combi):
    global MIN_TIME, is_visited, score_board

    init()

    q = deque([])

    for cb in combi:
        x, y = hospital_position[cb]
        q.append([x, y, 0])
        is_visited[x][y] = True

    temp_viruses = num_viruses

    if num_viruses == 0:
        MIN_TIME = 0
        return

    while q:

        start, end, score = q.popleft()

        for dx, dy in zip(dxs, dys):
            next_dx, next_dy = start + dx, end + dy
            if in_range(next_dx, next_dy):
                if not is_visited[next_dx][next_dy]:

                    is_visited[next_dx][next_dy] = True
                    if grid[next_dx][next_dy] == 1:  # 벽
                        continue
                    else:
                        if grid[next_dx][next_dy] == 0:  # 바이러스
                            is_visited[next_dx][next_dy] = True
                            temp_viruses -= 1
                            if temp_viruses == 0:
                                q = deque([])
                                score_board[next_dx][next_dy] = score + 1
                                break
                        score_board[next_dx][next_dy] = score + 1
                        q.append([next_dx, next_dy, score + 1])

    if temp_viruses != 0:
        return

    maximum = -1
    for i in range(N):
        for j in range(N):
            if score_board[i][j] != 0:
                maximum = max(maximum, score_board[i][j])

    MIN_TIME = min(MIN_TIME, maximum)


time = 0
make_combi([], 0)  # Backtrack

for combi in combinations:
    vaccinate(combi)
    if MIN_TIME == 0:
        break

if MIN_TIME != sys.maxsize:
    print(MIN_TIME)
else:
    print(-1)