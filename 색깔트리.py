from collections import defaultdict, deque

# 명령의 수 
Q = int(input().strip())

# 명령의 정보
ORDER_INFO = [
    [int(x) for x in input().strip().split()] for _ in range(Q)
]

NEXT_NODES = defaultdict(list)  # 20000 번 처리 건 때문에 dictionary로 처리. (매 번 타고타고 search 할 수는 없으니)
PREV_NODE = defaultdict(int)   # 부모 노드는 하나 이기 때문. 
ROOT_NODES = []
LEAF_NODES = []
COLOR_CHANGED = []

NODE_MAPPER = dict()    # key: 노드의 index, value: 해당 노드 Class
VALUE_DICT = defaultdict(set)



class NODE:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth

        self.current_depth = 1  # 해당 노드의 현재 depth


# 100: 노드 추가 
def add_node(order):
    
    global NEXT_NODES, NODE_MAPPER, PREV_NODE, LEAF_NODES, ROOT_NODES

    m_id, p_id, color, max_depth = order[1:]

    node = NODE(m_id, p_id, color, max_depth)

    # True: 실제로 노드를 추가한다.
    flag = True

    # 루트 노드면
    if p_id == -1:
        NODE_MAPPER[m_id] = node
        ROOT_NODES.append(m_id)
        LEAF_NODES.append(m_id)

    # 루트 노드가 아니면,
    else:
        upper_nodes = deque([p_id])

        depth_add = 1   # 노드 하나가 추가되는 것이기 때문 
        while upper_nodes:
            prev_node_num = upper_nodes.popleft()
            prev_node_class = NODE_MAPPER[prev_node_num]
            if prev_node_class.p_id != -1:
                upper_nodes.append(prev_node_class.p_id)
            if prev_node_class.current_depth + depth_add > prev_node_class.max_depth:
                flag = False
                break
            depth_add += 1  # 이 조건 하나 빠트려서 시간 엄청 잡아먹음 😭

        if flag:
            NEXT_NODES[p_id].append(m_id)
            PREV_NODE[m_id] = p_id
            NODE_MAPPER[m_id] = node
            
    if flag:
        if p_id != -1:
            if p_id in LEAF_NODES:
                LEAF_NODES.remove(p_id)
            LEAF_NODES.append(m_id)
    

# 200: 색깔 변경
def change_color(order):

    global NODE_MAPPER

    m_id, color = order[1:]

    whole_nodes = set()

    q = deque([m_id])

    while q:
        popped = q.popleft()
        whole_nodes.add(popped)
        if popped in NEXT_NODES:
            next_nodes = NEXT_NODES[popped]
            q.extend(next_nodes)

    for pn in whole_nodes:
        node = NODE_MAPPER[pn]
        node.color = color


# 300: 색깔 조회
def search_color(order):
    m_id = order[1]
    print(NODE_MAPPER[m_id].color)


# 400: 점수 조회
def search_score():
    
    count = 0
    color_dict = defaultdict(set)

    for ln in LEAF_NODES:
        current = ln
        color_dict[ln].add(NODE_MAPPER[ln].color)
        while True:
            if current in PREV_NODE:
                prev_node_idx = PREV_NODE[current]
                prev_node = NODE_MAPPER[prev_node_idx]
                prev_m_id, prev_p_id = prev_node.m_id, prev_node.p_id
                prev_color = prev_node.color
                color_dict[prev_m_id].update(list(color_dict[current]) + [prev_color])
                current = prev_node_idx
                if prev_p_id == -1:
                    break
            else:
                break

    for col, val in color_dict.items():
        count += len(val) ** 2
    
    print(count)


cnt = 0

while cnt < Q:

    order = ORDER_INFO[cnt]
    identity = order[0]

    # 노드 추가
    if identity == 100:
        add_node(order)

    # 색깔 변경
    elif identity == 200:
        change_color(order)

    # 색깔 조회
    elif identity == 300:
        search_color(order)

    # 점수 조회
    else:
        search_score()
        
    cnt += 1

