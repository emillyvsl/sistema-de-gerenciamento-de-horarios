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

// Função para excluir disciplina
window.excluirDisciplina = function(disciplinaId) {
    console.log("Função excluirDisciplina chamada com ID:", disciplinaId); // Imprime no console o ID da disciplina que será excluída.

    $.ajax({
        type: 'POST', // Define o método HTTP como POST.
        url: baseExcluirDisciplinaUrl.replace('0', disciplinaId), // Substitui '0' na URL base pela ID da disciplina para a solicitação.
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
            console.error('Erro ao excluir a disciplina:', status, error); // Imprime detalhes do erro no console.
            alert('Ocorreu um erro ao excluir a disciplina.'); // Exibe um alerta se ocorrer um erro durante a exclusão.
        }
    });
};

$(document).ready(function() {
    // Abrir o modal de edição e preencher os dados da disciplina
    $('#editarDisciplinaModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);  // Botão que acionou o modal
        var disciplinaId = button.data('id');
        var disciplinaNome = button.data('nome');
        var periodoId = button.data('periodo');  // ID do período selecionado

        var modal = $(this);
        modal.find('#id_nome').val(disciplinaNome);  // Preenche o campo nome
        modal.find('#id_periodo').val(periodoId);    // Preenche o campo período com o valor atual
        modal.find('#id_disciplina').val(disciplinaId);  // Insere o ID da disciplina
    });

    // Submeter o formulário de edição via AJAX
    $('#form-editar-disciplina').on('submit', function(e) {
        e.preventDefault();  // Prevenir comportamento padrão do formulário

        var disciplinaId = $('#id_disciplina').val();
        var editarUrl = baseEditarDisciplinaUrl.replace('0', disciplinaId);  // Atualiza a URL com o ID da disciplina

        $.ajax({
            type: 'POST',
            url: editarUrl,
            data: $(this).serialize(),  // Envia os dados do formulário
            success: function(response) {
                if (response.success) {
                    location.reload();  // Recarrega a página se a operação for bem-sucedida
                } else {
                    alert('Erro: ' + response.errors);
                }
            },
            error: function(xhr, status, error) {
                alert('Ocorreu um erro ao editar a disciplina.');
            }
        });
    });
});

$(document).ready(function() {
    var adicionarDisciplinaUrl = "{% url 'adicionar_disciplina_professor' %}";


    $('#adicionarDisciplinaModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Botão que acionou o modal
        var professorId = button.data('id'); // Extrai o ID do professor
        var modal = $(this);
        modal.find('#id_professor').val(professorId);
    });

    $('#form-adicionar-disciplina').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: adicionarDisciplinaUrl, // Usa a URL obtida do contexto do template
            type: 'POST',
            data: form.serialize(),
            success: function(response) {
                location.reload(); // Recarrega a página para atualizar a lista
            },
            error: function(xhr, status, error) {
                console.error('Erro:', error);
            }
        });
    });
});


$(document).ready(function() {
    $('#horas_preferidas').on('change', function() {
        var selectedHorarioId = $(this).val(); // Obtenha o ID do horário selecionado

        console.log("Horário selecionado: " + selectedHorarioId); // Debug

        if (selectedHorarioId) {
            // Faça a requisição AJAX apenas se um horário for selecionado
            $.ajax({
                url: buscarDiasRelacionadosUrl + "?horario_id=" + selectedHorarioId,
                method: "GET",
                success: function(response) {
                    // Supondo que response contenha os dias relacionados
                    $('#dias_relacionados').empty(); // Limpe os dias relacionados antes de adicionar novos
                    if (response.dias.length > 0) {
                        response.dias.forEach(function(dia) {
                            $('#dias_relacionados').append(`
                                <div>
                                    <input type="checkbox" id="dia-${dia.id}" name="dias_preferidos" value="${dia.id}">
                                    <label for="dia-${dia.id}">${dia.nome}</label>
                                </div>
                            `);
                        });
                    } else {
                        $('#dias_relacionados').append('<div>Nenhum dia relacionado encontrado.</div>');
                    }
                },
                error: function(xhr) {
                    console.error("Erro na requisição:", xhr);
                }
            });
        } else {
            $('#dias_relacionados').empty(); // Limpe os dias se nenhum horário for selecionado
        }
    });

    // Captura o envio do formulário de adicionar preferência
    $('#addPreferenciaModal form').on('submit', function(e) {
        e.preventDefault(); // Impede o envio padrão do formulário

        var formData = $(this).serialize(); // Captura os dados do formulário

        // Faz a requisição AJAX para enviar o formulário
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            success: function(response) {
                $('#addPreferenciaModal').modal('hide');
                alert('Preferência adicionada com sucesso.');
                // Opcionalmente, atualize a lista de preferências na página
            },
            error: function() {
                alert('Erro: Ocorreu um erro ao adicionar a preferência.');
            }
        });
    });


});
