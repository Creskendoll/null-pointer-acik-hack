import tensorflow as tf

class MyModel(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, units, batch_size):
        super(MyModel, self).__init__()
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

