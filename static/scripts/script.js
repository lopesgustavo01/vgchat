window.onload = function() {
  const socket = io('http://192.168.2.104:5000/');


  socket.on('update_server_number', function(data) {
    document.getElementById('num_server').src = data.num_server;
  });

  function addToChat(msg) {
    const span = document.createElement('span');
    const chat = document.querySelector('.chatbox');
    span.innerHTML = `<strong>${msg.name}</strong>: ${msg.message}`;
    chat.prepend(span); // Adiciona a mensagem no início da lista de mensagens
    chat.scrollTop = chat.scrollHeight; // Faz a rolagem para a parte inferior da caixa
  }

  socket.on('clear', () => {
    const chatbox = document.querySelector('.chatbox');
    chatbox.innerHTML = '';
  });


  document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.querySelector('p').textContent;
    const message = document.querySelector('input').value;
    socket.emit('sendMessage', { name: name, message: message });
    document.querySelector('input').value = '';
});


  socket.on('getMessage', (msg) => {
    addToChat(msg);
  });

  socket.on('message', (msgs) => {
    for (const msg of msgs) {
      addToChat(msg);
    }
  });



  var animation = bodymovin.loadAnimation({
    container: document.getElementById('animation-container'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: './static/animation/3113-duck-blue-style.json'
  });

  var animation1 = bodymovin.loadAnimation({
    container: document.getElementById('animation-container1'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: './static/animation/67908-duck.json'
  });

  var animation2 = bodymovin.loadAnimation({
    container: document.getElementById('animation-container2'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: './static/animation/69959-monkey-animator.json'
  });
};

document.getElementById('logout-link').addEventListener('click', function(event) {
        event.preventDefault();
        // Envia uma solicitação para a rota '/logout'
        fetch('/logout')
            .then(function(response) {
                // Redireciona para a página inicial após o logout
                window.location.href = '/';
            });
    });

function showChat() {
    var animation = document.getElementById('vg-chat-animation');
            animation.style.display = 'none';
    var chat = document.getElementById('chat');
    chat.style.display = 'flex';
}