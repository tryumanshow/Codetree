from collections import deque
from heapq import heappush

n, m = [int(x) for x in input().strip().split()]

grid_info = [
    [int(x) for x in input().strip().split()] for _ in range(n)
]


is_visited = []

dxs = [-1, 1, 0, 0]  # 상, 하, 좌, 우
dys = [0, 0, -1, 1]
answer = 0

def init():
    global is_visited

    is_visited = [
        [False] * n for _ in range(n)
    ]


def in_range(x, y):
    return (0 <= x < n) and (0 <= y < n)


def find_group():

    global answer

    heap = []

    # 이제 그 외의 폭탄들에 대해 생각 시작
    init()
    for i in range(n):
        for j in range(n):
            if not is_visited[i][j] and grid_info[i][j] > 0:
                q = deque([[i, j]])
                color = grid_info[i][j]
                cnt = 1
                red_bomb_idx_list = []
                little_heap = []
                heappush(little_heap, (-i, j))
                is_visited[i][j] = True

                while q:
                    x, y = q.popleft()

                    for dx, dy in zip(dxs, dys):
                        next_x = x + dx
                        next_y = y + dy
                        if not in_range(next_x, next_y):
                            continue
                        if not is_visited[next_x][next_y]:
                            next_identity = grid_info[next_x][next_y]
                            if next_identity == -100:
                                is_visited[next_x][next_y] = True
                                continue
                            if next_identity == -1:
                                is_visited[next_x][next_y] = True
                                continue
                            elif next_identity == 0:
                                is_visited[next_x][next_y] = True
                                red_bomb_idx_list.append([next_x, next_y])
                                q.append([next_x, next_y])
                                """
                                  0 1
                                  0 1
                                0 1   과 같은 경우 때문에 queue에 append도 반드시 해주어야 함. 
                                """
                            else:
                                if next_identity == color:
                                    is_visited[next_x][next_y] = True
                                    q.append([next_x, next_y])
                                    heappush(little_heap, (-next_x, next_y))
                                    cnt += 1

                if len(little_heap) >= 1:   # 빨간색을 제외하고라도 적어도 하나는 있어야.
                    cnt_to_add = 0
                    chosen_x, chosen_y = little_heap[0]
                    if len(red_bomb_idx_list) != 0:
                        cnt_to_add += len(red_bomb_idx_list)
                        for red_x, red_y in red_bomb_idx_list:
                            heappush(little_heap, (-int(red_x), red_y))

                if len(little_heap) >= 2:
                    heappush(heap, (-cnt-cnt_to_add, cnt_to_add, chosen_x, chosen_y, little_heap))

                for x, y in red_bomb_idx_list:
                    is_visited[x][y] = False

    answer += heap[0][0] ** 2

    return heap[0][-1]


def renew_grid(to_remove):

    for row, col in to_remove:
        grid_info[-row][col] = -100 # 공백은 -100으로 표현

def gravity():

    global grid_info

    new_grid_info = [
        [-100] * n for _ in range(n)
    ]

    def update(start, end):
        real_info = []
        for i in range(start, end):
            if grid_info[i][j] != -100:
                real_info.append(grid_info[i][j])
        for idx, i in enumerate(range(end - len(real_info), end)):
            new_grid_info[i][j] = real_info[idx]

    for j in range(n):
        black_idx = []
        for i in range(0, n):
            if grid_info[i][j] == -1:
                black_idx.append(i)

        if len(black_idx) == 0:
            update(0, n)

        else:
            for bi in black_idx:
                new_grid_info[bi][j] = -1
            if black_idx[0] != 0:
                black_idx = [-1] + black_idx
            if black_idx[-1] != n:
                black_idx.append(n)

            for front, back in zip(black_idx, black_idx[1:]):
                update(front+1, back)

    grid_info = new_grid_info


def rotate():

    global grid_info

    new_grid_info = [
        [0] * n for _ in range(n)
    ]

    for i in range(n):
        cnt = 0
        for j in range(n):
            new_grid_info[n-1-cnt][i] = grid_info[i][j]
            cnt += 1

    grid_info = new_grid_info


while True:

    try:
        to_remove = find_group()

        renew_grid(to_remove)

        gravity()

        rotate()

        gravity()

    except:
        break

print(answer)