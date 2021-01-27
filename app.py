from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

print(str(datetime.now()).split(' '))


@app.route('/')
def home():
    date = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%Y-%m-%d')
    time = datetime.now().astimezone(timezone('Asia/Calcutta')).strftime('%H:%M:%S')
    return jsonify({"status": True, "date": date, "time": time})


if __name__ == '__main__':
    app.run(debug=True)
