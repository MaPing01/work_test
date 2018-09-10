import re
import pandas as pd
word = pd.read_table('/root/workspace/demos/mptest/mptest/test.txt', encoding = 'utf-8', names = ['query'])
pattern = re.compile(u'没有|不了解')
result = filter(pattern.search, word['query'])
print(result)
