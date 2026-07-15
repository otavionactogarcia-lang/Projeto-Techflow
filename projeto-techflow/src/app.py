from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados temporário em memória (uma lista de dicionários)
tarefas = [
    {"id": 1, "titulo": "Estudar Engenharia de Software", "status": "A Fazer"},
    {"id": 2, "titulo": "Configurar pipeline de CI", "status": "Em Progresso"}
]

@app.route('/')
def index():
    # READ: Lê as tarefas e renderiza na tela
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    # CREATE: Adiciona uma nova tarefa à lista
    titulo = request.form.get('titulo')
    if titulo:
        novo_id = max([t['id'] for t in tarefas], default=0) + 1
        tarefas.append({"id": novo_id, "titulo": titulo, "status": "A Fazer"})
    return redirect(url_for('index'))

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    # UPDATE: Atualiza o status de uma tarefa existente
    novo_status = request.form.get('status')
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa['status'] = novo_status
            break
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    # DELETE: Remove uma tarefa da lista
    global tarefas
    tarefas = [t for t in tarefas if t['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)