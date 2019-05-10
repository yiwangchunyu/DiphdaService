import json
import os
import random
import time
import traceback

import requests
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from DiphdaService import settings
from DiphdaService.settings import MEDIA_URL_PREFIX
from needs.models import Need, Tag, Category, NEED_STATUS_MAP, Order
from user.models import User


@csrf_exempt
def create(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'user_id','level','category','tags','content','quote'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        need=Need.objects.create(**request.POST.dict())
        res['data']={'need_id':need.id}
    except:
        res = {'code': -3, 'msg': '需求创建失败', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def delete(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'need_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        Need.objects.filter(id=request.POST['need_id']).update(status=0)
    except:
        res = {'code': -3, 'msg': '需求删除失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def update(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'need_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        params=request.POST
        need_id=params['need_id']
        params.pop('need_id')
        Need.objects.filter(id=need_id).update(**params)
    except:
        res = {'code': -3, 'msg': '需求更新失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def show(request):
    res={'code':0, 'msg':'success', 'data':[]}
    try:
        params=request.POST.dict()
        params['status']=1
        qset=Need.objects.filter(**params).order_by('-ctime')
        for r in json.loads(serializers.serialize('json',qset)):
            row=r['fields']
            user_id=row['user_id']
            row.pop('user_id')
            qqset=User.objects.filter(id=user_id)
            row['user_info'] = json.loads(serializers.serialize('json',qqset))[0]['fields']
            row['need_id']=r['pk']
            row['tags']=json.loads(row['tags'])
            row['need_stat'] = row['need_status']
            row['need_status']=NEED_STATUS_MAP[row['need_status']]
            res['data'].append(row)
    except:
        res = {'code': -3, 'msg': '需求查询失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def getTags(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    try:
        qset = Tag.objects.all()
        for q in qset:
            res['data'].append(q.name)
    except:
        res = {'code': -3, 'msg': '需求标签查找失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def getCategories(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    try:
        qset = Category.objects.all()
        for q in qset:
            res['data'].append(q.name)
    except:
        res = {'code': -3, 'msg': '需求类别查找失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def createOrder(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if  not {'user_id','need_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        need=Need.objects.get(id=request.POST['need_id'])
        #订单可以被抢单
        if need.need_status==1:
            if need.user_id==request.POST['user_id']:
                res = {'code': -4, 'msg': '这是您自己的订单哦', 'data': []}
            else:
                Order.objects.create(need_id=request.POST['need_id'], user_id=request.POST['user_id'])
                need.need_status=2
                need.save()
                res = {'code': 0, 'msg': 'success', 'data': []}
        else:
            res = {'code': -3, 'msg': '此订单已被其他人抢单啦', 'data': []}
    except:
        res = {'code': -2, 'msg': '需求查询失败-2', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def listOrder(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if  not {'user_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        qset=Order.objects.filter(user_id=request.POST['user_id'],status=1)
        need_ids=[q.need_id for q in qset]
        qset=Need.objects.filter(id__in=need_ids)
        for r in json.loads(serializers.serialize('json',qset)):
            row=r['fields']
            user_id=row['user_id']
            row.pop('user_id')
            qqset=User.objects.filter(id=user_id)
            row['user_info'] = json.loads(serializers.serialize('json',qqset))[0]['fields']
            row['need_id']=r['pk']
            row['tags']=json.loads(row['tags'])
            row['need_stat'] = row['need_status']
            row['need_status']=NEED_STATUS_MAP[row['need_status']]
            res['data'].append(row)

    except:
        res = {'code': -2, 'msg': '需求查询失败-2', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def cancelOrder(request):
    # print(request.POST.keys())
    res = {'code': 0, 'msg': 'success', 'data': []}
    if  not {'need_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        order=Order.objects.get(status=1,need_id=request.POST['need_id'])
        order.status=0
        order.save()
        need=Need.objects.get(status=1,id=request.POST['need_id'])
        need.need_status=1
        need.save()
    except:
        res = {'code': -2, 'msg': '删除失败-2', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def orderUpdate(request):
    print(request.POST.keys())
    res = {'code': 0, 'msg': 'success', 'data': []}
    if  not {'need_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        params=request.POST.dict()
        print(type(params),params)
        need_id=params['need_id']
        params.pop('need_id')
        Order.objects.filter(need_id=need_id,status=1).update(**params)
    except:
        res = {'code': -3, 'msg': '更新失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def orderDetail(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    if  not {'need_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        order = Order.objects.get(status=1, need_id=request.POST['need_id'])
        res['data']=json.loads(serializers.serialize('json',Order.objects.filter(status=1, need_id=request.POST['need_id'])))[0]['fields']
    except:
        res = {'code': -2, 'msg': '查询失败-2', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

