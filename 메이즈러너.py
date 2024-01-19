from collections import defaultdict

N, M, K = [int(x) for x in input().strip().split()]

maze_info = [
    [int(x) for x in input().strip().split()] for _ in range(N)
]

# 특정 participant를 계속 트랙킹 하기 위해 의도적으로 뒤에 [i]를 추가
# False: 이미 움직였는지 아닌지, 나중에 체크하기 위한 용도
participant_info = [
    [int(x) - 1 for x in input().strip().split()] + [i, False] for i in range(M)
]

exit_info = [int(x) - 1 for x in input().strip().split()]
exit_info += [False]

dxs = [-1, 1, 0, 0]  # 상, 하, 좌, 우
dys = [0, 0, -1, 1]

moved_distance_dict = defaultdict(int)
coord_to_rotate = []
index_mapping_dict = dict()


def in_range(x, y):
    return (0 <= x < N) and (0 <= y < N)


def min_distance(x, y):
    return abs(x - exit_info[0]) + abs(y - exit_info[1])


def move_onestep(x, y, idx, *arg):
    distance = 0

    if x == -1:
        return

    for _, (dx, dy) in enumerate(zip(dxs, dys)):
        next_x = x + dx
        next_y = y + dy
        if in_range(next_x, next_y) and maze_info[next_x][next_y] == 0:
            # 출구에 도착했다면.
            if [next_x, next_y] == exit_info[:-1]:
                distance = 1
                participant_info[idx] = [-1, -1, -1, True]  # Dummy
                break
            # 그렇지 않다면
            elif min_distance(next_x, next_y) < min_distance(x, y):
                distance = 1
                participant_info[idx][:-2] = [next_x, next_y]
                break

    moved_distance_dict[idx] += distance


def find_minimum_square():
    global coord_to_rotate

    coord_to_rotate = []

    exit_x, exit_y, _ = exit_info

    # 좌측 최상단으로부터 모든 정사각형을 만들어 봄.
    for square_length in range(2, N):  # 길이가 2인 정사각형부터 탐색.
        for ul_x in range(N + 1 - square_length):  # ul: upper left
            for ul_y in range(N + 1 - square_length):
                br_x = ul_x + square_length  # br: bottom right
                br_y = ul_y + square_length

                # Condition check
                if ul_x <= exit_x < br_x and ul_y <= exit_y < br_y:
                    if any([x for x in participant_info if ul_x <= x[0] < br_x and ul_y <= x[1] < br_y]):
                        coord_to_rotate = [ul_x, ul_y, br_x - 1, br_y - 1]
                        return


def index_mapping():
    global coord_to_rotate, index_mapping_dict

    if len(coord_to_rotate) == 0:
        raise Exception('Strange')

    ul_x, ul_y, br_x, br_y = coord_to_rotate

    for x_idx, i in enumerate(range(ul_x, br_x + 1)):
        x_idx2 = 0
        for j in range(ul_y, br_y + 1):
            index_mapping_dict[f'{i},{j}'] = [ul_x + x_idx2, br_y - x_idx, maze_info[i][j]]  # 원래 값 저장해두기.
            x_idx2 += 1


def rotate():
    global index_mapping_dict, exit_info, coord_to_rotate, participant_info

    for key, value in index_mapping_dict.items():
        o_row, o_col = list(map(lambda x: int(x), key.split(',')))  # o: original
        r_row, r_col, o_value = value  # r: rotated

        if [o_row, o_col] == exit_info[:-1] and not exit_info[-1]:
            exit_info[:-1] = [r_row, r_col]
            exit_info[-1] = True

        for pi in participant_info:
            if pi[:2] == [o_row, o_col] and not pi[-1]:
                participant_info[pi[-2]][:2] = [r_row, r_col]
                participant_info[pi[-2]][-1] = True

        maze_info[r_row][r_col] = max(0, o_value - 1)

    # re-init
    index_mapping_dict = dict()
    for pi in participant_info:
        pi[-1] = False
    exit_info[-1] = False


cnt = 0
while cnt != K:

    for participant in participant_info:
        move_onestep(*participant)

    # early stop
    temp = 0
    for pi in participant_info:
        if pi[0] == -1:
            temp += 1

    if temp == len(participant_info):
        break

    find_minimum_square()
    index_mapping()
    rotate()

    cnt += 1

total_distance = 0
for value in moved_distance_dict.values():
    total_distance += value
print(total_distance)  # 모든 참가자들의 이동 거리 합
print(' '.join(list(map(lambda x: str(x + 1), exit_info[:-1]))))
