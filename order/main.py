from flask import (Flask, render_template, request)
from kafkabroker import producerSend
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None, cors_allowed_origins="*")
thread = None
thread_lock = Lock()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/order")
@cross_origin()
def order():
    return render_template('order.html')

@socketio.on('producer', namespace='/kafka')
def producersend(msg):
    data = msg
    topics = ["warehouse", "finance"]
    for item in topics :
        mapped = {}
        if item == "warehouse" :
            mapped = {"No invoice": data["invoiceno"], "merk": data["barang"], "qty": data["qty"]}
        else:
            mapped = {"No invoice": data["invoiceno"], "merk": data["barang"], "harga": data["price"],"qty": data["qty"]}
        
        producerSend(item, mapped)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
