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

# Função responsável pelo controle das conexões com o servidor 1.
@socketio.on('connect')
def connect_handler():
    global clients
    clients.add(request.sid)  # Adiciona o socket ID do cliente à lista de clientes conectados
    print(f'Cliente conectado: {request.sid}')
    socketio.emit('update_server_number', {'num_server': './static/imgs/1.png'})
    if clients != '':
        # Cria uma nova thread para processar a conexão do cliente
        thread = threading.Thread(target=client_thread, args=(request.sid,))
        thread.start()

# Função responsável pelo controle das desconexões com o servidor 1.
@socketio.on('disconnect')
def disconnect_handler():
    global clients
    clients.remove(request.sid)  # Remove o socket ID do cliente da lista de clientes conectados
    print(f'Cliente desconectado: {request.sid}')
    # Outras ações que você deseja realizar quando um cliente se desconecta

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

def send_all(client_sid, msg):
    emit('getMessage', msg, broadcast=True)
    print(f'Mensagem enviada pelo cliente: {client_sid},{msg}')

def client_thread(client_sid):
    # Lógica para processar a conexão do cliente em uma nova thread
    while True:
        @socketio.on('sendMessage')
        def send_message_handler(msg):
            global stop_server, exe
            if msg["message"] == 'stop':
                off()
            salvar = f'{msg["name"]},, {msg["message"]}'
            # Salvar mensagem em um arquivo de texto
            with open('mensagens.txt', 'a') as file:
                file.write(salvar + '\n')
            send_all_thread = threading.Thread(target=send_all(client_sid,msg), args=(request.sid,))
            send_all_thread.start()
    def client_message_handler():
        pass


    client_message_thread = threading.Thread(target=client_message_handler)
    client_message_thread.start()

def off():
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='192.168.2.104', port=5000)