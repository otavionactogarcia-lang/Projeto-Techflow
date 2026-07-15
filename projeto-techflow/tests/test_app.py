import os
import sys
import pytest

# Garante que o Python encontre a pasta src dentro de projeto-techflow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_listar_tarefas(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"TechFlow Solutions" in response.data

def test_adicionar_tarefa(client):
    response = client.post('/adicionar', data={'titulo': 'Item Unico de Teste'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Item Unico de Teste" in response.data

def test_deletar_tarefa(client):
    # 1. Adiciona uma tarefa com título bem específico
    client.post('/adicionar', data={'titulo': 'Tarefa Para Apagar'}, follow_redirects=True)
    
    # 2. Vamos buscar o ID dela diretamente na página inicial simulada
    # Como não temos banco real, vamos tentar disparar a rota de deletar com ID 1 ou o ID gerado.
    # Para garantir, deletamos o ID 1 que costuma ser o padrão inicial
    response = client.get('/deletar/1', follow_redirects=True)
    
    # 3. O status precisa ser 200 (OK)
    assert response.status_code == 200
    
    # 4. A tarefa não deve mais aparecer no texto da página renderizada
    assert b"Tarefa Para Apagar" not in response.data
