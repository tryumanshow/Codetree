from heapq import heapify, heappush, heappop
from collections import defaultdict

num_order = [int(x) for x in input().strip().split()][0]

info_line = [
    [int(x) for x in input().strip().split()] for _ in range(num_order)
]

first_line = info_line[0]
N, M, P = first_line[1:4]

temp_list = []
info_list = []
pid_list = []
rabbit_jump_cnt = defaultdict(int)
rabbit_current_x = defaultdict(int)
rabbit_current_y = defaultdict(int)
rabbit_score = defaultdict(int)

max_score = 0


def in_range(x, y):
    return (0 <= x < N) and (0 <= y < M)


#######
# 100 #
#######
def get_ready_for_race(info):
    global info_list, rabbit_jump_cnt

    # 토끼 별로 나누기
    temp_list = []
    for i in range(len(info) // 2):
        temp_list.append(info[2 * i: 2 * (i + 1)])

    # 100에서 이미 heap을 만들어 줆.
    for pid, d in temp_list:
        heappush(info_list, [rabbit_jump_cnt[pid],
                             rabbit_current_x[pid] + rabbit_current_y[pid],
                             rabbit_current_x[pid],
                             rabbit_current_y[pid],
                             pid,
                             d])  # d는 임의로 넣어준 것 (우선순위 판단에는 어차피 지장 x)
        pid_list.append(pid)
        rabbit_score[pid] = 0


def up_direction(x, y, rabbit_d):
    rabbit_d %= (2 * (N - 1))  # 원 상태로 돌아오는 이동 거리
    if rabbit_d > x:  # 아래쪽으로 방향을 틀어야 하는 경우
        rabbit_d -= (x + 1)
        x_cp = 1
        if rabbit_d > N - 1 - x_cp:  # 아래쪽에서 다시 위쪽으로
            rabbit_d -= (N - 1 - x_cp + 1)
            x_cp = N - 1 - 1 - rabbit_d
        else:
            x_cp += rabbit_d
    else:  # 위쪽으로만 가도 되는 경우
        x_cp = x - rabbit_d
    return x_cp, y


def down_direction(x, y, rabbit_d):
    rabbit_d %= (2 * (N - 1))
    limit = N - 1
    if rabbit_d > (limit - x):  # 위쪽으로 방향을 틀어야 하는 경우
        rabbit_d -= (limit - x + 1)
        x_cp = limit - 1
        if rabbit_d > x_cp:  # 다시 아래쪽으로 방향을 틀어야 하는 경우
            rabbit_d -= (x_cp + 1)
            x_cp = 1 + rabbit_d
        else:
            x_cp -= rabbit_d
    else:
        x_cp = x + rabbit_d
    return x_cp, y


def left_direction(x, y, rabbit_d):
    rabbit_d %= (2 * (M - 1))
    if rabbit_d > y:  # 오른쪽으로 방향을 틀어야 하는 경우
        rabbit_d -= (y + 1)
        y_cp = 1
        if rabbit_d > M - 1 - y_cp:  # 다시 왼쪽으로 방향을 틀어야 하는 경우
            rabbit_d -= (M - 1 - y_cp + 1)
            y_cp = M - 1 - 1 - rabbit_d
        else:
            y_cp += rabbit_d
    else:
        y_cp = y - rabbit_d
    return x, y_cp


def right_direction(x, y, rabbit_d):
    rabbit_d %= (2 * (M - 1))
    limit = M - 1
    if rabbit_d > (limit - y):  # 왼쪽으로 방향을 틀어야 하는 경우
        rabbit_d -= (limit - y + 1)
        y_cp = limit - 1
        if rabbit_d > y_cp:  # 다시 오른쪽으로 방향을 틀어야 하는 경우
            rabbit_d -= (y_cp + 1)
            y_cp = 1 + rabbit_d
        else:
            y_cp -= rabbit_d
    else:
        y_cp = y + rabbit_d
    return x, y_cp


#########
# 200-2 #
#########
def priority_queue_for_direction(rabbit_pid, rabbit_d):
    x, y = rabbit_current_x[rabbit_pid], rabbit_current_y[rabbit_pid]

    dir_heap = []

    for idx in range(4):
        # 상
        if idx == 0:
            x_cp, y_cp = up_direction(x, y, rabbit_d)
        elif idx == 1:
            x_cp, y_cp = down_direction(x, y, rabbit_d)
        elif idx == 2:
            x_cp, y_cp = left_direction(x, y, rabbit_d)
        else:
            x_cp, y_cp = right_direction(x, y, rabbit_d)

        heappush(dir_heap, [-(x_cp + y_cp), -x_cp, -y_cp])

    dir_selected = dir_heap[0]
    dir_row, dir_col = dir_selected[-2:]
    dir_row, dir_col = -dir_row, -dir_col
    score = dir_row + dir_col

    # 이동시킴
    rabbit_current_x[rabbit_pid] = dir_row
    rabbit_current_y[rabbit_pid] = dir_col
    rabbit_jump_cnt[rabbit_pid] += 1

    return score


# 200 main
def race_get_started(info):
    global pid_list, max_score, rabbit_score

    K, S = info

    pid_appear = set()

    scores_to_add = 0

    for _ in range(K):
        # 우선순위 가장 높은 토끼 pid & d
        popped_rabbit = heappop(info_list)
        rabbit_pid, rabbit_d = popped_rabbit[-2:]
        pid_appear.add(rabbit_pid)

        score = priority_queue_for_direction(rabbit_pid, rabbit_d)

        jump_cnt = rabbit_jump_cnt[rabbit_pid]
        x = rabbit_current_x[rabbit_pid]
        y = rabbit_current_y[rabbit_pid]

        scores_to_add += (score + 2)
        rabbit_score[rabbit_pid] -= (score + 2)
        heappush(info_list, [jump_cnt, x + y, x, y, rabbit_pid, rabbit_d])

    rabbit_score = {k: v + scores_to_add for k, v in rabbit_score.items()}

    new_heap = []
    heapify(new_heap)

    for il in info_list:
        if il[-2] in pid_appear:
            selected = il[1:]
            selected = list(map(lambda x: -x, selected))
            heappush(new_heap, selected)

    pid = -new_heap[0][-2]
    rabbit_score[pid] += S

    max_score = max(max_score, max(list(rabbit_score.values())))


# 300
def multiply_L(info):
    pid_t, L = info
    for idx, il in enumerate(info_list):
        if il[-2] == pid_t:
            info_list[idx][-1] *= L
            break


def get_max_score():
    print(max_score)


for il in info_line:

    identity = il[0]

    if identity == 100:
        get_ready_for_race(il[4:])

    elif identity == 200:
        race_get_started(il[1:])

    elif identity == 300:
        multiply_L(il[1:])

    else:
        get_max_score()
