import traceback

import requests

from DiphdaService.settings import CONFIG


def getOpenid(code):
    data={
        'appid':'wx8b0638d0d785d5b9',
        'secret':CONFIG['secret'],
        'grant_type':'authorization_code',
        'js_code':code
    }
    url='https://api.weixin.qq.com/sns/jscode2session'
    try:
        print(data)
        r=requests.post(url,data=data)
    except:
        traceback.print_exc()
        return {'code':-1,'msg':'timeout | getopenid failed!','data':[]}
    return {'code':0, 'msg':'success','data':r.json()}