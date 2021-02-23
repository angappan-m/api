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
        product_name = ""
        for x in perdaydatas.find():
            for i,p in enumerate(x['product_ids']):
                if p == product_id:
                    product_name = x['product_names'][i]
            if product_id in x['product_ids']:
                act_temp_c = x['act_temp_c']
                date = x['date']
                iotid = x['iot_id']
                pid = product_id
                pname = product_name
                req_temp = x['req_temp']
                output.append({"act_temp_c":act_temp_c,"date":date,"iotid":iotid,"product_id":pid,"product_name":pname,"req_temp":req_temp})
        return jsonify({'status':False,'message':'failed','data': output})

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
        
@app.route('/werehouseassignment',methods=['GET','POST'])
def werehouseassignment():
    pids = str(request.args['pids'])
    iotid = request.args['iotid']
    arr_pids = pids.split(',')
    iotAssignment = mongo.db.iotAssignment

    try:
        if iotAssignment.find({"iot_id": iotid}).count() > 0:
            #update
            query = {"iot_id": iotid}
            iotAssignment.update(query,{"$set" : {"product_ids": arr_pids}})
        else:
            #insert
            iotAssignment.insert_one({"iot_id":iotid,"product_ids": arr_pids})
        return jsonify({'status':True,'message':'success'})
    except:
        return jsonify({'status':False,'message':'failed'})


if __name__ == '__main__':
    app.run(debug=True)
