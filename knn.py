import numpy as np
import pandas as pd
import operator

#读取数据：将文件数据转换为数组
def file2mat(filename):
    data = pd.read_table(open(filename),sep='   ',header=None)
    returnMat = data[[0,1,2]].values
    classMat = data[3].values
    return returnMat,classMat

# 数据归一化
#new = (old - min)/range
def dataIni(dataSet):
    minval = dataSet.min(0)
    maxval = dataSet.max(0)
    range = maxval - minval
    returnDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    returnDataSet = dataSet - np.tile(minval,(m,1))
    returnDataSet = returnDataSet/np.tile(range,(m,1))
    return returnDataSet,range,minval


#计算欧拉距离
def classify(testSet,dataSet,lable,k):
    datasize = dataSet.shape[0]
    diffMat = np.tile(testSet,(datasize,1)) - dataSet
    sqdiffMat = diffMat ** 2
    sqdistance = sqdiffMat.sum(axis=1)
    distance = sqdistance ** 0.5
    sortDist = distance.argsort()  #由小到大排列返回索引
    countDict = {}
    for i in range(k):
        testLable = lable[sortDist[i]]
        countDict[testLable] = countDict.get(testLable,0) + 1
    sortedcountDict = sorted(countDict.items(),key=operator.itemgetter(1),reverse=True)
    print(sortedcountDict[0])
    print(sortedcountDict[0][0])
    return sortedcountDict[0][0]


def test():
    style = ['不喜欢', '一般', '喜欢']
    ffmile = float(input('飞行里程'))
    game = float(input('游戏'))
    ice = float(input('冰淇淋'))
    X, y = file2mat("1.txt")
    new_X, ranges, minval = dataIni(X)
    inArr = np.array([ffmile, game, ice])
    result = classify((inArr - minval) / ranges, new_X, y, 3)
    print('这个人', style[result - 1])


test()