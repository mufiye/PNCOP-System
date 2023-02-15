import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pandas import Series, DataFrame
import math

from pncop.pncop_algorithm.loadData import load_data, load_data_with_time
from threading import Thread
import traceback


# class MyThread(Thread):
#     def __init__(self, target=None, args=()):
#         super(MyThread, self).__init__()
#         self._target = target
#         self._args = args
#         # 先在__init__中声明 _result 变量
#         self._result = None

#     def run(self):
#         try:
#             if self._target:
#             	# 此处做修改
#                 self._result = self._target(self._args)
#             else:
#                 print('target is None')
#         finally:
#             # Avoid a refcycle if the thread is running a function with
#             # an argument that has a member that points to the thread.
#             del self._target, self._args

# 	# 添加get_result()成员函数
#     def get_result(self):
#         try:
#             if self._result:
#                 return self._result
#         except Exception as e:
#             traceback.print_exc()
#             return None

# def distance_R(x1,y1,x2,y2,R):
#     dis = math.sqrt((x2-x1)**2 + (y2-y1)**2)
#     if dis <= R:
#         return True
#     else:
#         return False

# def original_draw_data(df,R):
#     #映射成A1,A2...
#     df['CH_instance'] = df['CH'].map(str) + df['instance'].map(str)
#      #遍历数据，绘图
#     fig, ax = plt.subplots(figsize=(12, 7))
#     for i in range(len(df)):
#         if df['CH'][i]== 'A':
#             ax.scatter(df['X'][i],df['Y'][i],marker='8',c=(0.4940,0.1840,0.5560),s=100, alpha=0.4)
#         elif df['CH'][i] == 'B':
#             ax.scatter(df['X'][i],df['Y'][i],marker='o',c=([0.6350,0.0780,0.1840]),s=100, alpha=0.4)
#         elif df['CH'][i] == 'C':
#             ax.scatter(df['X'][i],df['Y'][i],marker='^',c='orange',s=100, alpha=0.4)
#         else:
#             ax.scatter(df['X'][i],df['Y'][i], marker='s',  c='blue',s=100, alpha=0.4)
#         ax.annotate(df['CH_instance'][i], (df['X'][i], df['Y'][i]))
#         # print(df['X'][i],df['Y'][i])
#     #连接距离小于R的点
#     for k in range(len(df)-1):
#         for m in range(k+1,len(df)):
#             if distance_R(df['X'][k], df['Y'][k], df['X'][m], df['Y'][m], R):
#                 ax.plot([df['X'][k],df['X'][m]],[df['Y'][k],df['Y'][m]])
#     plt.show()


def is_neighbor_in_points(object1, object2, R):
    distance = ((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2) ** 0.5
    if distance <= R:
        return True
    else:
        return False


def draw_single_series_data(R):
    object_type_list, object_list = load_data()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # plt.use('AGG')
    matplotlib.use("AGG")
    plt.figure(figsize=(3, 3))
    for item in object_list:
        if item.objectType == 'A':
            plt.scatter(item.x, item.y, marker='8', c='yellow', s=100, alpha=0.4)
        elif item.objectType == 'B':
            plt.scatter(item.x, item.y, marker='o', c='red', s=100, alpha=0.4)
        elif item.objectType == 'C':
            plt.scatter(item.x, item.y, marker='^', c='orange', s=100, alpha=0.4)
        else:
            plt.scatter(item.x, item.y, marker='s', c='blue', s=100, alpha=0.4)
        plt.annotate(item.objectType + str(item.objectId), (item.x, item.y))
    for i in range(len(object_list) - 1):
        for j in range(i, len(object_list)):
            if is_neighbor_in_points(object_list[i], object_list[j], R) and \
                    object_list[i].objectType != object_list[j].objectType:
                x_temp = [object_list[i].x, object_list[j].x]
                y_temp = [object_list[i].y, object_list[j].y]
                plt.plot(x_temp, y_temp, c='black')
    plt.savefig('/Users/mufiye/data-mining/PNCOP_sys/pncop_backend/images/single_time_series.png')


def draw_multiple_series_data(R):
    object_type_list, object_list = load_data_with_time()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    matplotlib.use("AGG")  # use the backend to avoid error
    plt.figure(figsize=(12, 3))

    for index in range(len(object_list)):
        subplt = plt.subplot(1, len(object_list), index + 1)
        for item in object_list[index]:
            if item.objectType == 'A':
                subplt.scatter(item.x, item.y, marker='8', c='yellow', s=100, alpha=0.4)
            elif item.objectType == 'B':
                subplt.scatter(item.x, item.y, marker='o', c='red', s=100, alpha=0.4)
            elif item.objectType == 'C':
                subplt.scatter(item.x, item.y, marker='^', c='orange', s=100, alpha=0.4)
            else:
                subplt.scatter(item.x, item.y, marker='s', c='blue', s=100, alpha=0.4)
            subplt.annotate(item.objectType + str(item.objectId), (item.x, item.y))
        for i in range(len(object_list[index]) - 1):
            for j in range(i, len(object_list[index])):
                if is_neighbor_in_points(object_list[index][i], object_list[index][j], R) and \
                        object_list[index][i].objectType != object_list[index][j].objectType:
                    x_temp = [object_list[index][i].x, object_list[index][j].x]
                    y_temp = [object_list[index][i].y, object_list[index][j].y]
                    subplt.plot(x_temp, y_temp, c='black')
    plt.savefig('/Users/mufiye/data-mining/PNCOP_sys/pncop_backend/images/multiple_time_series.png')

# def encapsulate_draw_single_series_data(R):
#     t = MyThread(target=draw_single_series_data, args=R)
#     t.start()
#     t.join()


# def encapsulate_draw_multiple_series_data(R):
#     t = MyThread(target=draw_multiple_series_data, args=R)
#     t.start()
#     t.join()


def main():
    R = 15
    draw_single_series_data(R)
    R = 5
    draw_multiple_series_data(R)


if __name__ == "__main__":
    main()
