from heapq import heappush, heappop, heapify
from collections import defaultdict

Q = int(input().strip())

INFO = [
    [int(x) for x in input().strip().split()] for _ in range(Q)
]

board = None
minDist = None
INF = float('inf')
n = 0
s = 0   # 여행 상품 출발지 

productHeap = []

registered_id = defaultdict(bool)
delete_id = defaultdict(bool)

#%%

# order 100
def make_board(info):
    
    global board, n

    n, m, graph = info[0], info[1], info[2:]

    board = [
        [INF] * n for _ in range(n)
    ]

    # 자기자신
    for idx in range(n):
        board[idx][idx] = 0
    # 자기자신 제외 나머지 
    for idx in range(len(graph)//3):
        start, end, weight = graph[3*idx : 3*(idx+1)]
        # if start == end:    # 어차피 최소 비용을 써야 하니까. 
        #     continue
        board[start][end] = min(board[start][end], weight)
        board[end][start] = min(board[end][start], weight)


# order 100
def perform_dijkstra():

    global minDist

    minDist = [INF] * n
    is_visited = [False] * n

    minDist[s] = 0  # 시작 노드의 거리는 0으로 설정

    heap = [(0, s)]  # (distance , src node)
    heapify(heap)

    while heap:
        current_dist, current_node = heappop(heap)

        if is_visited[current_node]:
            continue

        is_visited[current_node] = True 

        for neighbor, weight in enumerate(board[current_node]):
            if (weight != INF) and (not is_visited[neighbor]):
                distance = current_dist + weight

                if distance < minDist[neighbor]:
                    minDist[neighbor] = distance
                    heappush(heap, (distance, neighbor))

        
# order 200
def create_travel_product(sub_info):

    global productHeap, registered_id

    id_, revenue, dest = sub_info   # id_: 모두 다름. 

    registered_id[id_]

    value = revenue - minDist[dest] # revenue - cost
    heappush(productHeap, (-value, id_, revenue, dest)) # revenue - cost가 최대였으면 하기 때문 


# order 300
def remove_travel_product(id_):

    ########### 시간 초과 주범 ###########
    # global productHeap

    # for i, ph in enumerate(productHeap):
    #     if id_ == ph[1]:
    #         productHeap.pop(i)
    #         break

    # heapify(productHeap)   
    ###################################

    global delete_id

    if id_ in registered_id:
        delete_id[id_]


# order 400
def print_optimal_product():

    global productHeap

    # ########### 시간 초과 주범 ###########
    # temp_heap = []
    # flag = True

    # while productHeap:
    #     popped = heappop(productHeap) 
    #     if popped[1] in delete_id:
    #         continue
    #     if -1 * popped[0] >= 0:  # revenue - cost >= 0
    #         print(popped[1])
    #         flag = False
    #         break
    #     temp_heap.append(popped)

    # if flag:
    #     print(-1)

    # heapify(temp_heap)
    # for ph in productHeap:
    #     heappush(temp_heap, ph)

    # productHeap = temp_heap
    # ###################################

    while productHeap:
        first = productHeap[0]
        if first[0] > 0:
            break
        popped = heappop(productHeap)
        if popped[1] not in delete_id:
            print(popped[1])
            return

    return print(-1)


# order 500
def change_starting_point(starting_point):

    global s, productHeap

    s = starting_point
    perform_dijkstra()

    new_heap = []
    for _, id_, revenue, dest in productHeap:
        new_heap.append([id_, revenue, dest])
    productHeap = []
    for sub_info in new_heap:
        create_travel_product(sub_info)


#%%

cnt = 0
while cnt < Q:

    instance = INFO[cnt]

    order = instance[0]

    try:
        sub_info = instance[1:]
    except:
        pass

    # 코드트리 랜드 건설
    if order == 100:
        make_board(sub_info)
        perform_dijkstra()

    # 여행 상품 생성
    elif order == 200:
        create_travel_product(sub_info)
    
    # 여행 상품 취소
    elif order == 300:
        remove_travel_product(*sub_info)

    # 최적의 여행 상품 판매
    elif order == 400:
        print_optimal_product()

    # 여행 상품의 출발지 변경
    else:
        change_starting_point(*sub_info)

    cnt += 1
