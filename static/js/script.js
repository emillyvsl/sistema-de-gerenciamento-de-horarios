// Verifique se jQuery está carregado
console.log(typeof $); // Deve imprimir 'function' - Verifica se o jQuery foi carregado corretamente e se a variável `$` é uma função.

// Configurar jQuery para incluir o CSRF token em todas as solicitações
$.ajaxSetup({
    headers: {
        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content') // Adiciona o token CSRF às cabeçalhos de todas as solicitações AJAX.
    }
});

// Função para excluir professor
window.excluirProfessor = function(professorId) {
    console.log("Função excluirProfessor chamada com ID:", professorId); // Imprime no console o ID do professor que será excluído.
    
    $.ajax({
        type: 'POST', // Define o método HTTP como POST.
        url: baseExcluirProfessorUrl.replace('0', professorId), // Substitui '0' na URL base pela ID do professor para a solicitação.
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken') // Inclui o token CSRF obtido através da função `getCookie` nos dados da solicitação.
        },
        success: function(response) {
            console.log("Resposta de sucesso recebida:", response); // Imprime a resposta da solicitação bem-sucedida no console.
            if (response.success) {
                location.reload(); // Recarrega a página se a exclusão for bem-sucedida.
            } else {
                alert('Erro: ' + response.error); // Exibe um alerta com a mensagem de erro se a exclusão falhar.
            }
        },
        error: function(xhr, status, error) {
            console.error('Erro ao excluir o professor:', status, error); // Imprime detalhes do erro no console.
            alert('Ocorreu um erro ao excluir o professor.'); // Exibe um alerta se ocorrer um erro durante a exclusão.
        }
    });
};

// Função para obter o valor do cookie CSRF
function getCookie(name) {
    let cookieValue = null; // Inicializa a variável que armazenará o valor do cookie.
    if (document.cookie && document.cookie !== '') { // Verifica se há cookies disponíveis.
        const cookies = document.cookie.split(';'); // Divide os cookies em um array.
        for (let i = 0; i < cookies.length; i++) { // Itera sobre cada cookie.
            const cookie = cookies[i].trim(); // Remove espaços em branco ao redor do cookie.
            if (cookie.substring(0, name.length + 1) === (name + '=')) { // Verifica se o cookie é o que estamos procurando.
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); // Decodifica e armazena o valor do cookie.
                break; // Sai do loop após encontrar o cookie.
            }
        }
    }
    return cookieValue; // Retorna o valor do cookie encontrado.
}


$(document).ready(function() { // Espera até que o DOM esteja completamente carregado.
    console.log("jQuery está carregado e funcionando!"); // Imprime no console que o jQuery foi carregado corretamente.

    // Preencher o modal de edição com os dados do professor
    $('#editarProfessorModal').on('show.bs.modal', function(event) {
        console.log("Evento show.bs.modal disparado"); // Imprime no console quando o modal de edição é exibido.
        
        var button = $(event.relatedTarget); // Obtém o botão que abriu o modal.
        var professorId = button.data('id'); // Obtém o ID do professor a partir dos dados do botão.
        var professorNome = button.data('nome'); // Obtém o nome do professor a partir dos dados do botão.
        var professorCentro = button.data('centro'); // Obtém o centro do professor a partir dos dados do botão.
        
        var modal = $(this); // Obtém o modal atual.
        modal.find('#id_nome').val(professorNome); // Preenche o campo de nome no modal com o nome do professor.
        modal.find('#id_centro').val(professorCentro); // Preenche o campo de centro no modal com o centro do professor.
        modal.find('#id_professor').val(professorId); // Preenche o campo de ID no modal com o ID do professor.
        console.log("Modal preenchido com ID:", professorId, "Nome:", professorNome, "Centro:", professorCentro); // Imprime no console os dados preenchidos no modal.
    });

    // Manipular o envio do formulário de edição
    $('#form-editar-professor').on('submit', function(e) {
        e.preventDefault(); // Previne o envio padrão do formulário.
        console.log("Formulário de edição enviado"); // Imprime no console que o formulário de edição foi enviado.

        var professorId = $('#id_professor').val(); // Obtém o ID do professor a partir do campo oculto no formulário.
        var editarUrl = baseEditarProfessorUrl.replace('0', professorId); // Substitui '0' na URL base pela ID do professor para a solicitação.

        $.ajax({
            type: 'POST', // Define o método HTTP como POST.
            url: editarUrl, // Define a URL para a solicitação AJAX.
            data: $(this).serialize(), // Serializa os dados do formulário para enviar na solicitação.
            success: function(response) {
                console.log("Resposta de sucesso recebida:", response); // Imprime a resposta da solicitação bem-sucedida no console.
                if (response.success) {
                    location.reload(); // Recarrega a página se a edição for bem-sucedida.
                } else {
                    alert('Erro: ' + response.error); // Exibe um alerta com a mensagem de erro se a edição falhar.
                }
            },
            error: function(xhr, status, error) {
                console.error('Erro ao editar o professor:', status, error); // Imprime detalhes do erro no console.
                alert('Ocorreu um erro ao editar o professor.'); // Exibe um alerta se ocorrer um erro durante a edição.
            }
        });
    });

    // Função para remover mensagens automáticas
    var mensagemTimeout = 4000; // 5 segundos
    setTimeout(function() {
        $('.alert').fadeOut('slow'); // Faz com que as mensagens de alerta desapareçam lentamente após 5 segundos.
    }, mensagemTimeout);
});
