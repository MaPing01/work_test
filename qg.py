from __future__ import print_function, unicode_literals
import json
import requests


CLASSIFY_URL = 'http://api.bosonnlp.com/classify/analysis'


s = [
    '俄否决安理会谴责叙军战机空袭阿勒颇平民',
    '邓紫棋谈男友林宥嘉：我觉得我比他唱得好',
    'Facebook收购印度初创公司',
]

data = json.dumps(s)
headers = {'X-Token': 'YOUR_API_TOKEN'}
resp = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))


# shoud print [5, 4, 8]
print(resp.text)