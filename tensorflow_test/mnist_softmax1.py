from tensorflow_test import input_data
import tensorflow as tf


#读取数据的路径
mnist = input_data.read_data_sets("/root/workspace/demos/mptest/tensorflow_test/MNIST_data",one_hot=True)

#x不是一个特定的值，而是一个占位符placeholder,我们在tensorflow运行计算时输入这个值。
#希望输入任意数量的MNIST图像，每一张图展平成784的向量。
#None表示此向量的第一维度可以是任何长度。
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32,[None,784],name='x_input')
    #y_为实际值，从data中获取，为计算交叉熵添加的placeholder
    y_ = tf.placeholder("float",[None,10],name='y_input')
with tf.name_scope('layers'):
    with tf.name_scope('W'):
        #代表权重值，初始值为0
        W = tf.Variable(tf.zeros([784,10]))
    with tf.name_scope('bias'):
        #b为偏置量，初始值为0
        b = tf.Variable(tf.zeros([10]))
    with tf.name_scope('softmax'):
        #建立模型，y是匹配的概率
        #tf.matmul(x,w)表示x乘以w为优化器
        #y是预测值，y_是实际值
        #softmax为activation function激活函数
        y = tf.nn.softmax(tf.matmul(x,W)+ b,name='Wx_plus_b')
        tf.summary.histogram('y', y)
with tf.name_scope('cross_entropy'):
    #交叉熵
    cross_entropy = -tf.reduce_sum(y_*tf.log(y))
    tf.summary.scalar("cross_entropy",cross_entropy)
with tf.name_scope('train'):
    #用梯度下降算法以0.01的学习速率最小化交叉熵
    #GradientDescentOptimizer
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
#初始化我们创建的变量
# init = tf.initialize_all_variables()
init = tf.global_variables_initializer()
#在session里面启动模型
sess = tf.Session()
writer = tf.summary.FileWriter('/root/workspace/demos/mptest/tensorflow_test/log/',sess.graph)
sess.run(init)


#训练模型
#每次循环都会抓取训练数据中的100个批处理数据结点，然后用这些数据点作为参数替换之前的占位符来运行train_step
# for _ in range(100):
#     batch_xs,batch_ys = mnist.train.next_batch(100)
#     sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})
#     if i % 50 == 0:
#         result = sess.run(merge,feed_dict={x:mnist.test.images,y_:mnist.test.labels})
#         writer.add_summary(result,i)
merge = tf.summary.merge_all()
for i in range(100):
    batch_xs,batch_ys = mnist.train.next_batch(100)
    sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})
    if i % 5 == 0:
        result = sess.run(merge,feed_dict={x:batch_xs,y_:batch_ys})
        writer.add_summary(result,i)
###########模型评估##################
#tf.argmax能给出某个tensor对象在某一维上的数据最大值所在的索引值。
#由于标签向量是由0.1组成，因此最大值1所在的索引位置就是类别标签
with tf.name_scope("accuracy"):
    with tf.name_scope("correct_prediction"):
        correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))

#correct_prediction返回的是一组布尔值，为了确定预测比例，我们可以把布尔值转换为浮点数，然后取平均值
#tf.cast为类型转换函数
with tf.name_scope("accuracy"):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
    tf.summary.scalar("accuracy",accuracy)
#计算所学习到的模型在测试数据集上面的正确率
# merge = tf.summary.merge_all()
print(sess.run(accuracy,feed_dict={x:mnist.test.images,y_:mnist.test.labels}))



