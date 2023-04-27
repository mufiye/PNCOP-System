import time

import numpy as np
import pandas as pd


class pacaop_object:
    def __init__(self, objectType, objectId, x, y):
        self.objectType = objectType
        self.objectId = objectId
        self.x = x
        self.y = y


# first try only for spatial data mining
def load_data():
    # pd.set_option('display.notebook_repr_html', False)
    # 获取所有的表（结构为字典）
    # for sys
    sheets = pd.read_excel(io='/Users/mufiye/data-mining/PNCOP_sys/pncop_backend/pncop/datasets/colocationdata.xls', sheet_name=[0])
    # 获取其中的一个表
    sheet_1 = sheets[0]
    # print(sheet_1.values)

    # 获取类别list
    object_type_list = list(set(sheet_1.values[:, 0]))

    # 遍历
    object_list = []
    for i in range(sheet_1.values.shape[0]):
        pacop_object = pacaop_object(sheet_1.values[i, 0], int(sheet_1.values[i, 1]), sheet_1.values[i, 2], sheet_1.values[i, 3])
        object_list.append(pacop_object)
    object_type_list.sort()
    # print(object_type_list)
    return object_type_list, object_list


def load_data_with_time():
    sheets = pd.read_excel(io="/Users/mufiye/data-mining/PNCOP_sys/pncop_backend/pncop/datasets/模拟数据集.xls", sheet_name=[0, 1, 2, 3])
    object_type_set = set()
    object_list = []
    for i in range(4):
        time_slot_object_list = []
        for j in range(sheets[i].values.shape[0]):
            object_type_set.add(sheets[i].values[j, 0])
            pacop_object = pacaop_object(sheets[i].values[j, 0], int(sheets[i].values[j, 1]), sheets[i].values[j, 2], sheets[i].values[j, 3])
            time_slot_object_list.append(pacop_object)
        object_list.append(time_slot_object_list)
    object_type_list = list(object_type_set)
    object_type_list.sort()

    # print("in load data")
    # for time_slot_object_list in object_list:
    #     for ob in time_slot_object_list:
    #         print("{}{}".format(ob.objectType, ob.objectId))
    # print("end in load data")
    return object_type_list, object_list


def load_real_data_with_time():
    # ！！！放入后端框架时注意路径命名
    sheet = pd.read_csv('pncop/datasets/Crimes_2022.csv')
    sheet = sheet.dropna(how='any')
    # print(sheet.index)
    # print(sheet.index.names)
    #
    # print(sheet.columns)
    # print(sheet.columns.name)
    #
    # print(sheet)
    # ---------------------------
    object_type_set = set()
    object_list = []
    time_slot = 1
    instance_id = 1
    temp_object_list = []
    # for i in range(2):
    #     print(int(sheet.values[i, 3]))
    time_start = time.time()
    for i in range(sheet.values.shape[0]):
        if not time_slot == int(sheet.values[i, 3]):
            time_slot += 1
            instance_id = 1
            object_list.append(temp_object_list)
            temp_object_list = []
        object_type_set.add(sheet.values[i, 0])
        pacop_object = pacaop_object(sheet.values[i, 0], instance_id, sheet.values[i, 1], sheet.values[i, 2])
        temp_object_list.append(pacop_object)
        instance_id += 1
    object_type_list = list(object_type_set)
    object_type_list.sort()
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    return object_type_list, object_list


def main():
    object_type_list, object_list = load_data()
    print(object_type_list)
    for pacop_object in object_list:
        print(pacop_object.objectType, pacop_object.objectId, pacop_object.x, pacop_object.y)
    # object_type_list, object_list = load_real_data_with_time()
    # print(object_type_list)
    # print(object_list)


if __name__ == "__main__":
    main()