from flask import Flask, jsonify,request
from datetime import datetime
from pytz import timezone
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pharmaceuticalsDb'
app.config['MONGO_URI'] = 'mongodb+srv://pharmaceuticalsdb:Pharmaceuticals123@pharmaceuticalscluster0.o91q1.mongodb.net/pharmaceuticalsDb?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def home():
    return jsonify({"message":"welcome"})


@app.route('/datetimeapi',methods=['GET','POST'])
def datetimeapi():
    date = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%Y-%m-%d')
    time = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%H:%M:%S')
    return jsonify({"status": True, "date": date, "time": time})

@app.route('/perdaydatalogs',methods=['GET','POST'])
def perdaydatalogs():
    if request.method == 'GET':
        product_id = int(request.args['product_id'])
        perdaydatas = mongo.db.perDayDataLogs
        output = []
        for x in perdaydatas.find():
            if product_id in x['product_ids']:
                device_id = x['iot_id']
                date = x['date']
                act_temp = x['act_temp_c']
                req_temp = x['req_temp']
                for i,pid in enumerate(x['product_ids']):
                    if pid == product_id:
                        pname = x['product_names'][i]
                return jsonify({'status':True,'message':'success','data': [{"iot_id": device_id,"product_id": product_id,"product_name": pname,"date":date,"act_temp_c":act_temp,"req_temp":req_temp}]})
        return jsonify({'status':False,'message':'failed','data': []})

@app.route('/werehouseusers',methods=['GET','POST'])
def werehouseusers():
    if request.method == 'GET':
        username = request.args['uname']
        password = request.args['pass']
        wereHouseUsers = mongo.db.wereHouseUsers
        for x in wereHouseUsers.find():
            if x['username'] == str(username) and x['password'] == str(password):
                return jsonify({'status':True,'message':'success'})
            # output.append({"username":x['username'],"password":x['password']})
            else:
                return jsonify({'status':False,'message':'failed'})
        

if __name__ == '__main__':
    app.run(debug=True)
