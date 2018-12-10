#coding:utf-8

import json
import logging
import base64
import time
import requests
import hashlib
import xml.dom.minidom as mdom
from MainRobot.AiBase import AiBase
from urllib3 import request as urllib3req


class BaseAsr(AiBase):
    def __init__(self,*args,**kwargs):
        super(BaseAsr,self).__init__(*args,**kwargs)
        self.mader = ''

    def getTxt(self,content,statu=5):
        if self.rtype=='json':
            return self.json_parse(content,statu)
        elif self.rtype=='xml':
            return self.xml_parse(content,statu)
        return self.text_parse(content,statu)

    def sdk_request(self,con,uuid):
        con.execute('detect_speech', 'mifeng_asr {mader='+self.mader+',start-input-timers=false,no-input-timeout=1000}yes_no yes_no',
                    uuid)

    def web_request(self,r_file):
        pass

class AliAsr(BaseAsr):

    def __init__(self,*args,**kwargs):
        super(AliAsr,self).__init__(*args,**kwargs)
        self.mader='ali'

    def json_parse(self,content,statu=5):
        logging.info(content)
        if self.request_type == 'web':
            return self.web_json_parse(content)
        else:
            return self.sdk_json_parse(content, statu)

    def sdk_json_parse( self, content,statu ):
        if statu=='5':
            ret = json.loads(content)
            if 'result' in ret:
                return ret['result']['text']
        return None

    def web_json_parse(self,content):
        asr_result=json.loads(content)
        if asr_result['status']==20000000:
            return asr_result['result']
        else:
            logging.info("ali语音识别出错;ID:%s,状态码:%s,状态描述:%s",asr_result['task_id'],asr_result['status'],asr_result['message'])
        return None

    def web_request(self,r_file):
        with  open(r_file, 'rb') as f:
            file_content = f.read()
        # 设置HTTP请求头部
        x_header = {
            'X-NLS-Token': self.conf['token'],
            'Content-type': 'application/octet-stream',
            'Content-Length': len(file_content)}
        body = file_content
        # 设置RESTful请求参数
        req = '%s?appkey=%s&format=%s&sample_rate=%s&enable_punctuation_prediction=%s&enable_inverse_text_normalization=%s&enable_voice_detection=%s'
        query = req %(self.url,
                      self.conf['param']['appkey'],
                      self.conf['param']['format'],
                      self.conf['param']['sample_rate'],
                      self.conf['param']['enable_punctuation_prediction'],
                      self.conf['param']['enable_inverse_text_normalization'],
                      self.conf['param']['enable_voice_detection']
                      )
        response=self.webRequestByHeader("post",query,body,x_header,True)
        if response.status==200:
            return response.data
        else:
            logging.info(response.data)
        return None

class BaiduAsr(BaseAsr):

    def __init__(self,*args,**kwargs):

        super(BaiduAsr, self).__init__(*args,**kwargs)
        self.mader = 'baidu'

    def json_parse(self,content,statu=5):
        if self.request_type=='web':
            return self.web_json_parse(content)
        else:
            return self.sdk_json_parse(content,statu)

    def sdk_json_parse(content, statu):
        logging.info("百度sdk结果分析暂未实现")
        return None

    def web_json_parse(self,content):
        asr_result = json.loads(content)
        if asr_result['err_no'] == 0:
            return asr_result['result'][0]
        else:
            logging.info("keda语音识别出错;原因:%s", asr_result)
        return None


    def web_request(self,r_file):

        with  open(r_file, 'rb') as f:
            file_content = f.read()
        temp="audio/%s;rate=%s"
        header={}
        header["Content-Type"]=temp % (self.conf['param']['format'],self.conf['param']['rate'])
        param="cuid=%s&dev_pid=%s&token=%s" % (self.conf['param']['cuid'],self.conf['param']['dev_pid'],self.conf['param']['token'])
        url_temp="%s?%s" % (self.url,param)
        response=self.webRequestByHeader("post",url_temp,file_content,header,True)
        if response.status==200:
            return response.data
        else:
            logging.info(response.data)
        return None

class KedaAsr(BaseAsr):

    def __init__(self,*args,**kwargs):
        super(KedaAsr, self).__init__(*args,**kwargs)
        self.mader = 'keda'

    def json_parse(self,content,statu=5):
        logging.info(content)
        if self.request_type=='web':
            return self.web_json_parse(content)
        else:
            return self.sdk_json_parse(content,statu)

    def sdk_json_parse(self,content,statu):
        if statu=='5':
            txt=''
            ret = json.loads(content)
            if 'ws' in ret:
                for word in ret['ws']:
                    for cword in word['cw']:
                        txt += cword['w']
                        break
                return txt
        return None

    def web_json_parse(self,content):
        asr_result=json.loads(content)
        if asr_result['code']=="0":
            return asr_result['data']
        else:
            logging.info("keda语音识别出错;原因:%s",asr_result)
        return None


    def web_request(self,r_file):
        with  open(r_file, 'rb') as f:
            file_content = f.read()
        api_key = self.conf['pwd']
        x_appid = self.conf['uname']
        base64_audio = base64.b64encode(file_content)
        body = {'audio': base64_audio.decode()}
        x_param = base64.b64encode(json.dumps(self.conf['param']).replace(' ', '').encode('utf-8'))
        x_time = str(int(time.time()))
        p= api_key + x_time + x_param.decode('utf-8')
        x_checksum = hashlib.md5()
        x_checksum.update(p.encode('utf-8'))
        x_header = {'X-Appid': x_appid,
                    'X-CurTime': x_time,
                    'X-Param': x_param.decode('utf-8'),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                    'X-CheckSum': x_checksum.hexdigest()}
        response=self.webRequestByHeader("post",self.url,urllib3req.urlencode(body),x_header,True)
        logging.info(response)
        if response.status==200:
            return response.data
        else:
            logging.info(response.data)
        return None
