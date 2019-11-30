from flask import Flask, request
from flask_restful import Api
from os import environ
import json
from flask_cors import cross_origin
import logging
import tensorflow as tf
import os
from MyModel import MyModel
from keras_preprocessing.text import Tokenizer
import io
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path='', static_folder='public')

file_path = "/home/ken/Documents/acik-hack/null-pointer-acik-hack/res/train.txt"

# text = io.open(file_path, "r", encoding="ISO8859-9").read()
text = io.open(file_path, "r").read()

tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])

encoded = tokenizer.texts_to_sequences([text])[0]

word2idx = tokenizer.word_index
idx2word = tokenizer.index_word

BATCH_SIZE = 1000
embedding_dim = 100
units = 512
vocab_size = 9915

model = MyModel(vocab_size, embedding_dim, units, BATCH_SIZE)
optimizer = tf.optimizers.Adam()
checkpoint_dir = "./models/training_checkpoints_sait_12"
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)

checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

@app.route("/predict", methods=["GET"])
@cross_origin(headers=['Content-Type'])
def get():
    return "Ne baktın yarram."

@app.route("/")
def homepage():
    return app.send_static_file("homepage.html")

@app.route("/predict", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def predict():

    start_string = request.json

    n_words = 10

    for i in range(n_words):
        start_words = start_string.split()
        input_eval = [word2idx[i] for i in start_words]
        input_eval = tf.expand_dims(input_eval, 0)

        predictions, hidden = model(input_eval, hidden)

        predicted_id = tf.argmax(predictions[-1]).numpy()

        start_string += " " + idx2word[predicted_id]

    response = app.response_class(
        response=json.dumps({"prediction" : start_string}),
        status=200,
        mimetype='application/json'
    )
    return response, 200

port = int(environ.get("PORT", 5000))
app.run(host="0.0.0.0", debug=True, port=port)
# app.run(host="0.0.0.0", port=port)
