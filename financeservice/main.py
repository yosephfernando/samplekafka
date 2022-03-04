import eventlet
eventlet.monkey_patch()

from flask import (Flask, render_template, request)
from financeconsumer import financCons
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def backgroundcons():
    print ("In background_stuff")
    latestmessage = financCons()
    for message in latestmessage:
        print(message.value)
        cleaned = json.loads(message.value)
        cleaned["total"] = int(cleaned["harga"]) * int(cleaned["qty"])
        socketio.emit("response", cleaned, namespace="/kafka")

def listen():
    while True:
        backgroundcons()
        eventlet.sleep(5)

eventlet.spawn(listen)

@app.route("/")
def finance():
    return render_template('finance.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
