from main import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True, host='192.168.0.15', port=5000)