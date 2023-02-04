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


# 负模式参与度计算
def get_negative_participation(object_type_participation_dic, object_count_dic_list, time_slot):
    min_participation = 1  # 设置一个最大参与率
    for object_type in object_type_participation_dic.keys():
        participation = 1 - object_type_participation_dic[object_type] / object_count_dic_list[time_slot][object_type]
        if participation < min_participation:
            min_participation = participation
    return min_participation


# 负模式participation index的计算
def get_negative_participation_index(row_instances, pattern, object_count_dic, time_slot):
    participation_index = 0
    object_type_participation_dic = {}
    for object_type in pattern:
        instance_set = set()
        for row_instance in row_instances:
            for pacop_instance in row_instance:
                if pacop_instance.objectType == object_type:
                    instance_set.add(pacop_instance)
        object_type_participation_dic[object_type] = len(instance_set)
    participation_index = get_negative_participation(object_type_participation_dic, object_count_dic, time_slot)
    return participation_index


# 计算各个正模式的时间参与度
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


# 计算各个负模式的时间参与度
def get_negative_temporal_participation(alone_dic, object_time_slot_count_dic):
    min_temporal_participation = 1
    for pattern in alone_dic.keys():
        appear_times = alone_dic[pattern]
        partial_pattern_A = list(pattern[0])
        partial_pattern_B = list(pattern[1])
        for object_type in partial_pattern_A:
            participation = appear_times / object_time_slot_count_dic[object_type]
            if participation < min_temporal_participation:
                min_temporal_participation = participation
        for object_type in partial_pattern_B:
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
    # larger_table_instance_dic_after_process = table_instance_list_to_dic(copyed_table_instance_list)
    larger_table_instance_dic = table_instance_list_to_dic(copyed_table_instance_list)
    return larger_table_instance_dic  # , larger_table_instance_dic_after_process


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


# for generate the negative pattern
def gen_cand_co_location(k, object_type_list):
    total_pattern = []
    for possible_pattern in itertools.combinations(object_type_list, k):
        possible_pattern = list(possible_pattern)
        possible_pattern.sort()
        total_pattern.append(tuple(possible_pattern))
    return total_pattern


def if_contain(listA, listB):
    for element in listA:
        if element not in listB:
            return False
    return True


def from_positive_pattern_get_negative_pattern(total_pattern, positive_set, all_positive_set, negative_set_list_for_purn,
                                               table_instance, k, time_slot, spatial_prev, object_count_dic_list):
    candinate_sum_negative_set_list = [pattern for pattern in total_pattern if pattern not in positive_set]
    spatial_negative_set_list = []
    for sum_negative_pattern in candinate_sum_negative_set_list:
        sum_negative_pattern = list(sum_negative_pattern)
        for size in range(1, k):
            for partial_pattern_A in itertools.combinations(sum_negative_pattern, size):
                partial_pattern_A = list(partial_pattern_A)
                partial_pattern_B = [i for i in sum_negative_pattern if i not in partial_pattern_A]
                partial_pattern_A.sort()
                partial_pattern_B.sort()
                # 判断PI(A)与PI(B)是否符合条件
                if not (tuple(partial_pattern_A) in all_positive_set[size] and tuple(partial_pattern_B) in all_positive_set[k-size]):
                    continue
                # 对其进行剪枝，也就是比较快速的判断，如果AB'是负模式，B属于BC，则AB'C'也是负模式
                purned_flag = False
                for negative_pattern in negative_set_list_for_purn:
                    if tuple(partial_pattern_A) == negative_pattern[0] and if_contain(list(negative_pattern[1]), partial_pattern_B):
                        spatial_negative_set_list.append((tuple(partial_pattern_A), tuple(partial_pattern_B)))
                        purned_flag = True
                        break
                if purned_flag:
                    continue
                if tuple(sum_negative_pattern) in table_instance:
                    participation_index_A = get_negative_participation_index(table_instance[tuple(sum_negative_pattern)],
                                                                             partial_pattern_A, object_count_dic_list,
                                                                             time_slot)
                    if participation_index_A >= spatial_prev:
                        spatial_negative_set_list.append((tuple(partial_pattern_A), tuple(partial_pattern_B)))
                else:
                    spatial_negative_set_list.append((tuple(partial_pattern_A), tuple(partial_pattern_B)))
    return spatial_negative_set_list


# 重复的代码段有没有办法合并？
def findPNCOP(R, spatial_prev, temporal_prev):
    # spatial_prev = 0.4
    # temporal_prev = 0.4
    # R = 5.1  # 设最小邻近关系的距离

    object_type_list, object_list = load_data_with_time()
    object_count_dic_list, object_time_slot_count_dic = get_object_count(object_type_list, object_list)
    k = 1
    all_time_slots = len(object_list)
    all_positive_set = {}        # 所有的positive frequent set
    size_1_frequent_set_list = []
    for object_type in object_type_list:
        size_1_frequent_set_list.append(tuple(object_type))
    all_positive_set[k] = size_1_frequent_set_list
    current_positive_set = []    # 记录一个k范围下的所有set，为验证下一个k范围是否仍有可能有域更大的频繁项集
    candidate_positive_set_time_slot_record = {}  # 候选的positive frequent set在各个time slot上的分布
    current_frequent_table_instance = {}  # 记录一个k范围下的所有table instance(用于为下一个k生成table instance)，
                                          # 注意这个先在每个time slot下记录，之后在经过时间验证后去除不符合的频繁项集对应的table instance
    all_negative_set = {}       # 所有的negative frequent set
    negative_set_dic_for_purn = {}  # 用于剪枝
    for tt in range(all_time_slots):
        negative_set_dic_for_purn[tt] = []
    current_negative_set = []
    candidate_negative_set_time_slot_record = {}
    while True:
        if k == len(object_type_list):
            break
        k += 1
        candidate_positive_set_time_slot_record = {}
        candidate_negative_set_time_slot_record = {}
        current_positive_set = []
        current_negative_set = []
        total_pattern = gen_cand_co_location(k, object_type_list)
        for t in range(all_time_slots):
            print("k:{} t:{}".format(k, t))
            if k == 2:
                larger_table_instance_dic = create_size2_table_instance_one_slot(object_list, R, t)
                # original_larger_table_instance_dic = larger_table_instance_dic
            else:
                # original_larger_table_instance_dic,
                larger_table_instance_dic = generate_larger_table_instance(current_frequent_table_instance[t], k)
            frequent_table_instance, frequent_set = from_table_instance_get_frequent_set(larger_table_instance_dic,
                                                                                         object_count_dic_list,
                                                                                         spatial_prev,
                                                                                         t)
            print("frequent set:{}".format(frequent_set))
            # print("original table instance:{}".format(original_larger_table_instance_dic))
            print("table instance:{}".format(larger_table_instance_dic))
            print("frequent table instance:{}".format(frequent_table_instance))
            # if not k == 2:
            #     prev_frequent_table_instance = current_frequent_table_instance[t]
            current_frequent_table_instance[t] = frequent_table_instance
            for spatial_pattern in frequent_set:
                if spatial_pattern in candidate_positive_set_time_slot_record:
                    candidate_positive_set_time_slot_record[spatial_pattern] += 1
                else:
                    candidate_positive_set_time_slot_record[spatial_pattern] = 1
            spatial_negative_set_list = from_positive_pattern_get_negative_pattern(total_pattern, frequent_set,
                                                                              all_positive_set, negative_set_dic_for_purn[t],
                                                                              larger_table_instance_dic,
                                                                              k, t, spatial_prev, object_count_dic_list)
            print("spatial_negative_set_list:{}".format(spatial_negative_set_list))
            for spatial_negative_pattern in spatial_negative_set_list:
                if spatial_negative_pattern in candidate_negative_set_time_slot_record:
                    candidate_negative_set_time_slot_record[spatial_negative_pattern] += 1
                else:
                    candidate_negative_set_time_slot_record[spatial_negative_pattern] = 1
            negative_set_dic_for_purn[t].extend(spatial_negative_set_list)
        # print(candidate_positive_set_time_slot_record)
        print("k:{} candidate_negative_set_time_slot_record:{}".format(k, candidate_negative_set_time_slot_record))
        print("------------------------------------------------")
        # print(candidate_negative_set_time_slot_record)
        # 处理正模式的时间维度信息
        for key in candidate_positive_set_time_slot_record.keys():
            alone_dic = {key: candidate_positive_set_time_slot_record[key]}
            temporal_participation_index = get_temporal_participation(alone_dic, object_time_slot_count_dic)
            if temporal_participation_index >= temporal_prev:
                current_positive_set.append(tuple(key))

        # 处理负模式的时间维度信息
        for key in candidate_negative_set_time_slot_record.keys():
            alone_dic = {key: candidate_negative_set_time_slot_record[key]}
            temporal_participation_index = get_negative_temporal_participation(alone_dic, object_time_slot_count_dic)
            if temporal_participation_index >= temporal_prev:
                current_negative_set.append(tuple(key))

        # 对不满足时空模式的做剪枝，是不是不应该做
        # for t in current_frequent_table_instance:
        #     for key in list(current_frequent_table_instance[t]):
        #         if list(key) not in current_positive_set:
        #             current_frequent_table_instance[t].pop(key)
        all_positive_set[k] = current_positive_set
        all_negative_set[k] = current_negative_set
    for pattern_size in all_positive_set:
        if not pattern_size == 1:
            print("pattern size: {}".format(pattern_size))
            for st in all_positive_set[pattern_size]:
                print(st)
    print("-------------------------------------")
    print("negative set: ")
    for pattern_size in all_negative_set:
        if not pattern_size == 1:
            print("pattern size: {}".format(pattern_size))
            for st in all_negative_set[pattern_size]:
                print(st)
    return all_negative_set, all_positive_set


if __name__ == '__main__':
    findPNCOP()
