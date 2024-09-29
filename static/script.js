function atualizaStatus() {
    $.ajax({
        url: '/geladeira',
        method: 'GET', // Assegure-se de que a rota aceita o método GET
        success: function (data) {
            // Verifica se os dados retornam corretamente
            if (data.temperatura && data.porta) {
                $('#temperatura').text('Temperatura atual: ' + data.temperatura + '°C');
                $('#porta').text('Situação atual: ' + data.porta);
            } else {
                console.log('Erro: Dados inválidos recebidos', data);
            }
        },
        error: function (xhr, status, error) {
            console.log('Erro na requisição:', error);
        }
    });
}

$(document).ready(function () {
    atualizaStatus();
    setInterval(atualizaStatus, 5000); // Atualiza a cada 5 segundos
});
