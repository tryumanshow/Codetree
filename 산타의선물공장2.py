import math

num_orders = int(input().strip())

orders = [
    [int(x) for x in input().strip().split(' ')] for _ in range(num_orders)
]


heads = []
tails = []

next_box = dict()
prev_box = dict()

# bnum_to_belt = dict()
box_cnt_per_belt = []


"""
box 번호, 벨트 번호 모두 -> 기존 인덱스 -1 
"""


# 100: 공장 설립
def establish_factory(info):
    global heads, tails, next_box, prev_box, box_cnt_per_belt

    n, m = info[:2]
    belt_nums = [x - 1 for x in info[2:]]  # 인덱스 보정
    box_cnt_per_belt = [0] * n

    heads = [-1] * n
    tails = [-1] * n

    temp_list = [[] for _ in range(n)]  # 인덱스 보정

    for idx, bn in enumerate(belt_nums):
        # bnum_to_belt[idx] = bn  # box 번호 : belt 번호
        temp_list[bn].append(idx)
        box_cnt_per_belt[bn] += 1

    for idx, tl in enumerate(temp_list):
        if len(tl) == 0:  # 빈 벨트일 경우
            continue
        elif len(tl) == 1:  # 벨트에 박스가 하나 밖에 없을 경우
            heads[idx] = tl[0]
            tails[idx] = tl[0]
        else:  # 두 개 이상의 박스가 있을 경우
            for front, back in zip(tl, tl[1:]):
                next_box[front] = back
                prev_box[back] = front
            heads[idx] = tl[0]
            tails[idx] = tl[-1]

    del temp_list


# 200: 물건 모두 옮기기
def move_whole_boxes(info):
    """
    m_src 번째 벨트의 모든 물건들 -> m_dst 번째 벨트로 옮긴다.
    """

    m_src, m_dst = [x - 1 for x in info]

    # m_src 벨트에 아무 선물도 존재하지 않는 경우
    if heads[m_src] == -1:
        print(box_cnt_per_belt[m_dst])
        return

    # m_dst 벨트에 아무 선물도 존재하지 않는 경우
    if heads[m_dst] == -1:
        heads[m_dst] = heads[m_src]
        tails[m_dst] = tails[m_src]

    # 존재 하는 경우
    else:
        src_tail = tails[m_src]
        dst_head = heads[m_dst]

        next_box[src_tail] = dst_head
        prev_box[dst_head] = src_tail
        heads[m_dst] = heads[m_src]

    box_cnt_per_belt[m_dst] += box_cnt_per_belt[m_src]
    box_cnt_per_belt[m_src] = 0

    # bnum_to_belt update
    # next_src = heads[m_src]
    # while True:
    #     if next_src == tails[m_src]:
    #         bnum_to_belt[next_src] = m_dst
    #     elif next_src in next_box:
    #         bnum_to_belt[next_src] = m_dst
    #         next_src = next_box[next_src]
    #         continue
    #     break

    heads[m_src] = -1
    tails[m_src] = -1

    print(box_cnt_per_belt[m_dst])


# 300: 앞 물건만 교체하기
def change_only_the_very_front(info):
    """
    'm_src의 맨 앞의 박스' & 'm_dst의 맨 앞의 박스'  사이의 교환
    """

    def one_case1(m_src, m_dst):
        """
        m_dst에만 박스가 존재하며, m_dst의 맨 앞의 박스 -> m_src 맨 앞의 박스로 옮기는 상황.
        """

        if heads[m_dst] == tails[m_dst]:  # m_dst에 박스가 하나 밖에 없는 경우
            m_dst_front = heads[m_dst]
            heads[m_src] = m_dst_front
            tails[m_src] = m_dst_front
            heads[m_dst] = -1
            tails[m_dst] = -1

        else:  # m_dst에 박스가 두 개 이상 있는 경우
            m_dst_front = heads[m_dst]
            m_dst_next = next_box[m_dst_front]
            heads[m_src] = m_dst_front
            tails[m_src] = m_dst_front
            heads[m_dst] = m_dst_next

            del next_box[m_dst_front]
            del prev_box[m_dst_next]

        box_cnt_per_belt[m_src] += 1
        box_cnt_per_belt[m_dst] -= 1
        # bnum_to_belt[m_dst_front] = m_src

    # 한 벨트에는 박스가 한 개, 다른 한 벨트에는 두 개 이상의 박스가 존재하는 경우
    def one_case2(m_src, m_dst, src_front, dst_front):
        """
        m_src, m_dst 모두에 박스가 존재하는 경우 & m_src에는 한 개 , m_dst 벨트에 두 개 이상의 박스가 존재하는 경우
        """
        dst_next = next_box[dst_front]

        heads[m_dst] = src_front
        next_box[src_front] = dst_next
        prev_box[dst_next] = src_front

        heads[m_src] = dst_front
        tails[m_src] = dst_front

        # bnum_to_belt[src_front] = m_dst
        # bnum_to_belt[dst_front] = m_src

        del next_box[dst_front]

    m_src, m_dst = [x - 1 for x in info]

    # 둘 다 존재하지 않는 경우
    if heads[m_src] == -1 and heads[m_dst] == -1:
        print(0)
        return

    # m_src 벨트에 선물이 존재하지 않는 경우 = m_dst 벨트의 맨 앞 박스를 m_src로 옮긴다.
    elif heads[m_src] == -1 and heads[m_dst] != -1:
        one_case1(m_src, m_dst)

    # m_dst 벨트에 선물이 존재하지 않는 경우 = m_src 벨트의 맨 앞 박스를 m_dst로 옮긴다.
    elif heads[m_src] != -1 and heads[m_dst] == -1:
        one_case1(m_dst, m_src)

    # m_src, m_dst 벨트 모두에 선물이 존재하는 경우 = m_src, m_dst의 박스를 단순히 위치만 바꾼다.
    else:
        src_front, dst_front = heads[m_src], heads[m_dst]
        src_tail, dst_tail = tails[m_src], tails[m_dst]

        # 둘 다 한 개 씩만 있을 때
        if (src_front == src_tail) and (dst_front == dst_tail):
            heads[m_src] = dst_front
            tails[m_src] = dst_front
            heads[m_dst] = src_front
            tails[m_dst] = src_front
            # bnum_to_belt[src_front] = m_dst
            # bnum_to_belt[dst_front] = m_src

        # m_src에는 한 개, m_dst에는 여러 개가 존재할 때
        elif (src_front == src_tail) and (dst_front != dst_tail):
            one_case2(m_src, m_dst, src_front, dst_front)

        # m_dst에는 한 개, m_src에는 여러 개가 존재 할 때
        elif (src_front != src_tail) and (dst_front == dst_tail):
            one_case2(m_dst, m_src, dst_front, src_front)

        # 둘 다 여러 개가 존재할 때
        else:
            src_next, dst_next = next_box[src_front], next_box[dst_front]

            heads[m_src] = dst_front
            next_box[dst_front] = src_next
            prev_box[src_next] = dst_front

            heads[m_dst] = src_front
            next_box[src_front] = dst_next
            prev_box[dst_next] = src_front

            # bnum_to_belt[src_front] = m_dst
            # bnum_to_belt[dst_front] = m_src

    print(box_cnt_per_belt[m_dst])


# 400: 물건 나누기
def divide_boxes(info):
    """
    m_src 벨트에 있는 박스의 반절을 m_dst로 보내기
    """

    m_src, m_dst = [x - 1 for x in info]

    # m_src 벨트에 있는 선물이 1개 (이하)인 경우
    if box_cnt_per_belt[m_src] <= 1:
        print(box_cnt_per_belt[m_dst])
        return

    box_cnt_to_move = math.floor(box_cnt_per_belt[m_src] / 2)
    m_src_head = heads[m_src]

    cnt = 1
    last_box = m_src_head
    box_to_move = [m_src_head]
    while cnt < box_cnt_to_move:
        last_box = next_box[last_box]
        box_to_move.append(last_box)
        cnt += 1

    last_box = box_to_move[-1]
    # m_dst 벨트에 선물이 하나도 없는 경우
    if box_cnt_per_belt[m_dst] == 0:
        heads[m_dst] = heads[m_src]
        tails[m_dst] = last_box
        next_last = next_box[last_box]
        heads[m_src] = next_last
        del next_box[last_box]
        del prev_box[next_last]

    # m_dst 벨트에 선물이 있는 경우
    else:
        next_dst = next_box[last_box]
        del prev_box[next_dst]
        del next_box[last_box]
        heads[m_src] = next_dst

        m_dst_head = heads[m_dst]
        next_box[last_box] = m_dst_head
        prev_box[m_dst_head] = last_box
        heads[m_dst] = m_src_head

    box_cnt_per_belt[m_src] -= box_cnt_to_move
    box_cnt_per_belt[m_dst] += box_cnt_to_move

    # 박스번호 바꿔주기
    # for btm in box_to_move:
    #     bnum_to_belt[btm] = m_dst

    print(box_cnt_per_belt[m_dst])


# 500 선물 정보 얻기
def get_present_information(info):
    box_num = info[0] - 1

    a = -1
    if box_num in prev_box:
        a = prev_box[box_num] + 1

    b = -1
    if box_num in next_box:
        b = next_box[box_num] + 1

    print(a + 2 * b)


# 600: 벨트 정보 얻기
def get_belt_info(info):
    b_num = info[0] - 1

    a = heads[b_num] + 1  # 출력시 인덱스 다시 돌려줌
    b = tails[b_num] + 1

    if a == 0:
        assert b == 0, 'Strange'
        a = b = -1
        c = 0

    else:
        c = box_cnt_per_belt[b_num]

    print(a + 2 * b + 3 * c)


for order in orders:

    order_idx, info = order[0], order[1:]

    # 공장설립
    if order_idx == 100:
        establish_factory(info)

    # # 물건 모두 옮기기
    elif order_idx == 200:
        move_whole_boxes(info)

    # # 앞 물건만 교체하기
    elif order_idx == 300:
        change_only_the_very_front(info)

    # 물건 나누기
    elif order_idx == 400:
        divide_boxes(info)

    # 선물 정보 얻기
    elif order_idx == 500:
        get_present_information(info)

    # 벨트 정보 얻기
    else:
        get_belt_info(info)