#!/usr/bin/env python3
"""
Train a neural network to predict future salaries from past salaries, 
employer, job title and dempgraphic information.
"""
import numpy as np
import tensorflow as tf
import pdb
import input_vector
import sys

from nn_settings import *

learning_rate = 1e-4
epochs = 50000000
batch_size = 1000

x = tf.placeholder(tf.float32, [batch_size, n_input])
y = tf.placeholder(tf.float32, [batch_size, n_target])

n_inner_layers = 0
n_layers = n_inner_layers + 1
n_hidden = [100] * n_layers
assert(len(n_hidden) == n_layers)

w_i = tf.Variable(tf.truncated_normal([n_input, n_hidden[0]]))
b_i = tf.Variable(tf.zeros([n_hidden[0]]))
w_o = tf.Variable(tf.truncated_normal([n_hidden[-1], n_target]))
b_o = tf.Variable(tf.zeros([n_target]))

internal_weights = [tf.Variable(tf.truncated_normal([n_hidden[i], n_hidden[i + 1]])) for i in range(n_inner_layers)]
internal_biases =  [tf.Variable(tf.zeros([n_hidden[i + 1]])) for i in range(n_inner_layers)]

weights = [w_i] + internal_weights + [w_o]
biases = [b_i] + internal_biases + [b_o]


in_cols = range(n_input)
t_cols = range(n_input, n_input + n_target)
col_labels = ['Sct' + str(i) for i in range(n_sct)] + \
             ['Emp' + str(i) for i in range(n_emp)] + \
             ['Jbt' + str(i) for i in range(n_jbt)] + \
             ['StartYear' + str(y) for y in range(n_years - ts_thresh)] + \
             ['Salary' + str(y) for y in range(n_years - n_target)] + \
             other_cols

def nn(x, y):
    o = x
    for w, b in zip(weights, biases):
        o = tf.add(b, tf.matmul(o, w))

    cost = tf.reduce_mean(tf.square(y - o))
    return o, cost

def get_batch(samples, i):
    if i == 0:
        np.random.shuffle(samples)

    return {x: samples[i*batch_size:(i+1)*batch_size, in_cols],
            y: samples[i*batch_size:(i+1)*batch_size, t_cols]}



def main():
    try:
        train = np.load(data_folder + 'train_' + settings_string + '.npy').astype(np.float32)
        valid = np.load(data_folder + 'valid_' + settings_string + '.npy').astype(np.float32)
        if len(sys.argv) >= 2:
            print('Cached datasets found, input dataframe ' + sys.argv[1] + ' not used.')  
    except FileNotFoundError:
        if len(sys.argv) < 2:
            print('Cached datasets not found, please provide input dataframe')  
        else:
            input_vector.main()
            train = np.load(data_folder + 'train_' + settings_string + '.npy').astype(np.float32)
            valid = np.load(data_folder + 'valid_' + settings_string + '.npy').astype(np.float32)

    assert(n_input == train.shape[1] - n_target)


    saver = tf.train.Saver(weights + biases)
    n_batch = int(train.shape[0]/batch_size)

    pred, cost = nn(x, y)

    valid_x = valid[:, range(n_input)]
    valid_y = valid[:, range(n_input, n_input + n_target)]
    valid_pred, valid_cost = nn(valid_x, valid_y)

    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
    init = tf.global_variables_initializer()
    
    minloss = 0.25
    display_step = 1000
    validate_step = 10000

    with tf.Session() as sess:
        sess.run(init)
        
        for i in range(epochs):
            batch = get_batch(train, i % n_batch)
            sess.run(optimizer, feed_dict=batch)
            if i % display_step == 0:
                print(sess.run(cost, feed_dict=batch))
                if i % validate_step == 0:
                    loss = sess.run(valid_cost)
                    print('Validation loss: ', loss)
                    if loss < minloss:
                        minloss = loss
                        saver.save(sess, model_folder + 'model-' + str(loss), global_step=i)

    

if __name__ == "__main__":
    main()
