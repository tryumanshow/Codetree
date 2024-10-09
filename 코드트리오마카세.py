# 두 번째 풀이 

from collections import defaultdict

# L : 초밥 벨트의 길이, Q : 명령의 수 

L, Q = [int(x) for x in input().strip().split()]
ORDERS = [
    input().strip().split() for _ in range(Q)
]

WHOLE_QUERIES = []

SUSHI_MAKING_QUERIES = defaultdict(list)    # 100
ENTRANCE_QUERIES = dict()   # 200
NAMES = set()
ENTRY_TIME = dict()
POSITION = dict()

EXIT_TIME = dict()

class Query:
    def __init__(self, cmd, t, x, name, n):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n


for order in ORDERS:
    cmd = int(order[0])
    t, x, name, n = -1, -1, -1, -1  # 초기화
    if cmd == 100:
        t, x, name = order[1:]
    elif cmd == 200:
        t, x, name, n = order[1:]    
    else:
        t = order[1]

    if cmd == 300:
        cmd = 1000
    Q = Query(cmd, int(t), int(x), name, n)
    WHOLE_QUERIES.append(Q)

    if cmd == 100:
        SUSHI_MAKING_QUERIES[name].append(Q)
    # 중복해서 나타나는 경우가 없으므로 -> set 및 dictionary로 표기 
    elif cmd == 200:
        NAMES.add(name)
        ENTRY_TIME[name] = int(t)
        POSITION[name] = int(x)


# 자신의 이름이 적힌 초밥을 먹는 시간 계산
# 초밥이 사라지는 시간에 대한 Logic
for name in NAMES:
    # 해당 사람의 퇴장 시간 
    EXIT_TIME[name] = 0

    for query in SUSHI_MAKING_QUERIES[name]:
        # 처음 초밥들이 들어온 각자의 시간 
        in_time, in_position = query.t, query.x

        ## 손님이 들어왔을 때로부터 얼마나 시간이 더 지나서, 어떤 위치에서 현 시점의 스시가 사라지게 될 것인지. 
        
        # 아직 스시에 대해 해당 손님이 들어오지 않았을 때
        if in_time < ENTRY_TIME[name]:
            # 손님이 들어왔을 때 이전에 들어왔던 초밥은 현재 어디에 위치해 있는지
            position_at_entry_time = (in_position + (ENTRY_TIME[name] - in_time)) % L
            # 해당 위치의 초밥이 먹히기 위해서는 얼마의 시간이 더 필요한지. 
            additional_time = (POSITION[name] + L - position_at_entry_time) % L

            remove_time = ENTRY_TIME[name] + additional_time

        # 스시에 대해 해당 손님이 들어와 있을 때
        else:   
            additional_time = (POSITION[name] + L - in_position) % L
            remove_time = in_time + additional_time

        # EXIT_TIME[name] = remove_time으로 하면 안되는 이유: 시간이 동일한데, 놓여있는 초밥의 위치는 다를 때 -> 가까이 있는 초밥을 기준으로 잡을 수 있음 
        EXIT_TIME[name] = max(EXIT_TIME[name], remove_time)

        # position이나 초밥 개수는 알 필요가 없음 
        new_query = Query(400, remove_time, -1, name, -1)
        WHOLE_QUERIES.append(new_query)

for name in NAMES:
    WHOLE_QUERIES.append(Query(500, EXIT_TIME[name], -1, name, -1))

# 사진 촬영 이전에 초밥 회전 + 초밥 시식이 먼저이기 때문에 cmd 기준으로도 정렬해야함.
WHOLE_QUERIES = sorted(WHOLE_QUERIES, key=lambda x: (x.t, x.cmd))

sushi_alive, people_alive = 0, 0
for query in WHOLE_QUERIES:
    cmd = query.cmd
    if cmd == 100:
        sushi_alive += 1
    elif cmd == 200:
        people_alive += 1
    elif cmd == 400:
        sushi_alive -= 1
    elif cmd == 500:
        people_alive -= 1
    else:
        print(f"{people_alive} {sushi_alive}")


#%%

# 첫번째 풀이 : TC 3번 시간초과

from collections import defaultdict

# L : 초밥 벨트의 길이, Q: 명령의 수
L, Q = [int(x) for x in input().strip().split()]

ORDERS = [
    [x for x in input().strip().split()] for _ in range(Q)
]


# { X : { Name : 테이블 위 초밥 개수 } } , 단 Name은 여러 개 일 수 있음. 
SUSHI_STATE = defaultdict(lambda: defaultdict(int))
SUSHI_STATE_ROTATE = defaultdict(lambda: defaultdict(int))

# { X : { Name : 게스트가 먹을 수 있는 초밥 개수 } }
GUEST_STATE = defaultdict(lambda: defaultdict(int))

prev_t = 0


def rotate(current_t):

    global SUSHI_STATE, SUSHI_STATE_ROTATE, prev_t

    SUSHI_STATE_ROTATE = defaultdict(lambda: defaultdict(int))

    rotate_cnt = current_t - prev_t
    q, r = divmod(rotate_cnt, L)

    tmp_cnt = 1
    # 한 바퀴 다 돌린 후에 r로 바로 넘어간다. 
    end_number = L+r if q >= 1 else r
    while tmp_cnt < end_number:
        for x, value in SUSHI_STATE.items():
            key_move = (x + 1) % L
            SUSHI_STATE_ROTATE[key_move] = value
        eat_right_now()
        SUSHI_STATE = SUSHI_STATE_ROTATE
        SUSHI_STATE_ROTATE = defaultdict(lambda: defaultdict(int))
        tmp_cnt += 1

    SUSHI_STATE_ROTATE = defaultdict(lambda: defaultdict(int))

    for x, value in SUSHI_STATE.items():
        # value: dictionary 
        key_move = (x + 1) % L
        SUSHI_STATE_ROTATE[key_move] = value

    prev_t = current_t  


# 100
def make_sushi(order):

    global SUSHI_STATE_ROTATE

    # 시각 t에 위치 x 앞에 있는 벨트 위에 name 이름을 부착한 회전 초밥을 하나 올려 놓는다. 
    t, x, name = order
    t, x = int(t), int(x) 

    rotate(t)

    SUSHI_STATE_ROTATE[x][name] += 1

    eat_right_now()

   
# 200
def guest_comein(order):

    global GUEST_STATE, SUSHI_STATE_ROTATE

    # 이름이 name인 사람이 시각 t에 위치 x에 있는 의자로 가서 앉은 뒤 n개의 초밥을 먹을 때까지 기다림 
    t, x, name, n = order
    t, x, n = int(t), int(x), int(n)

    rotate(t)

    GUEST_STATE[x][name] = n

    eat_right_now()


def eat_right_now():

    global SUSHI_STATE_ROTATE, GUEST_STATE

    to_modify, to_remove = [], []

    for x, values in SUSHI_STATE_ROTATE.items():
        for name_, cnt_ in values.items():
            if x in GUEST_STATE:
                if name_ in GUEST_STATE[x]:
                    sushi_left = GUEST_STATE[x][name_] - cnt_   # sushi_left < 0 이면 떠난다. 
                    if sushi_left <= 0:
                        if sushi_left < 0:
                            to_modify.append([x, name_, -sushi_left])
                        else:
                            to_remove.append([x, name_])
                        del GUEST_STATE[x][name_]
                        if not GUEST_STATE[x]:
                            GUEST_STATE.pop(x)
                    else:
                        GUEST_STATE[x] = {name_: sushi_left}
                        to_remove.append([x, name_])
                
    for x, name, sushi_left in to_modify:
        SUSHI_STATE_ROTATE[x][name] = sushi_left
    for x, name in to_remove:
        del SUSHI_STATE_ROTATE[x][name]
        if not SUSHI_STATE_ROTATE[x]:
            SUSHI_STATE_ROTATE.pop(x)


# 300
def print_answer(t):

    t = int(t)

    rotate(t)
    eat_right_now()

    a = len(GUEST_STATE)
    b = 0

    for k, v in SUSHI_STATE_ROTATE.items():
        for v1, v2 in v.items():
            b += v2

    print(str(a) + ' ' + str(b))



#%%

cnt = 0

while cnt < Q:

    order = ORDERS[cnt]
    
    order_idx = int(order[0])

    if order_idx == 100:
        make_sushi(order[1:])

    elif order_idx == 200:
        guest_comein(order[1:])

    else:
        print_answer(order[1])

    SUSHI_STATE = SUSHI_STATE_ROTATE
    
    cnt += 1