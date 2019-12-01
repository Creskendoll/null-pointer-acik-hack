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
import requests
from OpenSSL import SSL
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file('./keyac.pem')
context.use_certificate_file('./certac.pem')
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path='', static_folder='public')

file_path = "./res/out.txt"

# text = io.open(file_path, "r", encoding="ISO8859-9").read()
text = io.open(file_path, "r", encoding="ISO8859-9").read()

tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])

encoded = tokenizer.texts_to_sequences([text])[0]

word2idx = tokenizer.word_index
idx2word = tokenizer.index_word

BATCH_SIZE = 256
embedding_dim = 100
units = 512
vocab_size = len(tokenizer.word_index) + 1

model = MyModel(vocab_size, embedding_dim, units, BATCH_SIZE)
optimizer = tf.optimizers.Adam()
checkpoint_dir = "./models/new_out"
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)

checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir)).expect_partial()

@app.route("/summary", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def summary():
    res = requests.post("https://turkcemetinozetleme.teaddict.net/ozetle/api/new", data={
        "contextOfText":request.data.decode()
    }, headers={
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8;"
    })
    print(res.text)
    response = app.response_class(
        response=json.dumps({"summary" : res.json()}),
        status=200,
        mimetype='application/json'
    )
    return response, 200

@app.route("/paraphrase", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def paraphrase():
    base_url = "https://tr.m.wikiquote.org/w/index.php?search="
    query = request.data.decode()
    res = requests.post(base_url+query, data={
        "contextOfText":request.data.decode()
    }, headers={
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8;"
    })
    print(res.text)
    response = app.response_class(
        response=json.dumps({"paraphrase" : res.json()}),
        status=200,
        mimetype='application/json'
    )
    return response, 200

@app.route("/", methods=["GET"])
def homepage():
    return app.send_static_file("homepage.html")
    # return "Ne baktın yarram."

@app.route("/suggest", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def predict():
    try:
        start_string = request.data.decode()
        n_words = 5
        hidden = [tf.zeros((1, units))]

        for i in range(n_words):
            start_words = start_string.split()
            input_eval = [word2idx[i] for i in start_words]
            input_eval = tf.expand_dims(input_eval, 0)

            predictions, hidden = model(input_eval, hidden)

            predicted_id = tf.argmax(predictions[-1]).numpy()

            start_string += " " + idx2word[predicted_id]

        print(start_string)
        response = app.response_class(
            response=json.dumps({"prediction" : start_string}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
        return response, 200
    except Exception as e:
        print(e)
        print(e.with_traceback())

port = int(environ.get("PORT", 5000))
# app.run(host="0.0.0.0", debug=True, port=port)
# app.run(host="0.0.0.0", debug=True, port=port, ssl_context=("certac.pem", "keyac.pem"))
app.run(host="0.0.0.0", debug=True, port=port)
# app.run(host="0.0.0.0", port=port)
