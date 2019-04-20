import json
import os
import random
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DiphdaService.settings import MEDIA_URL_PREFIX, BASE_DIR


@csrf_exempt
def upload(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    print(request.POST)
    if request.method == 'POST':
        files = request.FILES.getlist('files', None)  # input 标签中的name值
        print(files)
        if not files:
            res={'code':-1,'msg':"无上传文件", 'data':[]}
        else:
            date=time.strftime('%Y%m%d',time.localtime())
            url_mid = '/media/files/'+date+'/'
            dirs = BASE_DIR + url_mid
            folder = os.path.exists(dirs)
            if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(dirs)  # makedirs 创建文件时如果路径不存在会创建这个路径
            try:
                for file in files:
                    suffix = os.path.splitext(file.name)[1]
                    fname = "file_%s_%06d%s"%(str(int(round(time.time() * 1000))), random.randint(0,100000), suffix)
                    path = dirs + fname
                    f = open(path,'wb')
                    for line in file.chunks():
                        f.write(line)
                    f.close()
                    res['data'].append(MEDIA_URL_PREFIX+url_mid+fname)
            except Exception as e:
                res['code']=-2
                res['msg']=e
    return HttpResponse(json.dumps(res))