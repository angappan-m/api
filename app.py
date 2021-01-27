from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

print(str(datetime.now()).split(' '))


@app.route('/')
def home():
    date_time = str(datetime.now()).split(' ')
    date = date_time[0]
    time = date_time[1].split('.')[0]
    return jsonify({"status": True, "date": date, "time": time})


if __name__ == '__main__':
    app.run(debug=True)
