import tensorflow as tf

import os
import struct
import numpy as np

def load_mnist(path,kind = 'train'):
    """load mnist data from 'path'"""
    labels_path = os.path.join(path,"%s-labels.idx1-ubyte"%kind)
    images_path = os.path.join(path,"%s-images.idx3-ubyte"%kind)

    with open(labels_path,'rb') as lbpath:
        magic,n = struct.unpack(">II",lbpath.read(8))
        labels = np.fromfile(lbpath,dtype=np.uint8)

    with open(images_path,'rb') as imgpath:
        magic,num,row,cols = struct.unpack(">IIII",imgpath.read(16))
        images = np.fromfile(imgpath,dtype=np.uint8).reshape(len(labels),784)
        images.next_batch(100)

    return images,labels


data_path = "/root/workspace/demos/mptest/tensorflow_test/data"
load_mnist(data_path)