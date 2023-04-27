import itertools

# from pncop.pncop_algorithm.loadData import load_data
from loadData import load_data


# 获取每个实例出现的次数
def get_object_count(object_type_list, object_list):
    object_count_dic = {}
    for pacop_object_type in object_type_list:
        object_count_dic[pacop_object_type] = 0
        for pacop_object in object_list:
            if pacop_object.objectType == pacop_object_type:
                object_count_dic[pacop_object_type] += 1
    return object_count_dic


# 判断实例是否相邻
def is_neighbor(object1, object2, R):
    distance = ((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2) ** 0.5
    if distance <= R:
        return 1
    else:
        return 0


# 计算各个模式的参与度
# frequent_object_dic: key为类型,value为在特定pattern的出现次数。
def get_participation(frequent_object_dic, object_count_dic):
    min_participation = 1  # 设置一个最大参与率
    for object_type in frequent_object_dic.keys():
        participation = frequent_object_dic[object_type] / object_count_dic[object_type]
        if participation < min_participation:
            min_participation = participation
    return min_participation


# 根据实例列表和空间邻近关系生成二阶表实例
def create_size2_table_instance(object_list, R):
    size2_table_instance_list = []
    for i in range(len(object_list) - 1):
        for j in range(i, len(object_list)):
            if object_list[i].objectType != object_list[j].objectType and is_neighbor(object_list[i], object_list[j], R):
                size2_row_instance = [object_list[i], object_list[j]]
                size2_table_instance_list.append(size2_row_instance)
    return table_instance_list_to_dic(size2_table_instance_list)


def table_instance_list_to_dic(table_instance_list):
    table_instance_dic = {}
    for row_instance in table_instance_list:
        pacop_object_type_list = []
        for pacop_object in row_instance:
            pacop_object_type_list.append(pacop_object.objectType)
        pacop_object_type_list.sort()
        pacop_object_type_tuple = tuple(pacop_object_type_list)
        row_instance.sort(key=lambda obj: obj.objectType)
        if pacop_object_type_tuple not in table_instance_dic.keys():
            table_instance_dic[pacop_object_type_tuple] = [row_instance]
        else:
            table_instance_dic[pacop_object_type_tuple].append(row_instance)
    return table_instance_dic


# 难点！
# 由k-1阶满足参与率的表实例生成k阶粗表实例集
# T是满足参与率的k阶表"实例表"
# table_instance_dic是上一个size频繁模式的frequent_table_instance，k是频繁模式的size
# Question: 为啥会出现重复项
def generate_larger_table_instance(table_instance_dic, k):
    larger_table_instance_list = []
    keys = list(table_instance_dic.keys())
    keys.sort()
    for i in range(len(keys) - 1):
        for j in range(i + 1, len(keys)):
            # 考虑前几项相同，经排序后如果前几项不相同则表示肯定没有关联
            if keys[j][:-1] == keys[i][:-1]:
                for row_instance1 in table_instance_dic[keys[i]]:
                    for row_instance2 in table_instance_dic[keys[j]]:
                        if row_instance1[:-1] == row_instance2[:-1]:
                            larger_row_instance = []
                            larger_row_instance.extend(row_instance1)
                            larger_row_instance.append(row_instance2[-1])
                            larger_table_instance_list.append(larger_row_instance)
            else:
                break

    # 判断是否在k-1阶模式中存在频繁模式
    # Question: 拷贝是因为遍历的时候不适合做删除吗？
    copyed_table_instance_list = larger_table_instance_list.copy()
    for row_instance in larger_table_instance_list:
        for less_size_row_instance in itertools.combinations(row_instance, k - 1):
            less_size_row_instance = list(less_size_row_instance)
            # 判断实例种类组合是否为频繁项集，以及实例间的距离是否符合条件
            less_size_frequent_set = []
            for i in range(len(less_size_row_instance)):
                less_size_frequent_set.append(less_size_row_instance[i].objectType)
            less_size_frequent_set.sort()
            less_size_frequent_set = tuple(less_size_frequent_set)
            # Question: 判断实例列表是否in的时候可能会有问题？
            if less_size_frequent_set not in table_instance_dic.keys() or less_size_row_instance not in table_instance_dic[less_size_frequent_set]:
                copyed_table_instance_list.remove(row_instance)
                break
    larger_table_instance_dic = table_instance_list_to_dic(copyed_table_instance_list)
    return larger_table_instance_dic


# 验证参与度是否大于阈值，将符合条件的放入到集合中
# 参与度 = 实例在row instance中出现的次数 / 该类别总的实例个数
def from_table_instance_get_frequent_set(table_instance_dic, object_count_dic, min_prev):
    frequent_set = []
    frequent_table_instance = {}
    keys = list(table_instance_dic.keys())  # 如(A,B)
    keys.sort()
    # Question: 这个部分有问题
    for key in keys:
        object_type_participation_dic = {}
        for object_type in key:
            # 下标对应，需要row instance是有序的
            instance_set = set()
            for row_instance in table_instance_dic[key]:
                for pacop_instance in row_instance:
                    if pacop_instance.objectType == object_type:
                        instance_set.add(pacop_instance)
            object_type_participation_dic[object_type] = len(instance_set)
        participation = get_participation(object_type_participation_dic, object_count_dic)
        if participation >= min_prev:
            frequent_table_instance[key] = table_instance_dic[key]
            frequent_set.append(key)
    return frequent_table_instance, frequent_set


# 检查是否还有别的可能组合
def get_possible_pattern(frequent_set):
    possible_pattern_list = []
    for i in range(len(frequent_set)):
        for j in range(i + 1, len(frequent_set)):
            if frequent_set[j][:-1] == frequent_set[i][:-1]:
                temp = []
                temp.extend(frequent_set[i])
                temp.append(frequent_set[j][-1])
                possible_pattern_list.append(temp)
    return possible_pattern_list

"""
    # test for using tuple as keys of dictionary
    # dic = {("A", "B"): 1, ("B", "C"): 2}
    # dic[('B', 'C')] += 1
    # print(dic)

    # tuple and list
    # l = [1,3,2]
    # l.sort()
    # l = tuple(l)
    # print(l)
    # print(type(l))

    # tuple遍历
    # t = (1,2,3)
    # for i in t:
    #     print(i)
"""
def findColocationSet(R, spatial_prev):
    object_type_list, object_list = load_data()
    object_count = get_object_count(object_type_list, object_list)
    k = 2
    table_instance = create_size2_table_instance(object_list, R)

    # the code is for check
    # print("the table instance of size 2")
    # c = list(table_instance.keys())
    # c.sort()
    # print(c)

    frequent_table_instance, frequent_set = from_table_instance_get_frequent_set(table_instance, object_count, min_prev)
    print("frequent_table_instance of size {}:".format(k))
    for key in frequent_table_instance.keys():
        print("the table instance of frequent pattern {}: ".format(key))
        for row_instance in frequent_table_instance[key]:
            temp_list = []
            for item in row_instance:
                temp_list.append(str(item.objectType) + str(item.objectId))
            print(temp_list, end=" ")
        print("")
    # print("the frequent_table_instance of size 2")
    # for i in frequent_table_instance.keys():
    #     print(i, frequent_table_instance[i])
    # print("the frequent set of size 2:")
    # print(frequent_set)
    # Question: 循环终止的原理
    while True:
        k += 1
        possible_pattern_list = get_possible_pattern(frequent_set)
        if len(possible_pattern_list) == 0:
            break
        # print("C{}".format(k))
        # print(C)
        larger_table_instance_dic = generate_larger_table_instance(frequent_table_instance, k)
        print("k:{} larger_table_instance_dic:{}".format(k, larger_table_instance_dic))
        # test cases
        # print("the test cases")
        # for key in larger_table_instance_dic.keys():
        #     print("the table instance of frequent pattern {}: ".format(key))
        #     for row_instance in larger_table_instance_dic[key]:
        #         temp_list = []
        #         for item in row_instance:
        #             temp_list.append(str(item.objectType) + str(item.objectId))
        #         print(temp_list, end=" ")
        #     print("")

        frequent_table_instance, frequent_set = from_table_instance_get_frequent_set(larger_table_instance_dic, object_count, min_prev)
        print("k:{} frequent_table_instance:{}".format(k, frequent_table_instance))
        if bool(frequent_table_instance):
            print("frequent_table_instance of size {}:".format(k))
            for key in frequent_table_instance.keys():
                print("the table instance of frequent pattern {}: ".format(key))
                for row_instance in frequent_table_instance[key]:
                    temp_list = []
                    for item in row_instance:
                        temp_list.append(str(item.objectType) + str(item.objectId))
                    print(temp_list, end=" ")
                print("")
        if bool(frequent_set):
            print("frequent set {}: ".format(k))
            print(frequent_set)


if __name__ == '__main__':
    min_prev = 0.4  # 最小参与度
    R = 5.1  # 设最小邻近关系的距离为16
    findColocationSet(R, min_prev)

