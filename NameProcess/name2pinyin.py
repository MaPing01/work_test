from pypinyin import pinyin, lazy_pinyin, Style
import json
import sys
from re import findall,sub
def divid_name(name):
    len1 = len(name)
    if len1 == 2:
        firstname = name[0:1]
        secondname = name[1:2]
    elif len1 == 4:
        firstname = name[0:2]
        secondname = name[2:4]
        if not check1name(firstname):
            firstname = name[0:1]
            secondname = name[1:4]
    elif len1 == 3:
        firstname = name[0:2]
        secondname = name[2:3]
        if not check1name(firstname):
            firstname = name[0:1]
            secondname = name[1:3]
    else:
        firstname = ""
        secondname = name
    return firstname, secondname


def  check1name(firstname):
    with open(sys.path[0]+'/fuxing.txt', 'r') as rf:
        a = []
        a = rf.read()
    if firstname in a:
        return True
    return False

def part_to_pinyin(firstname, secondname):
    with open(sys.path[0]+'/duoyinzi.txt', 'r',encoding='utf-8') as rf:
        # dic = {'':''}
        # dic = eval(rf.read())
        dic = json.load(rf)
    fnamepy_list = []
    snamepy_list = []
    if firstname in dic.keys():
        fnamepy = dic[firstname]
        fnamepy_list.append(fnamepy)
    else:
        fnames = pinyin(firstname,style = Style.TONE3)
        for fname in fnames:
            fnamepy = fname[0]
            if findall("[1-4]", fnamepy) == []:
                fnamepy+= "1"
            fnamepy = sub("([0-4])(.*)", "\\2\\1", fnamepy)
            fnamepy = sub("ɡ", "g", fnamepy)
            fnamepy_list.append(fnamepy)
    snames = pinyin(secondname, style=Style.TONE3)
    for sname in snames:
        snamepy = sname[0]
        if findall("[1-4]", snamepy) == []:
            snamepy += "1"
        snamepy = sub("([0-4])(.*)", "\\2\\1", snamepy)
        snamepy = sub("ɡ", "g", snamepy)
        snamepy_list.append(snamepy)
    namepy_list =fnamepy_list + snamepy_list
    return namepy_list

def  to_pinyin(name):
    firstname, secondname = divid_name(name)
    namepy_list = part_to_pinyin(firstname, secondname)
    return  namepy_list


print(to_pinyin('单于'))
print(to_pinyin('张三'))
print(to_pinyin('李大仁'))
print(to_pinyin('诸葛亮'))
print(to_pinyin('易扬千禧'))