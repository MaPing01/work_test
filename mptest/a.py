import pandas as pd
import re
word = pd.read_table('/root/workspace/demos/mptest/mptest/test.txt', encoding = 'utf-8', names = ['query'])

def signquery(word):
    tobacco = [u'没有']
    word['have_tobacco'] = word['query'].apply(lambda name:name in tobacco)
    # print(word['query']
    # patt = re.search(r'')
    # word['have_tobacco'] = word['query'].apply(lambda name:re.search(r'mei',tobacco))
    return word

def filter_query(word):
    tobacco = [u'没有',u'']
    return word[word['query'].applymap(lambda name:name in tobacco)]['query'].to_dict().values()

# result = filter_query(word)
result = signquery(word)
print (result)