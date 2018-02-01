from flask import Flask, request
from sys import stderr
import flask
from Final_Impact_Model import *


app = Flask(__name__)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route("/ParametersList", methods = ['POST'])
def get_results2():
  all_data = request.get_json()
  return flask.jsonify(getMyPlotJSON(all_data['params'], all_data['model'], all_data['params']['analysis_params']['fuel']))
  

def getMyPlotJSON(params, model, fuel):
  data = FinalImpactModel(params, model, fuel)
  return data.to_dict()


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
