from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
import threading, time, requests, os
import signal


app = Flask(__name__)
app.config['SECRET_KEY'] = 'perinbocadaparafuseta!'
socketio = SocketIO(app)
messages = []
clients = set()  # Conjunto para armazenar os clientes conectados

exe = True


#funaçao pagina
@app.route('/')
def index():
    server = '2'
    return render_template('index.html')


@socketio.on('connect')
def connect_handler():
    global clients
    clients.add(request.sid)  # Adiciona o socket ID do cliente à lista de clientes conectados
    print(f'Cliente conectado: {request.sid}')
    socketio.emit('update_server_number', {'num_server': 2})
    socketio.emit('clear', room=request.sid)
    # Outras ações que você deseja realizar quando um cliente se conecta


@socketio.on('disconnect')
def disconnect_handler():
    global clients
    clients.remove(request.sid)  # Remove o socket ID do cliente da lista de clientes conectados
    print(f'Cliente desconectado: {request.sid}')
    # Outras ações que você deseja realizar quando um cliente se desconecta


@socketio.on('sendMessage')
def send_message_handler(msg):
    global stop_server, exe
    if msg["message"] == 'stop':
        off()
    salvar = f'{msg["name"]},, {msg["message"]}'
    # Salvar mensagem em um arquivo de texto
    with open('mensagens.txt', 'a') as file:
        file.write(salvar + '\n')
    emit('getMessage', msg, broadcast=True)


@socketio.on('message')
def message_handler(msg):
    messages = []
    with open('mensagens.txt', 'r') as file:
        while True:
            a = file.readline().rstrip('\n')
            if a == '':
                break
            b = a.split(',,')
            obj = {'name': b[0], 'message': b[1]}
            messages.append(obj)
    send(messages)


#funçao servidor
def check_connection(url):
    try:
        response = requests.get(url)
        print(response)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def off():
    global exe
    exe = True
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    while exe:
        time.sleep(1)
        exe = check_connection('http://192.168.2.104:5000/')
        print(exe)
        pass
    socketio.run(app, host='192.168.2.104', port=5000)

