import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from userext.models import Userext


# @csrf_exempt
# def update(request):
#     res = {'code': 0, 'msg': 'success', 'data': []}
#     if not {'user_id'}.issubset(set(request.POST.keys())):
#         return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
#     try:
#         a=1
#     except:
#         res = {'code': -3, 'msg': '更新失败-3', 'data': []}
#         traceback.print_exc()
#     return HttpResponse(json.dumps(res))

@csrf_exempt
def addExpc(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id','expc'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        if Userext.objects.filter(user_id=request.POST['user_id']).count()==0:
            Userext.objects.create(user_id=request.POST['user_id'],expc=request.POST['expc'])
        else:
            userext=Userext.objects.get(user_id=request.POST['user_id'])
            userext.expc=userext.expc+int(request.POST['expc'])
            userext.save()
    except:
        res = {'code': -3, 'msg': '更新失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def get(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if not {'user_id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': []}))
    try:
        if Userext.objects.filter(user_id=request.POST['user_id']).count()==0:
            Userext.objects.create(user_id=request.POST['user_id'])
        qset=Userext.objects.filter(user_id=request.POST['user_id'])
        res['data'] = json.loads(serializers.serialize("json", qset))[0]['fields']
    except:
        res = {'code': -3, 'msg': '更新失败-3', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))