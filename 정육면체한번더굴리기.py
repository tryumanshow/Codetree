from collections import deque

n, m = [int(x) for x in input().strip().split()]

grid = [
    [int(x) for x in input().strip().split()] for _ in range(n)
]

# 인접한 숫자들을 알기 위함
dxs1 = [-1, 1, 0, 0]  # 상, 하, 좌, 우
dys1 = [0, 0, -1, 1]

# 주사위 방향을 결정하기 위함
dxs2 = [0, 1, 0, -1]  # 우, 하, 좌, 상
dys2 = [1, 0, -1, 0]

position = [0, 0, 0]  # 주사위가 출발하는 지점 x, y, 방향
jusawhi = [1, 2, 3]  # 항상 위, 정면, 우측 정보를 담아서 진행

jusawhi_num_opposite = {
    1: 6,
    2: 5,
    3: 4,
    4: 3,
    5: 2,
    6: 1
}

jusawhi_dir_opposite = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}

answer = 0


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def jusawhi_after_roll(direction):
    global jusawhi

    up, front, right = jusawhi

    if direction == 0:  # 오른쪽
        jusawhi = [jusawhi_num_opposite[right], front, up]

    elif direction == 1:  # 아래쪽
        jusawhi = [jusawhi_num_opposite[front], up, right]

    elif direction == 2:  # 왼쪽
        jusawhi = [right, front, jusawhi_num_opposite[up]]

    else:  # 위쪽
        jusawhi = [front, jusawhi_num_opposite[up], right]


def jusawhi_operation():
    global position

    x, y, direction = position

    while True:  # 반드시 두 번 안에 끝나야 함.
        next_x, next_y = x + dxs2[direction], y + dys2[direction]
        if in_range(next_x, next_y):
            position = [next_x, next_y, direction]
            break
        else:
            direction = jusawhi_dir_opposite[direction]

    # After update
    x, y, direction = position

    jusawhi_after_roll(direction)

    bottom = jusawhi_num_opposite[jusawhi[0]]

    grid_num = grid[next_x][next_y]

    if bottom > grid_num:
        position[-1] = (direction + 1) % 4
    elif bottom < grid_num:
        position[-1] = (direction - 1) % 4
    else:
        pass


def scoring():
    global answer

    x, y, _ = position
    grid_num = grid[x][y]

    is_visited = [
        [False] * n for _ in range(n)
    ]

    is_visited[x][y] = True
    cnt = grid_num

    q = deque([[x, y]])

    while q:
        x, y = q.popleft()

        for dx, dy in zip(dxs1, dys1):
            next_dx, next_dy = x + dx, y + dy
            if in_range(next_dx, next_dy):
                if not is_visited[next_dx][next_dy]:
                    if grid[next_dx][next_dy] == grid_num:
                        is_visited[next_dx][next_dy] = True
                        cnt += grid_num
                        q.append([next_dx, next_dy])

    answer += cnt


def play():
    jusawhi_operation()

    scoring()


rolling = 0
while rolling < m:
    play()

    rolling += 1

print(answer)