
window.onload = function () {

    const socket = io('http://192.168.2.104:5000/');


    socket.on('update_server_number', function(data) {
    document.getElementById('num_server').src = data.num_server;
    });



    function addToChat(msg) {
      const span = document.createElement("span");
      const chat = document.querySelector(".chatbox");
      span.innerHTML = `<strong>${msg.name}</strong>: ${msg.message}`;
      chat.prepend(span); // Adiciona a mensagem no início da lista de mensagens

      chat.scrollTop = chat.scrollHeight; // Faz a rolagem para a parte inferior da caixa
    }

    socket.on('clear', ()=> {
        const chatbox = document.querySelector('.chatbox');
        chatbox.innerHTML = '';
    })

    socket.on('connect', () => {
        socket.send('Usuário conectado ao socket');
    });

    document.querySelector("form").addEventListener("submit", function (event) {
        event.preventDefault();
        const name = event.target[0].value;
        const message = event.target[1].value;
        socket.emit('sendMessage', {name, message});
        event.target[1].value = '';
    });

    socket.on('getMessage', (msg) => {
        addToChat(msg);
    });

    socket.on('message', (msgs) => {
        for (const msg of msgs) {
            addToChat(msg);
        }
    });
}


  // Configurar a animação do Lottie
  var animation = bodymovin.loadAnimation({
  container: document.getElementById('animation-container'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: './static/animation/3113-duck-blue-style.json'
});
var animation = bodymovin.loadAnimation({
  container: document.getElementById('animation-container1'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: './static/animation/67908-duck.json'
});
var animation = bodymovin.loadAnimation({
  container: document.getElementById('animation-container2'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: './static/animation/69959-monkey-animator.json'
});
