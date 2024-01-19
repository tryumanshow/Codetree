from collections import deque

n, q = [int(x) for x in input().strip().split()]

ices = [
    [int(x) for x in input().strip().split()] for _ in range(2 ** n)
]

empty_ices = [
    [0] * 2**n for _ in range(2**n)
]
rotation_level = [int(x) for x in input().strip().split()]

dxs = [-1, 1, 0, 0]
dys = [0, 0, -1, 1]

melt_list = []


def in_range(x, y):
    return 0 <= x < 2 ** n and 0 <= y < 2 ** n


def init():
    global empty_ices
    empty_ices = [
        [0] * 2 ** n for _ in range(2 ** n)
    ]


def select_rotation_index(idx):
    index = list(range(2 ** n + 1))[0::2 ** idx]
    return index


def rotate_instance(row_list, col_list):

    row_middle = (row_list[-1] - row_list[0]) // 2
    col_middle = (col_list[-1] - col_list[0]) // 2

    four_cases = []
    for row_start, row_end in zip(row_list, row_list[1:]):
        for col_start, col_end in zip(col_list, col_list[1:]):
            four_cases.append([row_start, row_end, col_start, col_end])

    for idx, (r1, r2, c1, c2) in enumerate(four_cases):
        for r in range(r1, r2):
            for c in range(c1, c2):
                if idx == 0:    # 1사분면 from 3사분면
                    empty_ices[r][c] = ices[r + row_middle][c]
                elif idx == 1:  # 2사분면 from 1사분면
                    empty_ices[r][c] = ices[r][c - col_middle]
                elif idx == 2:  # 3사분면 from 4사분면
                    empty_ices[r][c] = ices[r][c + col_middle]
                else:   # 4사분면 from 2사분면
                    empty_ices[r][c] = ices[r - row_middle][c]


def rotate(row1, row2, col1, col2):
    if row1 > row2:
        row1, row2 = row2, row1
    if col1 > col2:
        col1, col2 = col2, col1

    row_mid = (row2 + row1) // 2
    col_mid = (col2 + col1) // 2

    row_list = [row1, row_mid, row2]
    col_list = [col1, col_mid, col2]

    rotate_instance(row_list, col_list)


def actual_rotate(index):
    global ices

    for row1, row2 in zip(index, index[1:]):
        for col1, col2 in zip(index, index[1:]):
            rotate(row1, row2, col1, col2)

    ices = empty_ices


def judge_melting():
    temp = [
        [0] * 2 ** n for _ in range(2 ** n)
    ]

    for i in range(2 ** n):
        for j in range(2 ** n):

            for dx, dy in zip(dxs, dys):
                next_dx, next_dy = i + dx, j + dy
                if in_range(next_dx, next_dy):
                    if ices[next_dx][next_dy] > 0:
                        temp[i][j] += 1

    for i in range(2 ** n):
        for j in range(2 ** n):
            if temp[i][j] < 3:
                ices[i][j] = max(0, ices[i][j] - 1)


def find_cluster():
    total_iceberg = 0
    maximum = 0

    is_visited = [
        [False] * (2 ** n) for _ in range(2 ** n)
    ]

    for i in range(2 ** n):
        for j in range(2 ** n):

            if ices[i][j] == 0:
                is_visited[i][j] = True
                continue

            if is_visited[i][j]:
                continue

            q = deque([[i, j]])
            is_visited[i][j] = True
            total_iceberg += ices[i][j]
            cluster = 1

            while q:

                x, y = q.popleft()

                for dx, dy in zip(dxs, dys):
                    next_dx, next_dy = x + dx, y + dy
                    if in_range(next_dx, next_dy):
                        if not is_visited[next_dx][next_dy]:
                            if ices[next_dx][next_dy] == 0:
                                is_visited[next_dx][next_dy] = True
                            else:
                                total_iceberg += ices[next_dx][next_dy]
                                cluster += 1
                                is_visited[next_dx][next_dy] = True
                                q.append([next_dx, next_dy])

            maximum = max(maximum, cluster)

    return total_iceberg, maximum


for rl in rotation_level:

    init()

    index = select_rotation_index(rl)

    actual_rotate(index)

    init()

    judge_melting()

total_iceberg, maximum = find_cluster()

print(total_iceberg)
print(maximum)