from collections import defaultdict


n, m, k = [int(x) for x in input().strip().split()]

grid = [
    [int(x) for x in input().strip().split()] for _ in range(n)
]

is_visited = [
    [False] * n for _ in range(n)
]

score = 0

groups = defaultdict(list)
groups_with_four = defaultdict(bool)

dxs = [-1, 0, 1, 0]    # 상, 우, 하, 좌
dys = [0, 1, 0, -1]


def within_board(x, y):
    return (0 <= x < n) and (0 <= y < n)


def dfs(key, value):
    start_x, start_y = value
    four_flag = False

    for dx, dy in zip(dxs, dys):
        next_dx = start_x + dx
        next_dy = start_y + dy
        if within_board(next_dx, next_dy):
            if not is_visited[next_dx][next_dy]:
                if grid[next_dx][next_dy] not in [0, 1, 4]:
                    if len(groups[key]) == 1 and grid[next_dx][next_dy] != 2:
                        continue
                    if grid[next_dx][next_dy] == 2:
                        is_visited[next_dx][next_dy] = True
                        groups[key].append([next_dx, next_dy])
                        dfs(key, [next_dx, next_dy])
                    else:  # 3
                        if len(groups[key]) >= 2:
                            is_visited[next_dx][next_dy] = True
                            groups[key].append([next_dx, next_dy])
                            return
                elif grid[next_dx][next_dy] == 4:
                    if not four_flag:
                        groups_with_four[key] = True
                        four_flag = True


def initialize():
    cnt = 1
    for i in range(n):
        for j in range(n):
            number = grid[i][j]
            if number == 1:
                groups[cnt].append([i, j])
                groups_with_four[cnt] = False
                is_visited[i][j] = True
                cnt += 1

    # 그룹별 사람 찾기
    for key, value in groups.items():
        dfs(key, value[0])


def move_one_point():
    for key, value in groups.items():
        header = value[0]
        for dx, dy in zip(dxs, dys):
            next_dx, next_dy = header[0] + dx, header[1] + dy
            if within_board(next_dx, next_dy):

                # 경로 안이 사람이 없는 칸이 존재하는 경우
                if groups_with_four[key]:
                    if grid[next_dx][next_dy] == 4:
                        # 좌표 업데이트
                        grid[next_dx][next_dy] = 1
                        for prev_v, next_v in zip(value, value[1:]):
                            grid[prev_v[0]][prev_v[1]] = grid[next_v[0]][next_v[1]]
                        # + value 업데이트
                        coord_to_four = groups[key].pop(-1)
                        grid[coord_to_four[0]][coord_to_four[1]] = 4
                        groups[key].insert(0, [next_dx, next_dy])

                # 경로 안이 사람으로 꽉 차있는 경우
                else:
                    if grid[next_dx][next_dy] == 3:
                        value = groups[key]
                        men_idx = [1] + [2] * (len(value) - 2) + [3]
                        for idx, (v0, v1) in enumerate([value[-1]] + value[:-1]):
                            grid[v0][v1] = men_idx[idx]
                        grid[header[0]][header[1]] = 2
                        groups[key] = [groups[key][-1]] + groups[key][:-1]


def throw_a_ball(idx):
    q, r = divmod(idx, n)
    candidates = defaultdict(list)

    MAX = 21  # 문제 조건
    MIN = -MAX
    key_update, index_value = None, None

    if q % 4 == 0:  # →
        for key, value in groups.items():
            for v in value:
                if v[0] == r:  # x축은 같아야.
                    if v[1] < MAX:  # y축에서 가장 작은 것.
                        MAX = v[1]
                        index_value = v
                        key_update = key

    elif q % 4 == 1:  # ↑
        for key, value in groups.items():
            for v in value:
                if v[1] == r:  # y축은 같아야.
                    if v[0] > MIN:  # x축에서 제일 큰 것
                        MIN = v[0]
                        index_value = v
                        key_update = key

    elif q % 4 == 2:  # ←
        for key, value in groups.items():
            for v in value:
                if v[0] == n-r-1:  # x축은 같아야.
                    if v[1] > MIN:  # y축에서 제일 큰 것
                        MIN = v[1]
                        index_value = v
                        key_update = key

    else:  # ↓
        for key, value in groups.items():
            for v in value:
                if v[1] == n-r-1:  # y축은 같아야.
                    if v[0] < MAX:  # x축에서 제일 작은 것.
                        MAX = v[0]
                        index_value = v
                        key_update = key

    if index_value is not None:
        candidates[key_update] = index_value

    return candidates


def calculate_and_change_direction(candidates):

    if len(candidates) == 0:
        return

    global score

    key = list(candidates.keys())[0]
    men = groups[key] # 머리순서부터 고려
    men_prev = men
    idx = [i for i, x in enumerate(men) if x == candidates[key]][0]

    score += (idx+1)**2

    men = men[::-1]
    groups[key] = men

    values = list(map(lambda x: grid[x[0]][x[1]], men))

    for idx, mp in enumerate(men_prev):
        v = values[idx]
        grid[mp[0]][mp[1]] = v

initialize()

for idx in range(k):

    move_one_point()

    candidates = throw_a_ball(idx)

    calculate_and_change_direction(candidates)

print(score)