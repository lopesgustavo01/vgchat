from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'perinbocadaparafuseta!'


#--------------Rotas-----------------

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

#-----------importante pra teste-----------
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('username', '', expires=0)
    return response

#----------login------------------

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    vai = False
    with open("accounts.txt", 'r') as file:
        for line in file:
            b = line.rstrip('\n').split(',,')
            print(b[0], username, b[1], password)
            if b[0] == username and b[1] == password:
                response = make_response(redirect(url_for('home')))
                response.set_cookie('username', username)
                return response

    print('errou')
    return render_template('login.html', erro='senha ou login errado')


@app.route('/login')
def r_login():
    return render_template('login.html')

#parte menu
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
        return redirect(url_for('r_login'))
