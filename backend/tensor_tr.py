import os
import time

import numpy as np
import tensorflow as tf
import unidecode
from keras_preprocessing.text import Tokenizer
import io
# tf.enable_eager_execution()

BATCH_SIZE = 1000
BUFFER_SIZE = 1000
EPOCHS = 15

file_path = "/home/ken/Documents/acik-hack/null-pointer-acik-hack/res/out.txt"

text = io.open(file_path, "r", encoding="ISO8859-9").read()
# text = io.open(file_path, "r").read()

tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])

encoded = tokenizer.texts_to_sequences([text])[0]

vocab_size = len(tokenizer.word_index) + 1

word2idx = tokenizer.word_index
idx2word = tokenizer.index_word

sequences = []

for i in range(1, len(encoded)):
    sequence = encoded[i - 1 : i + 1]
    sequences.append(sequence)

sequences = np.array(sequences)

X, Y = sequences[:, 0], sequences[:, 1]  
X = np.expand_dims(X, 1)
Y = np.expand_dims(Y, 1)

dataset = tf.data.Dataset.from_tensor_slices((X, Y)).shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

class Model(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, units, batch_size):
        super(Model, self).__init__()
        self.units = units
        self.batch_size = batch_size

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)

        self.gru = tf.keras.layers.GRU(
            self.units,
            return_sequences=True,
            return_state=True,
            recurrent_activation="sigmoid",
            recurrent_initializer="glorot_uniform",
        )
        self.fc = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, hidden):
        inputs = self.embedding(inputs)

        output, states = self.gru(inputs, initial_state=hidden)

        output = tf.reshape(output, (-1, output.shape[2]))

        x = self.fc(output)

        return x, states

embedding_dim = 100
units = 512

model = Model(vocab_size, embedding_dim, units, BATCH_SIZE)

optimizer = tf.optimizers.Adam()

checkpoint_dir = "./models/training_checkpoints_15_strip"
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)

def loss_function(labels, logits):
    # return tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

# for epoch in range(EPOCHS):
#     start = time.time()

#     hidden = model.reset_states()

#     for (batch, (input, target)) in enumerate(dataset):
#         with tf.GradientTape() as tape:
#             predictions, hidden = model(input, hidden)

#             target = tf.reshape(target, (-1,))
#             loss = loss_function(target, predictions)

#             grads = tape.gradient(loss, model.variables)
#             optimizer.apply_gradients(zip(grads, model.variables))

#             if batch % 100 == 0:
#                 # print("Epoch {} Batch {} Loss{:.4f}".format(epoch + 1, batch, loss))
#                 print("Epoch {} Batch {}".format(epoch + 1, batch))

#     if (epoch + 1) % 10 == 0:
#         checkpoint.save(file_prefix=checkpoint_prefix)

checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

start_string = "aç"

hidden = [tf.zeros((1, units))]

n_words = 5

for i in range(n_words):
    start_words = start_string.split()
    input_eval = [word2idx[i] for i in start_words]
    input_eval = tf.expand_dims(input_eval, 0)

    predictions, hidden = model(input_eval, hidden)

    predicted_id = tf.argmax(predictions[-1]).numpy()

    start_string += " " + idx2word[predicted_id]

print(start_string)
