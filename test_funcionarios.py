from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import FuncionarioDB

client = TestClient(app)


def test_listar_funcionarios_com_mock():
    db_mock = MagicMock()

    db_mock.query.return_value.all.return_value = [
        FuncionarioDB(
            id=1,
            nome='João Silva',
            departamento='TI',
            cargo='Desenvolvedor',
            salario=5000.00
        )
    ]

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/funcionarios')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'João Silva'

    app.dependency_overrides.clear()


def test_criar_funcionario_com_mock():
    db_mock = MagicMock()

    def simular_refresh(funcionario):
        funcionario.id = 1  # simula o banco atribuindo um id

    db_mock.refresh.side_effect = simular_refresh

    app.dependency_overrides[get_db] = lambda: db_mock

    novo_funcionario = {
        'nome': 'Maria Souza',
        'departamento': 'RH',
        'cargo': 'Analista de RH',
        'salario': 4500.00
    }

    resposta = client.post('/funcionarios', json=novo_funcionario)

    assert resposta.status_code == 201
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


def test_buscar_funcionario_por_id_com_mock():
    db_mock = MagicMock()

    db_mock.query.return_value.filter.return_value.first.return_value = FuncionarioDB(
        id=1,
        nome='João Silva',
        departamento='TI',
        cargo='Desenvolvedor',
        salario=5000.00
    )

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/funcionarios/1')

    assert resposta.status_code == 200
    assert resposta.json()['id'] == 1
    assert resposta.json()['nome'] == 'João Silva'
    assert resposta.json()['departamento'] == 'TI'
    assert resposta.json()['cargo'] == 'Desenvolvedor'
    assert resposta.json()['salario'] == 5000.00

    app.dependency_overrides.clear()


def test_atualizar_funcionario_com_mock():
    db_mock = MagicMock()

    funcionario_existente = FuncionarioDB(
        id=1,
        nome='João Silva',
        departamento='TI',
        cargo='Desenvolvedor',
        salario=5000.00
    )

    db_mock.query.return_value.filter.return_value.first.return_value = funcionario_existente

    app.dependency_overrides[get_db] = lambda: db_mock

    funcionario_atualizado = {
        'nome': 'João Silva',
        'departamento': 'TI',
        'cargo': 'Desenvolvedor Sênior',
        'salario': 7000.00
    }

    resposta = client.put('/funcionarios/1', json=funcionario_atualizado)

    assert resposta.status_code == 200
    assert db_mock.commit.called

    app.dependency_overrides.clear()


def test_excluir_funcionario_com_mock():
    db_mock = MagicMock()

    funcionario_existente = FuncionarioDB(
        id=1,
        nome='João Silva',
        departamento='TI',
        cargo='Desenvolvedor',
        salario=5000.00
    )

    db_mock.query.return_value.filter.return_value.first.return_value = funcionario_existente

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/funcionarios/1')

    assert resposta.status_code == 200
    db_mock.delete.assert_called_once_with(funcionario_existente)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()