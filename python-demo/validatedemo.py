#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''易盾本机验证python示例代码
接口文档: http://dun.163.com/api.html
python版本：python2.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python validatedemo.py
'''
__author__ = 'yidun-dev'
__version__ = '0.1-dev'

from  hashlib import md5
import json
import random
import time
import urllib
import urllib.request


class ValidateAPIDemo(object):
    """易盾短信发送接口示例代码"""
    API_URL = "https://ye.dun.163yun.com/v1/check"
    VERSION = "v1"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return md5(buff.encode("utf-8")).hexdigest()

    def send(self, params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        params["signature"] = self.gen_signature(params)

        try:

            params = urllib.parse.urlencode(params)
            params = params.encode('utf-8')
            request = urllib.request.Request(self.API_URL, params)
            content = urllib.request.urlopen(request, timeout=5).read()
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    params = {
        "phone": "your phone",
        "token": "yidun token", #32位
		"accessToken": "xxx"
    }
    ret = api.send(params)
    if ret is not None:
        if ret["code"] == 200:
            result = ret["data"]["result"]
            if result == 1:
               ## 执行登录
            elif result == 2:
               ## 校验不通过, 降级短信
            else:
               ## 无法确定, 降级短信
        else:
            print ("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
