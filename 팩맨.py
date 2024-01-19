from heapq import heappush
from collections import defaultdict

MONSTER, TURN = [int(x) for x in input().strip().split()]

PACKMAN_POS = [int(x) - 1 for x in input().strip().split()]

MONSTER_POS = [
    [int(x) - 1 for x in input().strip().split()] for _ in range(MONSTER)
]

PACKMAN_DXS = [-1, 0, 1, 0]  # 상, 좌, 하, 우
PACKMAN_DYS = [0, -1, 0, 1]

MONSTER_DXS = [-1, -1, 0, 1, 1, 1, 0, -1]
MONSTER_DYS = [0, -1, -1, -1, 0, 1, 1, 1]

EGGS_POSITION = []
DEAD_POSITION = dict()

POS_TEMP = dict()


def in_range(x, y):
    return (0 <= x < 4) and (0 <= y < 4)


def monster_copy():
    global EGGS_POSITION

    EGGS_POSITION = []
    for pp in MONSTER_POS:
        EGGS_POSITION.append(pp)


def monster_move():
    global MONSTER_POS, POS_TEMP

    # initalize
    NEXT_MONSTER_POS = []
    POS_TEMP = defaultdict(int)

    for x, y, direction in MONSTER_POS:
        cnt = 0
        flag = False
        while cnt < 8:
            cnt += 1
            next_x = x + MONSTER_DXS[direction]
            next_y = y + MONSTER_DYS[direction]
            if not in_range(next_x, next_y):
                direction = (direction + 1) % 8  # 반시계 방향 45도 회전
                continue
            else:
                if f'{next_x},{next_y}' in DEAD_POSITION or [next_x, next_y] == PACKMAN_POS:
                    direction = (direction + 1) % 8
                    continue
                else:
                    NEXT_MONSTER_POS.append([next_x, next_y, direction])
                    POS_TEMP[f'{next_x},{next_y}'] += 1
                    flag = True
                    break
        if cnt == 8 and not flag:
            NEXT_MONSTER_POS.append([x, y, direction])
            POS_TEMP[f'{x},{y}'] += 1

    MONSTER_POS = NEXT_MONSTER_POS


def packman_move():
    global POS_TEMP, PACKMAN_POS, DEAD_POSITION, MONSTER_POS

    trajectory = []

    max_cnt = -100

    # 1st movement
    for idx1, (dx, dy) in enumerate(zip(PACKMAN_DXS, PACKMAN_DYS)):
        next_dx1 = PACKMAN_POS[0] + dx
        next_dy1 = PACKMAN_POS[1] + dy
        if not in_range(next_dx1, next_dy1):
            continue
        cnt1 = POS_TEMP[f'{next_dx1},{next_dy1}']

        # 2nd movement
        for idx2, (dx, dy) in enumerate(zip(PACKMAN_DXS, PACKMAN_DYS)):
            next_dx2 = next_dx1 + dx
            next_dy2 = next_dy1 + dy
            if not in_range(next_dx2, next_dy2):
                continue
            cnt2 = cnt1 + POS_TEMP[f'{next_dx2},{next_dy2}']
            visit_temp = [f'{next_dx1},{next_dy1}', f'{next_dx2},{next_dy2}']

            # 3rd movement
            for idx3, (dx, dy) in enumerate(zip(PACKMAN_DXS, PACKMAN_DYS)):
                next_dx3 = next_dx2 + dx
                next_dy3 = next_dy2 + dy
                if not in_range(next_dx3, next_dy3):
                    continue
                cnt3 = cnt2 if f'{next_dx3},{next_dy3}' in visit_temp else cnt2 + POS_TEMP[f'{next_dx3},{next_dy3}']

                if cnt3 > max_cnt:
                    max_cnt = cnt3
                    trajectory = [(idx1, idx2, idx3, next_dx3, next_dy3, [[next_dx1, next_dy1],
                                                                          [next_dx2, next_dy2],
                                                                          [next_dx3, next_dy3]])]
                elif cnt3 == max_cnt:
                    heappush(trajectory, (idx1, idx2, idx3, next_dx3, next_dy3, [[next_dx1, next_dy1],
                                                                                 [next_dx2, next_dy2],
                                                                                 [next_dx3, next_dy3]]))

    last_packman = trajectory[0]
    PACKMAN_POS = list(last_packman[-3:-1])
    packman_trajectory = last_packman[-1]

    # 시체 남기기
    for pt_x, pt_y in packman_trajectory:
        if POS_TEMP[f'{pt_x},{pt_y}'] != 0:
            DEAD_POSITION[f'{pt_x},{pt_y}'] = 3  # 어차피 두 마리 이상 존재해도 존재 자체가 중요해서 상관 없음.

    MONSTER_POS = [x for x in MONSTER_POS if [x[0], x[1]] not in packman_trajectory]


def dead_remove():
    global DEAD_POSITION

    DEAD_COPY = dict()

    for key, value in DEAD_POSITION.items():
        next_v = value - 1
        if next_v > 0:
            DEAD_COPY[key] = next_v

    DEAD_POSITION = DEAD_COPY


def clone_complete():
    MONSTER_POS.extend(EGGS_POSITION)


cnt = 0
while cnt < TURN:
    monster_copy()

    monster_move()

    packman_move()

    dead_remove()

    clone_complete()

    cnt += 1

print(len(MONSTER_POS))