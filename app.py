from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'perinbocadaparafuseta!'
io = SocketIO(app)

messages = []
clients = set()  # Conjunto para armazenar os clientes conectados


@app.route('/')
def home():
    return render_template("index.html")

@io.on('connect')
def connect_handler():
    global clients
    clients.add(request.sid)  # Adiciona o socket ID do cliente à lista de clientes conectados
    print(f'Cliente conectado: {request.sid}')
    # Outras ações que você deseja realizar quando um cliente se conecta

@io.on('disconnect')
def disconnect_handler():
    global clients
    clients.remove(request.sid)  # Remove o socket ID do cliente da lista de clientes conectados
    print(f'Cliente desconectado: {request.sid}')
    # Outras ações que você deseja realizar quando um cliente se desconecta


@io.on('sendMessage')
def send_message_handler(msg):
    salvar = f'{msg["name"]},, {msg["message"]}'
    # Salvar mensagem em um arquivo de texto
    with open('mensagens.txt', 'a') as file:
        file.write(salvar + '\n')
    emit('getMessage', msg, broadcast=True)

@io.on('message')
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
