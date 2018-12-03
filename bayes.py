import numpy as np
import math


def load_set():
    # 词表到向量的转换函数
    posting_list = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                    ['my', 'damn', 'is', 'so', 'cute', 'I', 'love', 'him'],
                    ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                    ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]
    return posting_list, class_vec


def create_set( data_set ):
    voc_set = set()
    # set函数只能处理1*n的list
    for document in data_set:
        voc_set = voc_set | set(document)
        # 求并集
    return list(voc_set)


def set2vec( voc_set, input_set ):
    return_vec = [0] * len(voc_set)
    for word in input_set:
        if word in voc_set:
            return_vec[voc_set.index(word)] = 1
            # 关于list的index方法，返回查找对象在list中的索引位置
    return return_vec


def train(train_matrix, train_category):
    # 朴素贝叶斯分类器训练函数
    num_train = len(train_matrix)
    num_words = len(train_matrix[0])
    p_abusive = sum(train_category)/float(num_train)
    p0num = np.ones(num_words)
    p1num = np.ones(num_words)
    p0_denom = 2.0
    p1_denom = 2.0
    p0vec = []
    p1vec = []
    for i in range(num_train):
        if train_category[i] == 1:
                print('train_matrix[%s]:%s'%(i,train_matrix[i]))
                print("before p1num:%s"%(p1num))
                print("before p1_denom:%s"%(p1_denom))
                print("sum(train_matrix[%s]:%s"%(i,sum(train_matrix[i])))
                p1num += train_matrix[i]
                p1_denom += sum(train_matrix[i])
                print("after p1num += train_matrix[%s]:%s"%(i,p1num))
                print("after p1_denom += sum(train_matrix[%s]):%s"%(i,p1_denom))
        else:
                print('train_matrix[%s]:%s'%(i,train_matrix[i]))
                print("before p0num:%s"%(p0num))
                print("before p0_denom:%s"%(p0_denom))
                print("sum(train_matrix[%s]:%s" % (i, sum(train_matrix[i])))
                p0num += train_matrix[i]
                p0_denom += sum(train_matrix[i])
                print("after p0num += train_matrix[%s]:%s"%(i,p0num))
                print("after p0_denom += sum(train_matrix[%s]):%s"%(i,p0_denom))
    for i in range(num_words):
        # p0vec.append(math.log(p0num[i] / p0_denom))
        # p1vec.append(math.log(p1num[i] / p1_denom))
        p0vec.append(p0num[i] / p0_denom)
        p1vec.append(p1num[i] / p1_denom)
    # 取对数是为了防止多个很小的数相乘使得程序下溢出或者得到不正确答案。
    return p_abusive, p0vec, p1vec

def classify(vec2classify, p0vec, p1vec, pclass1):
    # p0 = sum(vec2classify * p0vec) + math.log(pclass1)
    # p1 = sum(vec2classify * p1vec) + math.log(1.0-pclass1)
    p0 = np.multiarray(vec2classify * p0vec)*pclass1
    p1 = np.multiarray(vec2classify * p1vec )*(1.0 - pclass1)
    if p1 > p0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    word_list, class_list = load_set()
    word_set = create_set(word_list)
    train_mat = []
    for j in range(len(word_list)):
        train_mat.append(set2vec(word_set, word_list[j]))
    p_a, p0v, p1v = train(train_mat, class_list)
    test_entry = ['love', 'my', 'dalmation']
    this_doc = np.array(set2vec(word_set, test_entry))
    print("%s is classified as:%d"%(test_entry, classify(this_doc, p0v, p1v, p_a)))
    test_entry = ['stupid', 'garbage']
    this_doc = np.array(set2vec(word_set, test_entry))
    print("%s is classified as:%d"%(test_entry, classify(this_doc, p0v, p1v, p_a)))