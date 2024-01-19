q = int(input().strip())

orders = [
    [int(x) for x in input().strip().split(' ')] for _ in range(q)
]

first_order = orders[0]
n, m = first_order[1:3]  # n개의 선물, m개의 벨트 ( 12개의 선물, 3개의 벨트 )
box_per_belt = n // m  # 벨트당 4개의 상자

# 벨트별로 head, tail 표기
heads = [0] * m
tails = [0] * m

ids_to_weights = dict()  # { box_id: weights , box_id: weights , ... }
box_ids_to_belt = dict()  # { box_id: belt number , box_id: belt number , ... }

# 이중연결리스트의 연결관계 포현 위한 딕셔너리
boxes_prev = {}
boxes_next = {}

belt_broken = [False] * m


# 100: 공장설립
def factory_establish(info):
    real_info = info[2:]
    ids = real_info[: len(real_info) // 2]
    weights = real_info[len(real_info) // 2:]

    assert len(ids) == len(weights), 'Length should be same.'

    for idx, (id_, weight_) in enumerate(zip(ids, weights)):
        ids_to_weights[id_] = weight_

        # 벨트마다 id를 순서대로 추가
        q, r = divmod(idx, box_per_belt)  # box_per_belt = n // m
        box_ids_to_belt[id_] = q + 1  # 박스번호 : 벨트번호 (인덱스 + 1)

        # 맨 앞
        if r == 0:
            heads[q] = id_
            # 맨 뒤 // elif가 아닌 if인 이유: head이자 tail일 수 있기 때문. (벨트 당 박스가 하나 밖에 없을 경우에.)
        if r == box_per_belt - 1:
            tails[q] = id_
            continue

        # 이를 통해, 굳이 box 별로 리스트를 소유할 필요가 없어짐. => 어떻게든 단순연결리스트를 없애는 게 이 문제의 핵심.
        next_id = ids[idx + 1]
        boxes_prev[next_id] = id_
        boxes_next[id_] = next_id


# 200: 물건 하차
def drop_boxes(info):
    w_max = info[0]

    weight_sum = 0

    # 1번부터 m번까지의 벨트
    for belt_num in range(m):

        first_box_id = heads[belt_num]
        last_box_id = tails[belt_num]

        # 벨트에 박스가 하나도 없을 경우
        if first_box_id == -1:
            continue

        first_box_weight = ids_to_weights[first_box_id]

        # 벨트에 하나 밖에 남아있지 않을 경우
        if first_box_id == last_box_id:
            if first_box_weight <= w_max:
                weight_sum += first_box_weight
                del box_ids_to_belt[first_box_id]
                heads[belt_num] = -1
                tails[belt_num] = -1
            continue

        # 하차 후 한 칸 씩 앞으로 내릴 상자들이 남아있을 경우
        next_box_id = boxes_next[first_box_id]
        head, tail = first_box_id, last_box_id

        # 하차를 하는 경우
        if first_box_weight <= w_max:
            weight_sum += first_box_weight
            heads[belt_num] = next_box_id
            del boxes_next[first_box_id]
            del boxes_prev[next_box_id]
            del box_ids_to_belt[first_box_id]

        # 뒤로 보내는 경우
        else:
            heads[belt_num] = next_box_id
            del boxes_prev[next_box_id]
            del boxes_next[first_box_id]
            boxes_prev[first_box_id] = tail
            boxes_next[tail] = first_box_id
            tails[belt_num] = first_box_id

    print(weight_sum)


# 300: 물건 제거
def remove_boxes(info):
    global box_ids_to_belt

    r_id = info[0]

    try:  # 벨트에 물건이 있는 경우
        belt_num = box_ids_to_belt[r_id] - 1

        head = heads[belt_num]
        tail = tails[belt_num]

        # element가 하나 밖에 없는 경우
        if head == tail == r_id:
            heads[belt_num] = -1
            tails[belt_num] = -1
            del box_ids_to_belt[r_id]

        # r_id가 head인 경우
        elif head == r_id:
            next_box_id = boxes_next[r_id]
            heads[belt_num] = next_box_id
            del boxes_next[r_id]
            del boxes_prev[next_box_id]
            del box_ids_to_belt[r_id]

        # r_id가 tail인 경우
        elif tail == r_id:
            prev_box_id = boxes_prev[r_id]
            tails[belt_num] = prev_box_id
            del boxes_next[prev_box_id]
            del boxes_prev[r_id]
            del box_ids_to_belt[r_id]

        # r_id가 head와 tail 사이에 끼여있는 경우
        else:
            prev_box_id = boxes_prev[r_id]
            next_box_id = boxes_next[r_id]
            boxes_prev[next_box_id] = prev_box_id
            boxes_next[prev_box_id] = next_box_id
            del box_ids_to_belt[r_id]
            del boxes_prev[r_id]
            del boxes_next[r_id]

        print(r_id)

    except:  # 벨트에 물건이 없는 경우
        print(-1)


# 400: 물건 확인
def identify_boxes(info):
    f_id = info[0]

    try:  # 벨트에 물건이 있는 경우
        belt_num = box_ids_to_belt[f_id] - 1

        head = heads[belt_num]
        tail = tails[belt_num]

        # element가 하나 밖에 없는 경우
        if head == tail == f_id:
            pass

        # f_id가 head인 경우
        elif head == f_id:
            pass

        # f_id가 tail인 경우
        elif tail == f_id:
            tail_prev = boxes_prev[f_id]

            boxes_next[f_id] = head
            boxes_prev[head] = f_id
            heads[belt_num] = f_id
            tails[belt_num] = tail_prev
            del boxes_next[tail_prev]
            del boxes_prev[f_id]

        # f_id가 head와 tail 사이에 끼여있는 경우
        else:
            tail_prev = boxes_prev[f_id]
            del boxes_prev[f_id]
            del boxes_next[tail_prev]
            boxes_next[tail] = head
            boxes_prev[head] = tail
            tails[belt_num] = tail_prev
            heads[belt_num] = f_id

        print(belt_num + 1)

    except:
        print(-1)


# 500: 벨트 고장
def broken_belts(info):
    broken_belt_num = info[0]
    belt_num_correction = broken_belt_num - 1

    prev_head, prev_tail = heads[belt_num_correction], tails[belt_num_correction]

    # 고장나지 않았을 경우
    if not belt_broken[belt_num_correction]:

        rg = list(range(belt_num_correction + 1, m)) + list(range(belt_num_correction))
        for idx in rg:
            if not belt_broken[idx]:
                tail = tails[idx]
                if tail == -1:
                    heads[idx - 1] = -1
                    tails[idx - 1] = -1
                    heads[idx] = prev_head
                    tails[idx] = prev_tail
                    box_ids_to_belt[prev_head] = idx + 1
                    break
                boxes_prev[prev_head] = tail
                boxes_next[tail] = prev_head
                tails[idx] = prev_tail
                start = prev_head
                while True:
                    box_ids_to_belt[start] = idx + 1
                    try:
                        next_one = boxes_next[start]
                        start = next_one
                    except:
                        break
                break

        heads[belt_num_correction] = -1
        tails[belt_num_correction] = -1
        belt_broken[belt_num_correction] = True
        print(broken_belt_num)

    else:
        print(-1)


for order in orders:

    idx = order[0]
    rest = order[1:]

    if idx == 100:
        factory_establish(rest)

    elif idx == 200:
        drop_boxes(rest)

    elif idx == 300:
        remove_boxes(rest)

    elif idx == 400:
        identify_boxes(rest)

    else:
        broken_belts(rest)