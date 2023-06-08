from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
import threading
import os
import signal


app = Flask(__name__)
app.config['SECRET_KEY'] = 'perinbocadaparafuseta!'
socketio = SocketIO(app)
messages = []
clients = set()  # Conjunto para armazenar os clientes conectados

@app.route('/')
def home():

    server = '1'
    return render_template('index.html')


@socketio.on('connect')
def connect_handler():
    global clients
    clients.add(request.sid)  # Adiciona o socket ID do cliente à lista de clientes conectados
    print(f'Cliente conectado: {request.sid}')
    socketio.emit('update_server_number', {'num_server': 1})



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

def off():
    global exe
    exe = True
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    #server_thread = threading.Thread(target=stop_server_thread)
    #server_thread.start()
    socketio.run(app, debug=True, host='192.168.2.104', port=5000)
    #server_thread.join()


