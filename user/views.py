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
from user.models import User, Tag


@csrf_exempt
def create(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'openid','username','avatar'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        user=User.objects.create(**request.POST.dict())

        #保存头像
        r = requests.get(user.avatar)
        date = time.strftime('%Y%m%d', time.localtime())
        dirs = settings.MEDIA_ROOT + '/avatar/' + date + '/'
        url_mid = '/media/avatar/' + date + '/'
        fname = 'avatar_' + str(user.id) + '_'+ str(int(round(time.time() * 1000))) + '.jpg'
        folder = os.path.exists(dirs)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(dirs)
        with open(dirs+fname, "wb") as code:
            code.write(r.content)

        #头像url入库
        user.avatar=MEDIA_URL_PREFIX + url_mid + fname
        user.save()

    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(res))


@csrf_exempt
def login(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'openid'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        qset=User.objects.filter(openid=request.POST['openid'])
        if qset.count()==1:
            res['data']=json.loads(serializers.serialize("json", qset))[0]['fields']
            res['data']['id']=json.loads(serializers.serialize("json", qset))[0]['pk']
            res['data']['tags']=json.loads(json.loads(serializers.serialize("json", qset))[0]['fields']['tags'])
        else:
            res={'code':-2, 'msg':'登录失败-2','data':[]}

    except:
        res = {'code': -3, 'msg': '登录失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        params = request.POST
        user_id = params['user_id']
        params.pop('user_id')

        if 'avatar' in params.keys():
            # 保存头像
            r = requests.get(params['avatar'])
            date = time.strftime('%Y%m%d', time.localtime())
            dirs = settings.MEDIA_ROOT + '/avatar/' + date + '/'
            url_mid = '/media/avatar/' + date + '/'
            fname = 'avatar_' + str(user_id) + '_' + str(int(round(time.time() * 1000))) + '.jpg'
            folder = os.path.exists(dirs)
            if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(dirs)
            with open(dirs + fname, "wb") as code:
                code.write(r.content)

            # 头像url入库
            params['avatar']=MEDIA_URL_PREFIX + url_mid + fname

        User.objects.update(**params)
    except:
        res = {'code': -3, 'msg': '更新失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def show(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        qset = User.objects.filter(id=request.POST['user_id'])
        if qset.count() == 1:
            res['data'] = json.loads(serializers.serialize("json", qset))[0]['fields']
            res['data']['id'] = json.loads(serializers.serialize("json", qset))[0]['pk']
            res['data']['tags'] = json.loads(json.loads(serializers.serialize("json", qset))[0]['fields']['tags'])
        else:
            res = {'code': -2, 'msg': '用户不存在-2', 'data': []}
    except:
        res = {'code': -3, 'msg': '用户查找失败-3', 'data': []}
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
        res = {'code': -3, 'msg': '用户标签查找失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))