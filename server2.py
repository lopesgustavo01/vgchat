from main import *
import time, requests

exe = True

@socketio.on('connect')
def connect_handler():
    global clients
    # Adiciona o socket ID do cliente à lista de clientes conectados
    clients.add(request.sid)
    print(f'Cliente conectado: {request.sid}')
    socketio.emit('update_server_number', {'num_server': './static/imgs/2.png'})
    # Verifica se há algum cliente, se houver, cria uma cliente para cada com base no seu ID
    if clients != '':
        # Cria uma nova thread para processar a conexão do cliente
        thread = threading.Thread(target=client_thread, args=(request.sid,))
        thread.start()

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
        exe = check_connection('http://192.168.0.15:5000/')
        print(exe)
        pass
    socketio.run(app, debug=True, host='192.168.0.15', port=5000)