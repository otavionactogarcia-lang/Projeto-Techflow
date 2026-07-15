import pytest
from src.app import app, tarefas

@pytest.fixture
def client():
    """
    Configura um cliente de testes simulado para interagir com o Flask
    sem a necessidade de rodar o servidor manualmente.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_listar_tarefas(client):
    """
    Testa se a página inicial (Read) carrega corretamente (Código 200)
    e exibe o título principal do projeto.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"TechFlow Solutions" in response.data

def test_adicionar_tarefa(client):
    """
    Testa a criação (Create) de uma tarefa simulando o envio do formulário
    e verifica se ela foi inserida corretamente na lista de memória.
    """
    # Envia os dados para a rota de adicionar
    response = client.post('/adicionar', data={'titulo': 'Tarefa de Teste Automatizado'}, follow_redirects=True)
    
    # Verifica se a página carregou com sucesso após o redirecionamento
    assert response.status_code == 200
    # Verifica se o elemento está no nosso "banco de dados" em memória
    assert any(t['titulo'] == 'Tarefa de Teste Automatizado' for t in tarefas)

def test_deletar_tarefa(client):
    """
    Testa a exclusão (Delete) de uma tarefa com base num ID existente
    e garante que ela deixa de constar na lista.
    """
    # Adiciona previamente uma tarefa para garantir que existe um registro
    client.post('/adicionar', data={'titulo': 'Tarefa para deletar'})
    id_para_deletar = tarefas[-1]['id']

    # Executa a rota de exclusão para esse ID
    response = client.get(f'/deletar/{id_para_deletar}', follow_redirects=True)
    
    # Verifica se o código respondeu com sucesso
    assert response.status_code == 200
    # Verifica se o ID realmente desapareceu do banco de dados temporário
    assert not any(t['id'] == id_para_deletar for t in tarefas)