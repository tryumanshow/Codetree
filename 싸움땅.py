from collections import defaultdict

# n: 격자의 수
# m: 플레이어의 수
# k: 라운드 수
n, m, k = [int(x) for x in input().strip().split()]

gun_power = [
    [[int(x)] for x in input().strip().split()] for _ in range(n)
]  # 여러 개의 총을 담으려고 일부러 리스트의 리스트를 선언해둠.

players_info = [
    [int(x) for x in input().strip().split()] for _ in range(m)
]

players_pos_dict = dict()
players_gun_dict = defaultdict(int)
pos_cnt = defaultdict(int)

for idx, pi in enumerate(players_info):
    """
    x, y, d, s
    x: x index
    y: y index
    d: 방향
    s: 초기 능력치
    """
    players_info[idx] = pi[2:]  # 위치 정보는 제외하고 players_pos_dict로 관리
    pos_x, pos_y = [int(x) - 1 for x in pi[:2]]  # 위치 보정
    players_pos_dict[idx] = [pos_x, pos_y]  # 좌표 상의 player_idx - 1로 관리
    pos_cnt[f'{pos_x},{pos_y}'] += 1

dxs = [-1, 0, 1, 0]  # 상, 우, 하, 좌
dys = [0, 1, 0, -1]

opposite_direction = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}

points = [0] * m


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def stage1_1(idx):
    global players_info, players_pos_dict, pos_cnt

    d, s = players_info[idx]
    x, y = players_pos_dict[idx]

    while True:

        dx, dy = dxs[d], dys[d]
        next_dx, next_dy = x + dx, y + dy

        if in_range(next_dx, next_dy):
            players_pos_dict[idx] = [next_dx, next_dy]
            players_info[idx][0] = d  # global?
            pos_cnt[f'{x},{y}'] -= 1
            pos_cnt[f'{next_dx},{next_dy}'] += 1
            return

        d = opposite_direction[d]


def stage2_1(idx, x, y):
    global players_gun_dict

    gun_grid_current = gun_power[x][y]
    guns_sum = sum(gun_grid_current)

    if guns_sum > 0:  # 총이 있는 경우

        player_gun = players_gun_dict[idx]
        gun_max = max(gun_grid_current)

        if player_gun == 0:  # 플레이어에게 총이 없었다는 것.
            players_gun_dict[idx] = gun_max
            gun_power[x][y].remove(gun_max)
        else:
            if gun_max > player_gun:
                players_gun_dict[idx] = gun_max
                gun_power[x][y].remove(gun_max)
                gun_power[x][y].append(player_gun)


def stage2_2_1(idx, x, y):
    global points

    two_players = []
    for i, pos_tmp in players_pos_dict.items():
        if [x, y] == pos_tmp:
            two_players.append(i)

    me = idx
    two_players.remove(me)
    other = two_players[0]

    me_initial = players_info[me][-1]
    other_initial = players_info[other][-1]

    me_gun_power = players_gun_dict[me]
    other_gun_power = players_gun_dict[other]

    me_sum = me_initial + me_gun_power
    other_sum = other_initial + other_gun_power

    score = abs(me_sum - other_sum)
    winner, loser = 0, 0
    if me_sum > other_sum:
        points[me] += score
        winner, loser = me, other
    elif me_sum < other_sum:
        points[other] += score
        winner, loser = other, me
    else:
        if me_initial > other_initial:
            points[me] += score
            winner, loser = me, other
        else:
            points[other] += score
            winner, loser = other, me

    return winner, loser


def stage2_2_2(loser_idx):
    global players_info

    d, s = players_info[loser_idx]
    x, y = players_pos_dict[loser_idx]

    gun_of_loser = players_gun_dict.pop(loser_idx)
    gun_power[x][y].append(gun_of_loser)

    pos_cnt[f'{x},{y}'] -= 1

    while True:

        next_dx, next_dy = x + dxs[d], y + dys[d]
        if (pos_cnt[f'{next_dx},{next_dy}'] >= 1) or (not in_range(next_dx, next_dy)):
            d = (d + 1) % 4

        else:
            pos_cnt[f'{next_dx},{next_dy}'] += 1
            players_info[loser_idx][0] = d
            players_pos_dict[loser_idx] = [next_dx, next_dy]

            stage2_1(loser_idx, next_dx, next_dy)

            return


def stage2_2_3(winner_idx, x, y):
    stage2_1(winner_idx, x, y)


def stage2(idx):

    x, y = players_pos_dict[idx]

    if pos_cnt[f'{x},{y}'] == 1:  # 이동 방향에 플레이어가 없는 경우
        stage2_1(idx, x, y)

    elif pos_cnt[f'{x},{y}'] >= 2:
        winner_idx, loser_idx = stage2_2_1(idx, x, y)
        stage2_2_2(loser_idx)
        stage2_2_3(winner_idx, x, y)


curr = 0
while curr != k:

    for idx in range(m):
        stage1_1(idx)
        stage2(idx)

    curr += 1

points = list(map(lambda x: str(x), points))
points = ' '.join(points)
print(points)