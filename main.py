from flask import request
from flask_socketio import SocketIO, emit, send
import threading
import os
import signal
from rotas import app


socketio = SocketIO(app)
messages = []
clients = set()  # Conjunto para armazenar os clientes conectados


# Função responsável pelo controle das conexões com o servidor 1.
@socketio.on('connect')
def connect_handler():
    global clients
    # Adiciona o socket ID do cliente à lista de clientes conectados
    clients.add(request.sid)
    print(f'Cliente conectado: {request.sid}')
    socketio.emit('update_server_number', {'num_server': './static/imgs/1.png'})
    # Verifica se há algum cliente, se houver, cria uma cliente para cada com base no seu ID
    if clients != '':
        # Cria uma nova thread para processar a conexão do cliente
        thread = threading.Thread(target=client_thread, args=(request.sid,))
        thread.start()

# Função responsável pelo controle das desconexões com o servidor 1.
@socketio.on('disconnect')
def disconnect_handler():
    global clients, client_threads
    print(client_threads)
    client_sid = request.sid
    clients.remove(client_sid)  # Remove o socket ID do cliente da lista de clientes conectados
    print(f'Cliente desconectado: {client_sid}')


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

def save_data(msg):
    salvar = f'{msg["name"]},, {msg["message"]}'
    # Salvar mensagem em um arquivo de texto
    with open('mensagens.txt', 'a') as file:
        file.write(salvar + '\n')

# Função responsável por enviar a mensagem do servidor para todos os clientes conectados
def send_all(client_sid, msg):
    # emit envia a mensagem para o JavaScript no "index.html"
    emit('getMessage', msg, broadcast=True)
    print(f'Mensagem enviada pelo cliente: {client_sid},{msg}')

def client_thread(client_sid):
    # Lógica para processar a conexão do cliente em uma nova thread
    while True:
        @socketio.on('sendMessage')
        def send_message_handler(msg):
            if msg["message"] == 'stop':
                off()
            # Thread de salvar as mensagens
            save_data_thread = threading.Thread(target=save_data(msg), args=(request.sid,))
            save_data_thread.start()

            # Thread de mostrar mensagem para todos
            send_all_thread = threading.Thread(target=send_all(client_sid,msg), args=(request.sid,))
            send_all_thread.start()

# Função para realizar o teste do servidor de backup
def off():
    os.kill(os.getpid(), signal.SIGINT)




