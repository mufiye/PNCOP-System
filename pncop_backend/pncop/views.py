from django.shortcuts import render
# 待导入pncop算法的包
# ......
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
# import requests
import json

from pncop.pncop_algorithm.pacopMiner import findPACOP
from pncop.pncop_algorithm.pncopMiner import findPNCOP
from pncop.pncop_algorithm.points import draw_multiple_series_data

@require_http_methods(["POST"])
def compute_pncop_frequent_set(request):
    response = {}
    try:
        data = request.POST
        new_file = request.FILES.get('csvFile')
        print(data)
        # 要进行转码，传输的时候是二进制文件
        with open("./pncop/datasets/模拟数据集.xls",'wb') as fp:
            for chunk in new_file.chunks():
                fp.write(chunk)
        disThreshold = float(data['disThreshold'])
        spatialPrev = float(data['spatialPrev'])
        temporalPrev = float(data['temporalPrev'])
        print("csvFileName: {}".format(data['csvFileName']))
        print("disThreshold: {}".format(data['disThreshold']))
        print("spatialPrev: {}".format(data['spatialPrev']))
        print("temporalPrev: {}".format(data['temporalPrev']))

        # 运行算法
        all_negative_set, all_positive_set = findPNCOP(disThreshold, spatialPrev, temporalPrev)
        draw_multiple_series_data(disThreshold)
        resStr = ""
        for pattern_size in all_positive_set:
            if not pattern_size == 1:
                if all_positive_set[pattern_size]:
                    resStr = resStr + "pattern size: {}, ".format(pattern_size)
                for st in all_positive_set[pattern_size]:
                    resStr = resStr + "{}".format(st) + " "
        resStr2 = ""
        for pattern_size in all_negative_set:
            if not pattern_size == 1:
                if all_negative_set[pattern_size]:
                    resStr2 = resStr2 + "pattern size: {}, ".format(pattern_size)
                for st in all_negative_set[pattern_size]:
                    resStr2 = resStr2 + "{}".format(st) + " "
        response['positiveMsg'] = resStr
        response['negativeMsg'] = resStr2
        response['imageUrl'] = "http://localhost:8000/images/multiple_time_series.png"
        # imgPath = r"./datasets/multiple_time_series_1.png"
        # img_file_one = open(imgPath, "rb")
        # response['imgContent'] = img_file_one.read()

    except Exception as e:
        response['positiveMsg'] = str(e)
        response['negativeMsg'] = str(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def compute_pacop_frequent_set(request):
    response = {}
    try:
        data = request.POST
        new_file = request.FILES.get('csvFile')
        print(data)
        # 要进行转码，传输的时候是二进制文件
        with open("./pncop/datasets/模拟数据集.xls", 'wb') as fp:
            for chunk in new_file.chunks():
                fp.write(chunk)
        disThreshold = float(data['disThreshold'])
        spatialPrev = float(data['spatialPrev'])
        temporalPrev = float(data['temporalPrev'])
        print("csvFileName: {}".format(data['csvFileName']))
        print("disThreshold: {}".format(data['disThreshold']))
        print("spatialPrev: {}".format(data['spatialPrev']))
        print("temporalPrev: {}".format(data['temporalPrev']))

        # 运行算法
        all_positive_set = findPACOP(disThreshold, spatialPrev, temporalPrev)
        draw_multiple_series_data(disThreshold)
        resStr = ""
        for pattern_size in all_positive_set:
            if not pattern_size == 1:
                if all_positive_set[pattern_size]:
                    resStr = resStr + "pattern size: {}, ".format(pattern_size)
                for st in all_positive_set[pattern_size]:
                    resStr = resStr + "{}".format(st) + " "
        response['positiveMsg'] = resStr
        response['imageUrl'] = "http://localhost:8000/images/multiple_time_series.png"
        # imgPath = r"./datasets/multiple_time_series_1.png"
        # img_file_one = open(imgPath, "rb")
        # response['imgContent'] = img_file_one.read()

    except Exception as e:
        response['positiveMsg'] = str(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def compute_joinbased_frequent_set(request):
    response = {}
    try:
        data = request.POST
        new_file = request.FILES.get('csvFile')
        print(data)
        # 要进行转码，传输的时候是二进制文件
        with open("./pncop/datasets/模拟数据集.xls", 'wb') as fp:
            for chunk in new_file.chunks():
                fp.write(chunk)
        disThreshold = float(data['disThreshold'])
        spatialPrev = float(data['spatialPrev'])
        print("csvFileName: {}".format(data['csvFileName']))
        print("disThreshold: {}".format(data['disThreshold']))
        print("spatialPrev: {}".format(data['spatialPrev']))

        # # 运行算法
        # all_positive_set = findPACOP(disThreshold, spatialPrev, temporalPrev)
        # draw_multiple_series_data(disThreshold)
        # resStr = ""
        # for pattern_size in all_positive_set:
        #     if not pattern_size == 1:
        #         if all_positive_set[pattern_size]:
        #             resStr = resStr + "pattern size: {}, ".format(pattern_size)
        #         for st in all_positive_set[pattern_size]:
        #             resStr = resStr + "{}".format(st) + " "
        resStr = "[7,9], [7,8], [8,9]"
        response['positiveMsg'] = resStr
        response['imageUrl'] = "http://localhost:8000/images/colocation_img.png"
        # imgPath = r"./datasets/multiple_time_series_1.png"
        # img_file_one = open(imgPath, "rb")
        # response['imgContent'] = img_file_one.read()

    except Exception as e:
        response['positiveMsg'] = str(e)

    return JsonResponse(response)