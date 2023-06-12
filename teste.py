from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask_socketio import SocketIO, emit, send
import threading
import os
import signal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'perinbocadaparafuseta!'
socketio = SocketIO(app)
messages = []
clients = set()  # Conjunto para armazenar os clientes conectados

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Faça o que quiser com os dados do formulário, como salvar em um banco de dados
        salvar = f'{username},,{password}'
        # Salvar mensagem em um arquivo de texto
        with open('accounts.txt', 'a') as file:
            file.write(salvar + '\n')

        print("Olá")
        return redirect(url_for('home'))

@app.route('/register')
def retorna():
    return render_template("register.html")


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('/')))
    response.set_cookie('username', '', expires=0)
    return response

@app.route('/login', methods=['POST'])
def login():
    #data = request.get_json()
    username = request.form('username')
    password = request.form('password')
    username2 = False
    with open("accounts.txt", 'r') as file:
        while True:
            a = file.readline().rstrip('\n')
            if a == '':
                break
            b = a.split(',,')
            print(b)
            if b[0] == username:
                print(b[1], password)
                if b[1] == password:
                    username2 = True
                    print("DEU PORRA")
                    break
    if username2:
        response = make_response(redirect(url_for('/')))
        response.set_cookie('username', username)
        return response
    else:
        return jsonify({'success': False}), 401

@app.route('/login')
def retorna_login():
    return render_template('teste.html')

@app.route('/')
def home():
    # Verifique se o cookie de usuário existe para determinar se o usuário está logado
    server = '1'
    username = request.cookies.get('username')
    if username:
        # Usuário está logado
        return render_template('index.html', username=username)
    else:
        # Usuário não está logado
        return redirect(url_for('/login'))

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

# Salva as mensagens do servidor em um .txt para que seja possível iniciar o segundo servidor sem perder nada
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

# Função para realizar o teste do servidor de backup
def off():
    os.kill(os.getpid(), signal.SIGINT)



if __name__ == '__main__':
    socketio.run(app, debug=True, host='192.168.0.115', port=5000, allow_unsafe_werkzeug=True)
