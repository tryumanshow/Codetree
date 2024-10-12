from collections import defaultdict

n = int(input().strip())

grid = [
    [int(x) for x in input().strip().split(' ')] for _ in range(n)
]

grid_temp = [
    [0] * n for _ in range(n)
]

score = 0

is_visited = [
    [False] * n for _ in range(n)
]

groups = [
    [0] * n for _ in range(n)
]
groups_to_value = dict()
groups_cnt = defaultdict(int)

dxs = [-1, 0, 1, 0]  # 상, 우, 하, 좌
dys = [0, 1, 0, -1]


def in_bound(x, y):
    return (0 <= x < n) and (0 <= y < n)


def init_info():
    global is_visited, grid_temp
    is_visited = [
        [False] * n for _ in range(n)
    ]


def dfs(i, j, group_num):
    value = grid[i][j]
    for dx, dy in zip(dxs, dys):
        next_dx = i + dx
        next_dy = j + dy
        if in_bound(next_dx, next_dy):
            if value == grid[next_dx][next_dy]:
                if not is_visited[next_dx][next_dy]:
                    groups_cnt[group_num] += 1
                    is_visited[next_dx][next_dy] = True
                    groups[next_dx][next_dy] = group_num
                    dfs(next_dx, next_dy, group_num)


def make_group():
    init_info()

    global group_num, groups_to_value, groups_cnt

    group_num = 1
    for i in range(n):  # row
        for j in range(n):  # col
            if not is_visited[i][j]:  # Group의 그 어느 시작점이든 괜찮음.
                is_visited[i][j] = True
                groups[i][j] = group_num
                groups_cnt[group_num] += 1
                groups_to_value[group_num] = grid[i][j]
                dfs(i, j, group_num)
                group_num += 1


def calculate_score():
    global score

    init_info()

    neighbor_dict = defaultdict(int)

    for i in range(n):
        for j in range(n):
            if not is_visited[i][j]:
                group = groups[i][j]
                for dx, dy in zip(dxs, dys):
                    next_dx = i + dx
                    next_dy = j + dy
                    if in_bound(next_dx, next_dy):
                        next_group = groups[next_dx][next_dy]
                        if next_group > group:
                            neighbor_dict[(group, next_group)] += 1
                is_visited[i][j] = True

    for key, value in neighbor_dict.items():
        key_a, key_b = key
        space_a = groups_cnt[key_a]
        space_b = groups_cnt[key_b]
        score += (space_a + space_b) * groups_to_value[key_a] * groups_to_value[key_b] * value


def rotate_grim():
    def rotate_grim_instance(ul_x, ul_y):  # ul : upper left, br: bottom right

        for i in range(n // 2):
            for j in range(n // 2):
                grid_temp[ul_x + j][ul_y + (n // 2) - i - 1] = grid[ul_x + i][ul_y + j]

    half = n // 2
    rotate_list = [
        [0, 0],  # [좌상단 row, 좌상단 col]
        [0, half + 1],
        [half + 1, 0],
        [half + 1, half + 1]
    ]

    for rl in rotate_list:
        rotate_grim_instance(*rl)


def rotate_shipja():
    global grid

    coord_list = []
    for i in range(n):
        coord_list.append([n // 2, i])
        coord_list.append([i, n // 2])

    coord_list.remove([n // 2, n // 2])

    for x, y in coord_list:
        grid_temp[n - 1 - y][x] = grid[x][y]

    grid = grid_temp


def re_init():
    global grid_temp, groups_to_value, groups_cnt
    grid_temp = [
        [0] * n for _ in range(n)
    ]
    groups_to_value = dict()
    groups_cnt = defaultdict(int)


for _ in range(4):
    make_group()

    calculate_score()

    rotate_grim()

    rotate_shipja()

    re_init()

print(score)