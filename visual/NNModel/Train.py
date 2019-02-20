# Ideas:
# * Combine left and right into a single input
# * Remove X, Y and Up, I never press those
# 

import datetime
import time

import tensorflow as tf

import Config as config

ValidationPeriod = config.get_validation_period()
best_cost = 0
model = None
data = None


def do_validation(session, state, step, saver):
    global best_cost, model, data
    # global global_step

    feed_dict = {
        data.input: data.data[-1],
        data.output: data.labels[-1],
        data.cost_weight: data.cost[-1],
    }
    for i, (c, h) in enumerate(model.initial_state):
        feed_dict[c] = state[i].c
        feed_dict[h] = state[i].h
    # (cost, step) = session.run([model.cost, global_step], feed_dict)
    cost = session.run(model.cost, feed_dict)
    print("Batches: %05d Cost: %.4f (%s)" % (step, cost, str(datetime.datetime.now())))
    if best_cost == 0 or cost < best_cost:
        best_cost = cost
        print("Saving model.")
        saver.save(session, config.get_checkpoint_dir() + '\mario', global_step=step, write_meta_graph=False)


def train():
    global data, best_cost, model
    data = config.get_data(training=True)
    # print(config.get_checkpoint_dir())
    print("Batches: %d Batch Size: %d Sequence Length: %d" % (data.num_batches, data.batch_size, data.num_steps))
    model = config.get_model(data, training=True)
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    step = 0
    with tf.Session() as session:
        last_checkpoint = tf.train.latest_checkpoint(config.get_checkpoint_dir() + '\\')
        if last_checkpoint is not None:
            print("Restoring session from path:" + last_checkpoint)
            saver.restore(session, last_checkpoint)
            step = int(last_checkpoint.split("-")[-1]) + 1
        else:
            session.run(init)
        state = session.run(model.initial_state)
        validation_state = state
        fetches = {
            "train": model.train_op,
            "final_state": model.final_state
        }
        start_time = time.time()
        last_validation = start_time - ValidationPeriod
        while True:
            try:
                state = session.run(model.initial_state)
                # data.random_reorder()
                for b in range(data.num_batches - 1):
                    if time.time() - last_validation > ValidationPeriod:
                        last_validation += ValidationPeriod
                        do_validation(session, validation_state, step, saver)
                    feed_dict = {
                        data.input: data.data[b],
                        data.output: data.labels[b],
                        data.cost_weight: data.cost[b],
                    }
                    for i, (c, h) in enumerate(model.initial_state):
                        feed_dict[c] = state[i].c
                        feed_dict[h] = state[i].h
                    vals = session.run(fetches, feed_dict)
                    state = vals["final_state"]
                    step = step + 1
                validation_state = state
            except KeyboardInterrupt:
                # step = session.run(global_step)
                print("Manually saving model.")
                saver.save(session, config.get_checkpoint_dir() + '\mario', global_step=step, write_meta_graph=False)


if __name__ == "__main__":
    train()
