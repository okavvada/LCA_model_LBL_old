from __future__ import print_function
from sys import stderr
# steps:
# pip install flask
# Run server:
# FLASK_DEBUG=1 FLASK_APP=server.py flask run
import flask
from flask import Flask, request
from Final_Impact_Model import *


app = Flask(__name__)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route("/ParametersList", methods = ['POST'])
def get_results2():
  all_data = request.get_json()
  return flask.jsonify(getMyPlotJSON(all_data['params'], all_data['model']))

def getMyPlotJSON(params, model):
  data = FinalImpactModel(params, model)
  return data.to_dict()


if __name__ == '__main__':
    app.run()
