import sys
from heapq import heappop, heappush, heapify
from collections import defaultdict

Q = int(input())

orders = []
for _ in range(Q):
    order = input().split(' ')
    orders.append(order)

waiting_queue = defaultdict(list)  # [ [ 시간, 채점 우선순위, url ] , [ 시간, 채점 우선순위, url ] , ... ] <- 원래 input이 들어온다면 취해야 할 형태

url_in_queue = defaultdict(int)  # '채점 대기 큐에 있는 task에 존재하는 url'
domain_in_judging = defaultdict(int)
evaluator_in_progress = []
jid_to_info = dict()
history = dict()


# 코드트리 채점기 준비
def prepare_evaluator(info):  # 100

    global N, evaluator_in_progress, url_in_queue

    N, initial_url = info
    N = int(N)  # 채점기의 개수
    evaluator_in_progress = [False] * N
    domain, p_id = initial_url.split('/')

    # '도메인 별'로 대기 큐를 만들 예정
    waiting_queue[domain] = []
    heappush(waiting_queue[domain], (1, 0, initial_url))  # [우선순위, 시간, url] 순으로 임의로 순서 변경.

    url_in_queue[initial_url] += 1


# 채점 요청
def request_evaluation(info):  # 200

    global waiting_queue, url_in_queue

    t, p, u = info  # 시간, 우선순위, url
    t, p = int(t), int(p)

    # 대기 큐에 있는 task 중 u와 정확히 일치하는 url이 존재하는 경우
    if url_in_queue[u] > 0:
        return

    domain, pid = u.split('/')
    # 도메인 별로 우선순위 큐를 생성.
    if domain in waiting_queue:
        heappush(waiting_queue[domain], (p, t, u))  # ( 우선순위 , 들어온 시간 , url )
    else:
        waiting_queue[domain] = []
        heappush(waiting_queue[domain], (p, t, u))

    url_in_queue[u] += 1


# 채점 시도
def try_evaluation(in_time):  # 300

    global evaluator_in_progress, url_in_queue, waiting_queue, jid_to_info

    # 채점 시도 시간
    in_time = int(in_time[0])

    # 쉬고 있는 채점기가 하나도 없는 경우
    if sum(evaluator_in_progress) == N:  # 해당 함수 가장 마지막의 내용을 맨 앞으로 당겨옴.
        return

    temp_heap = []

    for domain, value in waiting_queue.items():
        if domain_in_judging[domain] != 0:  # 도메인이 현재 채점을 진행 중인 도메인 중 하나인 경우
            continue
        if domain in history:  # 도메인과 정확히 일치하는 도메인에 대해 ...
            start, end, domain, judging_jid = history[domain]
            gap = end - start
            if in_time < start + 3 * gap:
                continue

        if len(value) == 0:
            continue

        heappush(temp_heap, value[0])

    if len(temp_heap) == 0:
        return

    selected = temp_heap[0]
    p, t, u = selected

    j_id = 0
    for i, boolean in enumerate(evaluator_in_progress):
        if not boolean:  # 채점 안 하고 있는.
            j_id = i
            break
    evaluator_in_progress[j_id] = True

    selected = list(selected)
    selected[1] = in_time
    selected = tuple(selected)
    jid_to_info[j_id + 1] = selected  # 인덱스 조정 ( key: 채점기 번호 )

    domain, pid = u.split('/')
    domain_in_judging[domain] += 1
    heappop(waiting_queue[domain])

    url_in_queue[u] -= 1


# 채점 종료
def exit_evaluation(info):  # 400

    global evaluator_in_progress, jid_to_info, domain_in_judging

    t, j_id = info
    t, j_id = int(t), int(j_id)

    if j_id not in jid_to_info:
        return

    p, start, u = jid_to_info[j_id]
    del jid_to_info[j_id]

    evaluator_in_progress[j_id - 1] = False

    domain = u.split('/')[0]
    domain_in_judging[domain] -= 1
    if domain not in history:
        history[domain] = [start, t, domain, j_id]  # 이전의 것들에 대한 정보는 필요 없음.
    else:
        if start > history[domain][0]:
            history[domain] = [start, t, domain, j_id]


# 채점 대기 큐 조회
def wait_evaluation():  # 500
    cnt = 0
    for value in waiting_queue.values():
        cnt += len(value)
    print(cnt)


for idx, order in enumerate(orders):

    code, info = int(order[0]), order[1:]

    if code == 100:
        prepare_evaluator(info)

    elif code == 200:
        request_evaluation(info)

    elif code == 300:
        try_evaluation(info)

    elif code == 400:
        exit_evaluation(info)

    else:
        wait_evaluation()