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
from needs.models import Need


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
        params=request.POST
        qset=Need.objects.filter(**params).order_by('-ctime')
        for r in json.loads(serializers.serialize('json',qset)):
            row=r['fields']
            row['need_id']=r['pk']
            res['data'].append(row)
    except:
        res = {'code': -3, 'msg': '需求查询失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))