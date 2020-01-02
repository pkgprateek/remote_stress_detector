from flask import Flask,request,jsonify,render_template
import json
from functools import reduce
from datetime import datetime
app = Flask(__name__)

data = []
@app.route('/raw')
def raw():
  return jsonify(data)

def getdata():
  global data
  return data

def stress_predict():
  input = data[-1]['data']
  return -3.92535141+0.05534093*input

@app.route('/')
def index():
  print(data)
  return render_template('index.html',data=data,stressed = stress_predict())
@app.route('/data/writeout',methods = ['GET'])
def writeout():
  json.dump(data,open("DATABACKUP.json",'w'))
  return "WRITTEN"

@app.route('/<int:age>')
def indexbob(age):
  max_heartrate = 220-age
  sum = 0
  sum = reduce((lambda x,y:x+y),[x['data'] for x in data[-5::]])
  #sum = 20
  sum/=5.0
  if sum >= 0.5*max_heartrate and sum <=0.8*max_heartrate:
    return "Exercising"  + repr(sum)
  else:
    return "at Rest" + repr(sum)

@app.route('/data/readin',methods = ['GET'])
def readin():
  global data
  data = json.load(open("DATABACKUP.json"))
  return "WRITTEN"

@app.route('/data/add',methods = ['POST'])
def add_data():
  foo = dict()
  if not data:
    foo['id'] = 1
  else:   
    foo['id'] = data[-1]['id']+1
  foo['ip'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
  foo['data'] = int(request.json.get('data',))
  foo['timestamp'] = datetime.now().isoformat()
  data.append(foo)
  return jsonify({'data': foo}), 201


if __name__ == '__main__':
  app.run(debug=True)