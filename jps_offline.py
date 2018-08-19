from matrix_data import map_matrix

class jps_node(object):
    def __init__(self):
        self.lu = 0
        self.u = 0
        self.ru = 0
        self.l = 0
        self.r = 0
        self.ld = 0
        self.d = 0
        self.rd = 0
    
    def __repr__(self):
        return "(u: " + str(self.u) + ", l: " + str(self.l) + ", r: " + str(self.r) + ", d: " + str(self.d) + ", lu: " + str(self.lu) + ", ru: " + str(self.ru) + ", rd: " + str(self.rd) + ", ld: " + str(self.ld) + ")"

    def __add__(self, node):
        ret_node = jps_node()
        ret_node.lu = self.lu + node.lu
        ret_node.u = self.u + node.u
        ret_node.ru = self.ru + node.ru
        ret_node.l = self.l + node.l
        ret_node.r = self.r + node.r
        ret_node.ld = self.ld + node.ld
        ret_node.d = self.d + node.d
        ret_node.rd = self.rd + node.rd
        return ret_node

    def is_emtpy(self):
        return not (self.lu or self.u or self.ru or self.l or self.r or self.ld or self.d or self.rd)

class primary_jps_node(object):
    def __init__(self):
        self.u = False
        self.l = False
        self.r = False
        self.d = False
    
    def __repr__(self):
        return "(u: " + str(self.u) + ", l: " + str(self.l) + ", r: " + str(self.r) + ", d: " + str(self.d) + ")"


def is_invalid(i, j):
    return i < 0 or j < 0 or i >= len(map_matrix) or j >= len(map_matrix[0])

def is_obstacle(i, j):
    if i < 0 or j < 0 or i >= len(map_matrix) or j >= len(map_matrix[0]):
        return False
    return map_matrix[i][j] > 0


def init_matrix(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix):
    for i in range(0, len(map_matrix)):
        primary_jp_row = []
        straight_jp_row = []
        diagnal_jp_row = []
        jp_row = []
        for j in range(0, len(map_matrix[0])):
            primary_jp_row.append(primary_jps_node())
            straight_jp_row.append(jps_node())
            diagnal_jp_row.append(jps_node())
            jp_row.append(jps_node())
        primary_jp_matrix.append(primary_jp_row)
        straight_jp_matrix.append(straight_jp_row)
        diagnal_jp_matrix.append(diagnal_jp_row)
        jp_matrix.append(jp_row)


# calculate primary jp
def calculate_primary_jp(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix):
    for i in range(0, len(primary_jp_matrix)):
        for j in range(0, len(primary_jp_matrix[0])):
            # check is obs
            if is_obstacle(i, j):
                continue
            # from up
            primary_jp_matrix[i][j].u = (not is_obstacle(i-1, j) and is_obstacle(i-1, j-1)) or (not is_obstacle(i+1, j) and is_obstacle(i+1, j-1))
            # from left
            primary_jp_matrix[i][j].l = (not is_obstacle(i, j-1) and is_obstacle(i-1, j-1)) or (not is_obstacle(i, j+1) and is_obstacle(i-1, j+1))
            # from right
            primary_jp_matrix[i][j].r = (not is_obstacle(i, j-1) and is_obstacle(i+1, j-1)) or (not is_obstacle(i, j+1) and is_obstacle(i+1, j+1))
            # from down
            primary_jp_matrix[i][j].d = (not is_obstacle(i-1, j) and is_obstacle(i-1, j+1)) or (not is_obstacle(i+1, j) and is_obstacle(i+1, j+1))

    # print(primary_jp_matrix)
    # for primary_jp_row in primary_jp_matrix:
    #     print(primary_jp_row)


def calculate_straight_jp(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix):
    # calculate straight jp
    for i in range(0, len(straight_jp_matrix)):
        for j in range(0, len(straight_jp_matrix[0])):
            # to up
            k = j - 1
            while k >= 0:
                if is_obstacle(i, k):
                    break
                if primary_jp_matrix[i][k].d:
                    straight_jp_matrix[i][j].u = j - k
                    break
                k -= 1

            # to left
            k = i - 1
            while k >= 0:
                if is_obstacle(k, j):
                    break
                if primary_jp_matrix[k][j].r:
                    straight_jp_matrix[i][j].l = i - k
                    break
                k -= 1
            
            # to right
            k = i + 1
            while k < len(primary_jp_matrix):
                if is_obstacle(k, j):
                    break
                if primary_jp_matrix[k][j].l:
                    straight_jp_matrix[i][j].r = k - i
                    break
                k += 1
            
            # to down
            k = j + 1
            while k < len(primary_jp_matrix[0]):
                if is_obstacle(i, k):
                    break
                if primary_jp_matrix[i][k].u:
                    straight_jp_matrix[i][j].d = k - j
                    break
                k += 1

    # print(straight_jp_matrix)
    # for straight_jp_row in straight_jp_matrix:
    #     print(straight_jp_row)


def calculate_diagnal_jp(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix):
    # calculate straight jp
    for i in range(0, len(diagnal_jp_matrix)):
        for j in range(0, len(diagnal_jp_matrix[0])):
            # lu
            k = 1
            while not is_obstacle(i-k, j-k) and not is_invalid(i-k, j-k):
                if straight_jp_matrix[i-k][j-k].l or straight_jp_matrix[i-k][j-k].u:
                    diagnal_jp_matrix[i][j].lu = k
                    break
                k += 1
            
            # ru
            k = 1
            while not is_obstacle(i+k, j-k) and not is_invalid(i+k, j-k):
                if straight_jp_matrix[i+k][j-k].r or straight_jp_matrix[i+k][j-k].u:
                    diagnal_jp_matrix[i][j].ru = k
                    break
                k += 1
            
            # ld
            k = 1
            while not is_obstacle(i-k, j+k) and not is_invalid(i-k, j+k):
                if straight_jp_matrix[i-k][j+k].l or straight_jp_matrix[i-k][j+k].d:
                    diagnal_jp_matrix[i][j].ld = k
                    break
                k += 1
            
            # rd
            k = 1
            while not is_obstacle(i+k, j+k) and not is_invalid(i+k, j+k):
                if straight_jp_matrix[i+k][j+k].r or straight_jp_matrix[i+k][j+k].d:
                    diagnal_jp_matrix[i][j].rd = k
                    break
                k += 1
    # for diagnal_jp_matrix in diagnal_jp_matrix:
    #     print(diagnal_jp_matrix)


def add_wall_distance(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix):
    for i in range(0, len(jp_matrix)):
        for j in range(0, len(jp_matrix[0])):
            # combine straight_matrix and diagnal_matrix
            jp_matrix[i][j] = straight_jp_matrix[i][j] + diagnal_jp_matrix[i][j]

            # lu
            if jp_matrix[i][j].lu <= 0:
                k = 1
                while not is_obstacle(i-k, j-k) and not is_invalid(i-k, j-k):
                    jp_matrix[i][j].lu = -k
                    k += 1
            # u
            if jp_matrix[i][j].u <= 0:
                k = 1
                while not is_obstacle(i, j-k) and not is_invalid(i, j-k):
                    jp_matrix[i][j].u = -k
                    k += 1
            # ru
            if jp_matrix[i][j].ru <= 0:
                k = 1
                while not is_obstacle(i+k, j-k) and not is_invalid(i+k, j-k):
                    jp_matrix[i][j].ru = -k
                    k += 1
            # l
            if jp_matrix[i][j].l <= 0:
                k = 1
                while not is_obstacle(i-k, j) and not is_invalid(i-k, j):
                    jp_matrix[i][j].l = -k
                    k += 1
            # r
            if jp_matrix[i][j].r <= 0:
                k = 1
                while not is_obstacle(i+k, j) and not is_invalid(i+k, j):
                    jp_matrix[i][j].r = -k
                    k += 1
            # ld
            if jp_matrix[i][j].ld <= 0:
                k = 1
                while not is_obstacle(i-k, j+k) and not is_invalid(i-k, j+k):
                    jp_matrix[i][j].ld = -k
                    k += 1
            # d
            if jp_matrix[i][j].d <= 0:
                k = 1
                while not is_obstacle(i, j+k) and not is_invalid(i, j+k):
                    jp_matrix[i][j].d = -k
                    k += 1
            # rd
            if jp_matrix[i][j].rd <= 0:
                k = 1
                while not is_obstacle(i+k, j+k) and not is_invalid(i+k, j+k):
                    jp_matrix[i][j].rd = -k
                    k += 1


if __name__ == '__main__':
    # init jp matrix
    primary_jp_matrix = []
    straight_jp_matrix = []
    diagnal_jp_matrix = []
    jp_matrix = []

    init_matrix(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix)
    calculate_primary_jp(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix)
    calculate_straight_jp(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix)
    calculate_diagnal_jp(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix)
    add_wall_distance(primary_jp_matrix, straight_jp_matrix, diagnal_jp_matrix, jp_matrix)

    for jp_matrix in jp_matrix:
        print(jp_matrix)