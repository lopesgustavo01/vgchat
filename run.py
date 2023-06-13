from teste import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True, host='192.168.2.104', port=5000)