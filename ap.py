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
@app.route('/')
def home():
    server = '2'
    return render_template('index.html')

# Função responsável pelo controle das conexões com o servidor 1.
@socketio.on('connect')
def connect_handler():
    global clients
    # Adiciona o socket ID do cliente à lista de clientes conectados
    clients.add(request.sid)
    print(f'Cliente conectado: {request.sid}')
    socketio.emit('update_server_number', {'num_server': 2})
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

# Salva as mensagens do servidor em um .txt par que seja possível inciar o segundo sem perder nada
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
            global stop_server, exe
            if msg["message"] == 'stop':
                off()
            # Thread de salvar as mensagens
            save_data_thread = threading.Thread(target=save_data(msg), args=(request.sid,))
            save_data_thread.start()

            # Thread de mostrar mensagem para todos
            send_all_thread = threading.Thread(target=send_all(client_sid,msg), args=(request.sid,))
            send_all_thread.start()

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
    exe = False
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == '__main__':
    while exe:
        time.sleep(1)
        exe = check_connection('http://192.168.0.15:5000/')
        print(exe)
        pass
    socketio.run(app, host='192.168.0.15', port=5000)