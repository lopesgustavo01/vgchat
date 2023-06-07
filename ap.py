from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

# Dicionário de threads dos usuários
user_threads = {}


@socketio.on('connect')
def handle_connect():
    # Cria uma nova thread para processar a conexão do cliente
    thread = threading.Thread(target=handle_client)
    thread.start()


@socketio.on('disconnect')
def handle_disconnect():
    # Remove o usuário da lista de usuários conectados e finaliza a thread correspondente
    user_id = request.sid
    user_threads[user_id]['running'] = False
    del user_threads[user_id]


@socketio.on('message')
def handle_message(data):
    user_id = request.sid
    user_threads[user_id]['message'] = data['message']


def handle_client():
    user_id = request.sid

    # Cria uma nova thread para cuidar do usuário
    thread = threading.Thread(target=handle_user, args=(user_id,))
    user_threads[user_id] = {'thread': thread, 'message': None, 'running': True}
    thread.start()


def handle_user(user_id):
    while user_threads[user_id]['running']:
        # Verifica se há uma nova mensagem para o usuário
        if user_threads[user_id]['message']:
            message = user_threads[user_id]['message']
            emit('message', {'user_id': user_id, 'message': message}, broadcast=True)
            user_threads[user_id]['message'] = None

        socketio.sleep(1)  # Aguarda 1 segundo antes de verificar novamente


@app.route('/')
def index():
    return render_template('index1.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
