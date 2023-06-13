$(document).ready(function() {
    $('#registration-form').submit(function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();

        $.ajax({
            type: 'POST',
            url: '/register',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
               window.location.href = '/login';
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#btn-voltar').click(function() {
        window.history.back(); // Voltar para a página anterior
    });
});