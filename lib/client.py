import traceback

import requests

from DiphdaService.settings import CONFIG


def getOpenid(code):
    data={
        'appid':'wx6d11ad308fa3283b',
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