from flask import Flask, jsonify
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

@app.route('/datetimeapi')
def home():
    date = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%Y-%m-%d')
    time = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%H:%M:%S')
    return jsonify({"status": True, "date": date, "time": time})


if __name__ == '__main__':
    app.run(debug=True)
