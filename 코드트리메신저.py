# 두 번째 풀이 

MAX_N = 100001
MAX_D = 21  # ❌ 0 ~ 20 인덱싱 할 수 있도록 ( 22로 안해도 됨. )

# DP에 이용할 변수들
UPWARDS = [
    [0] * MAX_D for _ in range(MAX_N)
]   
DOWNWARDS = [0] * MAX_N 

# UPWARDS[node_idx][authority]
# 노드 node_idx에서 권한 authority 일 때 전달할 수 있는 메시지의 개수
# DOWNWARDS[node_idx] 
# 하위 노드들로부터 node_idx까지 전달할 수 있는 총 메시지의 수 

# 그 외 변수들
PARENTS = [0] * MAX_N 
AUTHORITIES = [0] * MAX_N
NOTIFICATIONS = [True] * MAX_N
# CHILDREN 과 같은 거추장스러운 변수는 선언하지 않음. 


# N: 채팅방수, Q: 명령수
N, Q = [int(x) for x in input().strip().split()]

ORDERS = [
    [int(x) for x in input().strip().split()] for _ in range(Q)
]

def init(orders):

    global PARENTS, AUTHORITIES, UPWARDS, DOWNWARDS

    n = len(orders) // 2

    parent_ids, authorities = orders[:n], orders[n:]

    # PARENTS, AUTHORITIES 업데이트
    for i in range(1, n+1):
        PARENTS[i] = parent_ids[i-1]
        authority = authorities[i-1]
        if authority > 20:
            authority = 20  # 최대 깊이: 20
        AUTHORITIES[i] = authority

    # UPWARDS, DOWNWARDS 업데이트
    # 첫줄이 100 0 0 1 1 2 2 4 4 1 1 2 1 2 2 1 1 라서 숫자 표기가 헷갈리는 거지
    # 100 0 0 1 1 2 2 4 4 1 1 3 1 2 2 1 1 으로 두고 결과 찍어보면, 이해가 확 됨. 
    # 결국 각 노드들에 대해 for 문을 돌릴 때 UPWARD, DOWNWARD는 서로 independent 함
    for i in range(1, n+1):
        current_node = i    # 
        authority = AUTHORITIES[i]
        UPWARDS[current_node][authority] += 1
        # ∵ PARENTS[0] = 0
        while authority > 0 and PARENTS[current_node]:
            parent_node = PARENTS[current_node]
            authority -= 1
            if authority > 0:
                UPWARDS[parent_node][authority] += 1
            DOWNWARDS[parent_node] += 1
            current_node = parent_node


def on_off(node_id):

    global NOTIFICATIONS

    parent_id = PARENTS[node_id]
    num = 1

    noti_on = NOTIFICATIONS[node_id]

    while parent_id:
        # UPWARDS의 모든 column들을 훑음
        for i in range(num, MAX_D):    ## ❌ 22로 안 해도 됨 
            upward_value = UPWARDS[node_id][i]
            if noti_on: # 값 없애기
                DOWNWARDS[parent_id] -= upward_value
            else:   # 원복
                DOWNWARDS[parent_id] += upward_value
            
            if i > num: # depth dimension 왼 -> 오 ( depth를 위로 늘려나가는 중 )
                if noti_on:
                    UPWARDS[parent_id][i - num] -= upward_value
                else:
                    UPWARDS[parent_id][i - num] += upward_value
        
        # 부모 노드의 notification이 꺼져있으면 더 이상 위로 전파하지 않음 
        if not NOTIFICATIONS[parent_id]:
            break

        parent_id = PARENTS[parent_id]
        num += 1

    NOTIFICATIONS[node_id] = not noti_on


def authority_change(order):

    global AUTHORITIES, UPWARDS, DOWNWARDS

    c, new_power = order

    old_authority = AUTHORITIES[c]
    new_power = min(new_power, MAX_D - 1)   # ❌ 풀이: min(new_power, 20)
    AUTHORITIES[c] = new_power

    noti_on = NOTIFICATIONS[c]

    # 기존의 권한 관련 내용 삭제

    UPWARDS[c][old_authority] -= 1
    if noti_on: # 해당 node 위의 알림망이 ON 상태라면 함께 업데이트 해주어야
        parent_id = PARENTS[c]
        num = 1
        while parent_id:
            if old_authority >= num:
                DOWNWARDS[parent_id] -= 1
            if old_authority > num:
                UPWARDS[parent_id][old_authority - num] -= 1
            if not NOTIFICATIONS[parent_id]:
                break
            parent_id = PARENTS[parent_id]
            num += 1

    # 새로 부여 받은 권한 내용으로 업데이트
    UPWARDS[c][new_power] += 1
    if noti_on:
        parent_id = PARENTS[c]
        num = 1
        while parent_id:
            if new_power >= num:
                DOWNWARDS[parent_id] += 1
            if new_power > num:
                UPWARDS[parent_id][new_power - num] += 1
            if not NOTIFICATIONS[parent_id]:
                break
            parent_id = PARENTS[parent_id]
            num += 1
         

def exchange_parent(order):

    global PARENTS

    node1, node2 = order

    parent1, parent2 = PARENTS[node1], PARENTS[node2]

    node1_noti = NOTIFICATIONS[node1]
    node2_noti = NOTIFICATIONS[node2]

    if node1_noti:
        on_off(node1)
    if node2_noti:
        on_off(node2)

    PARENTS[node1], PARENTS[node2] = parent2, parent1

    if node1_noti:
        on_off(node1)
    if node2_noti:
        on_off(node2)

    
def print_result(node_id):
    print(DOWNWARDS[node_id])


cnt = 0
while cnt < Q:

    order = ORDERS[cnt]

    cmd = order[0]

    if cmd == 100:
        init(order[1:])

    elif cmd == 200:
        on_off(order[1])
    
    elif cmd == 300:
        authority_change(order[1:])

    elif cmd == 400:
        exchange_parent(order[1:])

    else:
        print_result(order[1])

    cnt += 1
    
#####

# 첫번째 풀이 

from collections import defaultdict, deque

N, Q = [
    int(x) for x in input().strip().split()
]

ORDERS = [
    [int(x) for x in input().strip().split()] for _ in range(Q)
]

PARENTS = []
AUTHORITY = []

NEXT_NODES = defaultdict(list)
DELETED_NEXT_NODES = defaultdict(list)

PREV_NODES = dict()
DELETED_PREV_NODES = dict()

# { 노드 번호: 노드 클래스 }
NODE_DICT = dict()


class NODE:
    def __init__(self, node_num):
        self.node_num = node_num
        self.noti_on = True
        self.authority = 0
        self.depth = 0


# 100
def prepare_inner_messenger(info):

    global PARENTS, AUTHORITY, NEXT_NODES, PREV_NODES, NODE_DICT

    cnt = len(info)
    q = cnt // 2

    PARENTS, AUTHORITY = info[:q], info[q:]

    for i in range(N+1):
        node = NODE(i)
        if i != 0:  # 최상위 노드는 제외 
            node.authority = AUTHORITY[i-1]
        NODE_DICT[i] = node

    for idx in range(1, len(PARENTS)+1):
        PREV_NODES[idx] = PARENTS[idx-1]
        
    for key, value in PREV_NODES.items():
        NEXT_NODES[value].append(key)
        
    NEXT_NODES = dict(sorted(NEXT_NODES.items(), key=lambda x: x[0]))
    q = []
    for child in NEXT_NODES[0]:
        q.append([child, 0])
    q = deque(q) 
    
    while q:
        parent, cnt = q.popleft()
        if cnt + 1 > 20:
            next_nodes = NEXT_NODES[parent]
            del NEXT_NODES[parent]
            for nn in next_nodes:
                del PREV_NODES[nn]
            continue
        NODE_DICT[parent].depth = cnt + 1
        if parent in NEXT_NODES:
            grand_children = NEXT_NODES[parent]
            grand_children = list(zip(*[grand_children, [cnt+1]*len(grand_children)]))
            q.extend(grand_children)


# 200
def notification_on_off(c):

    global NODE_DICT, PREV_NODES, DELETED_PREV_NODES

    node = NODE_DICT[c]
    node.noti_on = not node.noti_on

    # 최상위 노드의 경우에는 전혀 영향 받지 않으므로 
    if c != 0:

        # ON -> OFF 
        if not node.noti_on:
            prev_node = PREV_NODES[c]

            DELETED_NEXT_NODES[prev_node].append(c)
            DELETED_PREV_NODES[c] = prev_node
            
            NEXT_NODES[prev_node].remove(c)
            del PREV_NODES[c]

        # OFF -> ON
        else:
            prev_node = DELETED_PREV_NODES.pop(c)   

            NEXT_NODES[prev_node].append(c)
            PREV_NODES[c] = prev_node

            if c in DELETED_NEXT_NODES[prev_node]:
                DELETED_NEXT_NODES[prev_node].remove(c)
                if not DELETED_NEXT_NODES[prev_node]:
                    del DELETED_NEXT_NODES[prev_node]
                
    NODE_DICT[c] = node


# 300
def authority_power_modification(info):

    c, power = info

    node = NODE_DICT[c]
    node.authority = power
    NODE_DICT[c] = node


# 400
def change_parent(info):

    def get_parent_children(c):

        if c in PREV_NODES:
            flag = True
            c_parent = PREV_NODES[c]
        else:
            flag = False
            c_parent = DELETED_PREV_NODES[c]

        return c_parent, flag

    def change_parent_children(c1, c2, c1_parent, c2_parent, c1_flag):
        
        global PREV_NODES, NEXT_NODES, DELETED_NEXT_NODES, DELETED_PREV_NODES
        
        if c1_flag: 
            NEXT_NODES[c1_parent].remove(c1)
            NEXT_NODES[c2_parent].append(c1)
            del PREV_NODES[c1]
            PREV_NODES[c1] = c2_parent
            # PREV_NODES[c2] = c1_parent
            
        else:
            DELETED_NEXT_NODES[c1_parent].remove(c1)
            DELETED_NEXT_NODES[c2_parent].append(c1)
            del DELETED_PREV_NODES[c1]
            DELETED_PREV_NODES[c1] = c2_parent

    c1, c2 = info
        
    c1_parent, flag1 = get_parent_children(c1)
    c2_parent, flag2 = get_parent_children(c2)

    change_parent_children(c1, c2, c1_parent, c2_parent, flag1)
    change_parent_children(c2, c1, c2_parent, c1_parent, flag2)


# 500
def count_and_print(c):

    cnt = 0
    current_node_depth = NODE_DICT[c].depth
    
    if c not in NEXT_NODES:
        print(cnt)
        return

    next_nodes = NEXT_NODES[c]
    next_nodes = deque(next_nodes)

    while next_nodes:
        next_node = next_nodes.popleft()
        next_node_class = NODE_DICT[next_node]
        if not next_node_class.noti_on or current_node_depth > 20: 
            continue
        if next_node_class.depth - current_node_depth <= next_node_class.authority:
            cnt += 1
        if next_node in NEXT_NODES:
            next_nodes.extend(NEXT_NODES[next_node])

    print(cnt)


cnt = 0

while cnt < Q:

    order = ORDERS[cnt]

    idx = order[0]

    if idx == 100:
        prepare_inner_messenger(order[1:])

    elif idx == 200:
        notification_on_off(order[1])

    elif idx == 300:
        authority_power_modification(order[1:])

    elif idx == 400:
        change_parent(order[1:])

    else:
        count_and_print(order[1])
    
    cnt += 1