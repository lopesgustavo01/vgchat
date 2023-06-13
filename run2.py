from teste import app, socketio
import time, requests


exe = True

def check_connection(url):
    try:
        response = requests.get(url)
        print(response)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


if __name__ == '__main__':
    while exe:
        time.sleep(1)
        exe = check_connection('http://192.168.2.104:5000/')
        print(exe)
        pass
    socketio.run(app, debug=True, host='192.168.2.104', port=5000)