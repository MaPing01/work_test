import tensorflow as tf

state = tf.Variable(0,name='counter')#define variable state ,variable name is counter ,defaule value is 0
print(state.name)
one = tf.constant(1)

new_value = tf.add(state,one)
update = tf.assign(state,new_value)

init = tf.initialize_all_variables()#定义了变量必须初始化(创建初始化op)，session 也必须运行初始化

with tf.Session() as sess:
    sess.run(init) #定义了变量必须首先运行初始化op，激活变量
    for _ in range(5):
        sess.run(update)
        print(sess.run(state))