"""
设置两层循环，外层循环改变k的值，内层循环改变time slot的值
内层循环（time slot）根据table instance生成可能的frequent set，并计算spatial participation index来进行筛选
外层循环存储一个key为frequent set的字典来记录每个frequent set出现的次数，以此来计算temporal participation index
"""
import itertools

from pncop.pncop_algorithm.loadData import load_data_with_time


# 获取每个实例在每个时间片出现的次数
# object_count_dic_list: 一维是时间维度，二维是每种类别在该时间出现的次数(list内嵌入字典)
# object_time_slot_count_dic: 一个key是objectType类型, value是在几个时间片出现的字典
def get_object_count(object_type_list, object_list):
    object_count_dic_list = [{} for num in range(len(object_list))]
    object_time_slot_count_dic = {}
    for pacop_object_type in object_type_list:
        object_time_slot_count_dic[pacop_object_type] = 0
    for i in range(len(object_list)):
        for pacop_object_type in object_type_list:
            object_count_dic_list[i][pacop_object_type] = 0
        for pacop_object in object_list[i]:
            object_count_dic_list[i][pacop_object.objectType] += 1
        for key in object_count_dic_list[i]:
            if not object_count_dic_list[i][key] == 0:
                if key in object_time_slot_count_dic:
                    object_time_slot_count_dic[key] += 1
                else:
                    object_time_slot_count_dic[key] = 1
    return object_count_dic_list, object_time_slot_count_dic


# 判断实例是否相邻
def is_neighbor(object1, object2, R):
    distance = ((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2) ** 0.5
    if distance <= R:
        return 1
    else:
        return 0


# 计算各个模式的空间参与度
# frequent_object_dic: key为类型,value为在特定pattern的出现次数。
def get_spatial_participation(frequent_object_dic, object_count_dic_list, time_slot):
    min_spatial_participation = 1  # 设置一个最大参与率
    for object_type in frequent_object_dic.keys():
        participation = frequent_object_dic[object_type] / object_count_dic_list[time_slot][object_type]
        if participation < min_spatial_participation:
            min_spatial_participation = participation
    return min_spatial_participation


# 计算各个模式的时间参与度
# pattern_time_dic: key为pattern，value为在时间维度上的存在周期
def get_temporal_participation(pattern_time_dic, object_time_slot_count_dic):
    min_temporal_participation = 1
    for pattern in pattern_time_dic.keys():
        appear_times = pattern_time_dic[pattern]
        pattern = list(pattern)
        for object_type in pattern:
            participation = appear_times / object_time_slot_count_dic[object_type]
            if participation < min_temporal_participation:
                min_temporal_participation = participation
    return min_temporal_participation


def create_size2_table_instance_one_slot(object_list, R, time_slot):
    size2_table_instance_list = []
    for i in range(len(object_list[time_slot]) - 1):
        for j in range(i, len(object_list[time_slot])):
            if object_list[time_slot][i].objectType != object_list[time_slot][j].objectType and \
                    is_neighbor(object_list[time_slot][i], object_list[time_slot][j], R):
                size2_row_instance = [object_list[time_slot][i], object_list[time_slot][j]]
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
def from_table_instance_get_frequent_set(table_instance_dic, object_count_dic_list, spatial_prev, time_slot):
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
        participation = get_spatial_participation(object_type_participation_dic, object_count_dic_list, time_slot)
        if participation >= spatial_prev:
            frequent_table_instance[key] = table_instance_dic[key]
            frequent_set.append(key)
    return frequent_table_instance, frequent_set


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


# 重复的代码段有没有办法合并？
def findPACOP(R, spatial_prev, temporal_prev):
    # spatial_prev = 0.4
    # temporal_prev = 0.4
    # R = 5.1  # 设最小邻近关系的距离为16

    object_type_list, object_list = load_data_with_time()
    object_count_dic_list, object_time_slot_count_dic = get_object_count(object_type_list, object_list)
    k = 2
    all_time_slots = len(object_list)
    candidate_frequent_set = {}  # 候选的frequent set（所有time slot下经过spatial验证的），等待接受temporal验证
    all_frequent_set = {}        # 所有frequent set
    current_frequent_set = []    # 记录一个k范围下的所有set，为验证下一个k范围是否仍有可能有域更大的频繁项集
    current_frequent_table_instance = {}  # 记录一个k范围下的所有table instance(用于为下一个k生成table instance)，
                                          # 注意这个先在每个time slot下记录，之后在经过时间验证后去除不符合的频繁项集对应的table instance
    for t in range(all_time_slots):
        table_instance = create_size2_table_instance_one_slot(object_list, R, t)
        frequent_table_instance, frequent_set = from_table_instance_get_frequent_set(table_instance,
                                                                                     object_count_dic_list,
                                                                                     spatial_prev,
                                                                                     t)
        print("k: {} t: {} frequent set: {}".format(k, t, frequent_set))
        current_frequent_table_instance[t] = frequent_table_instance
        for spatial_pattern in frequent_set:
            if spatial_pattern in candidate_frequent_set:
                candidate_frequent_set[spatial_pattern] += 1
            else:
                candidate_frequent_set[spatial_pattern] = 1
    for key in candidate_frequent_set.keys():
        alone_dic = {key: candidate_frequent_set[key]}
        temporal_participation_index = get_temporal_participation(alone_dic, object_time_slot_count_dic)
        if temporal_participation_index >= temporal_prev:
            current_frequent_set.append(list(key))
    for t in current_frequent_table_instance:
        for key in list(current_frequent_table_instance[t]):
            if list(key) not in current_frequent_set:
                current_frequent_table_instance[t].pop(key)
    all_frequent_set[k] = current_frequent_set

    while True:
        k += 1
        possible_pattern_list = get_possible_pattern(current_frequent_set)
        if len(possible_pattern_list) == 0:
            break
        candidate_frequent_set = {}
        current_frequent_set = []
        for t in range(all_time_slots):
            larger_table_instance_dic = generate_larger_table_instance(current_frequent_table_instance[t], k)
            frequent_table_instance, frequent_set = from_table_instance_get_frequent_set(larger_table_instance_dic,
                                                                                         object_count_dic_list,
                                                                                         spatial_prev,
                                                                                         t)
            print("k: {} t: {} frequent set: {}".format(k, t, frequent_set))
            current_frequent_table_instance[t] = frequent_table_instance
            for spatial_pattern in frequent_set:
                if spatial_pattern in candidate_frequent_set:
                    candidate_frequent_set[spatial_pattern] += 1
                else:
                    candidate_frequent_set[spatial_pattern] = 1

        for key in candidate_frequent_set.keys():
            alone_dic = {key: candidate_frequent_set[key]}
            temporal_participation_index = get_temporal_participation(alone_dic, object_time_slot_count_dic)
            if temporal_participation_index >= temporal_prev:
                current_frequent_set.append(list(key))

        for t in current_frequent_table_instance:
            for key in list(current_frequent_table_instance[t]):
                if list(key) not in current_frequent_set:
                    current_frequent_table_instance[t].pop(key)
        all_frequent_set[k] = current_frequent_set

    for pattern_size in all_frequent_set:
        print("pattern size: {}".format(pattern_size))
        for st in all_frequent_set[pattern_size]:
            print(st)
    return all_frequent_set


if __name__ == '__main__':
    findPACOP(5.1, 0.4, 0.4)