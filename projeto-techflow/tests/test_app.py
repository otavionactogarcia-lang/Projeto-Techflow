import os
import sys
import pytest

# Garante que o Python encontre a pasta src dentro de projeto-techflow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app, tarefas

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Limpa a lista antes de cada teste para evitar lixo de dados
    tarefas.clear()
    tarefas.extend([
        {"id": 1, "titulo": "Revisar rotas de entrega", "status": "Pendente", "prioridade": "Alta"},
        {"id": 2, "titulo": "Cadastrar novo motorista", "status": "Concluído", "prioridade": "Média"}
    ])
    with app.test_client() as client:
        yield client

def test_listar_tarefas(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"TechFlow Solutions" in response.data

def test_adicionar_tarefa(client):
    response = client.post('/adicionar', data={'titulo': 'Tarefa de Teste Automatizado'}, follow_redirects=True)
    assert response.status_code == 200
    assert any(t['titulo'] == 'Tarefa de Teste Automatizado' for t in tarefas)

def test_deletar_tarefa(client):
    # Usamos o ID 1 que foi resetado e garantido pela fixture
    id_para_deletar = 1
    response = client.get(f'/deletar/{id_para_deletar}', follow_redirects=True)
    assert response.status_code == 200
    assert not any(t['id'] == id_para_deletar for t in tarefas)
