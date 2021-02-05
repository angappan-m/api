from flask import Flask, jsonify,request
from datetime import datetime
from pytz import timezone
from flask_pymongo import PyMongo

# cluster = MongoClient("mongodb+srv://pharmaceuticalsdb:Pharmaceuticals123@pharmaceuticalscluster0.o91q1.mongodb.net/pharmaceuticalsDb?retryWrites=true&w=majority")
# db = cluster['pharmaceuticalsDb']
# collection = db['perDayDataLogs']
# data = list(collection.find())
#
# print(data)

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pharmaceuticalsDb'
app.config['MONGO_URI'] = 'mongodb+srv://pharmaceuticalsdb:Pharmaceuticals123@pharmaceuticalscluster0.o91q1.mongodb.net/pharmaceuticalsDb?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def home():
    return jsonify({"message":"welcome"})


@app.route('/datetimeapi',methods=['GET','POST'])
def datetime():
    date = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%Y-%m-%d')
    time = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%H:%M:%S')
    return jsonify({"status": True, "date": date, "time": time})

@app.route('/perdaydatalogs',methods=['GET','POST'])
def perdaydatalogs():
    if request.method == 'GET':
        device_id = int(request.args['device_id'])
        product_id = int(request.args['product_id'])
        perdaydatas = mongo.db.perDayDataLogs
        output = []
        for x in perdaydatas.find({"iot_id": device_id}):
            product_ids = x['product_ids']
            i = 0
            for y in product_ids:
                if y == product_id:
                    output.append({'product_id': product_id,'product_name': x['product_names'][i],'date': x['date'],'iot_id':x['iot_id'],'loc': x['loc_latlon'],'loc_deg': x['loc_latlondeg'],'act_temp_c': x['act_temp_c'],'light' : x['light'],'hum' : x['humidity'],'req_temp' : x['req_temp']})
                else:
                    i = i + 1

        return jsonify({'status':True,'message':'success','data': output})

if __name__ == '__main__':
    app.run(debug=True)
