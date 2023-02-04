from django.shortcuts import render
# 待导入pncop算法的包
# ......
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
# import requests
import json
from pncop.pncop_algorithm.pncopMiner import findPNCOP

@require_http_methods(["POST"])
def compute_frequent_set(request):
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
        resStr = "positive patterns: "
        for pattern_size in all_positive_set:
            if not pattern_size == 1:
                if all_positive_set[pattern_size]:
                    resStr = resStr + "pattern size: {}".format(pattern_size)
                for st in all_positive_set[pattern_size]:
                    resStr = resStr + "{}".format(st)
        # resStr = resStr + "-------------------------------------"
        resStr2 = "negative set: "
        for pattern_size in all_negative_set:
            if not pattern_size == 1:
                if all_negative_set[pattern_size]:
                    resStr2 = resStr2 + "pattern size: {}".format(pattern_size)
                for st in all_negative_set[pattern_size]:
                    resStr2 = resStr2 + "{}".format(st)
        response['positiveMsg'] = resStr
        response['negativeMsg'] = resStr2
        
    except  Exception as e:
        response['positiveMsg'] = str(e)
        response['negativeMsg'] = str(e)
        

    return JsonResponse(response)




