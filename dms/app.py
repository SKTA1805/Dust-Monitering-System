from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import serial

app = Flask(__name__)
socketio = SocketIO(app)
ser = serial.Serial('COM9', 9600)  # Replace 'COM3' with your serial port

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')  # Add a new route for the table page
def table():
    return render_template( 'table.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/favicon.ico')
def favicon():
    return '', 404

def read_serial():
    while True:
        data = ser.readline().decode().strip()
        socketio.emit('serial_data', {'data': data})
        socketio.emit('update_density_table', {'density': data})  # Add this line to update the table

if __name__ == '__main__':
    socketio.start_background_task(target=read_serial)
    socketio.run(app)
