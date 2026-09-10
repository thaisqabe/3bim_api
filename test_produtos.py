from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import ProdutoDB

client = TestClient(app)


def test_listar_produtos_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'Teclado'

    app.dependency_overrides.clear()


def test_criar_produto_com_mock():
    db_mock = MagicMock()

    def simular_refresh(produto):
        produto.id = 1  # simula o banco atribuindo um id ao registro

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_produto = {'nome': 'Monitor', 'preco': 799.90, 'quantidade': 5}
    resposta = client.post('/produtos', json=novo_produto)

    assert resposta.status_code == 201
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()

def test_buscar_produto_por_id_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = ProdutoDB(
        id=1,
        nome='Teclado',
        preco=89.90,
        quantidade=15
    )

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos/1')

    assert resposta.status_code == 200
    assert resposta.json()['id'] == 1
    assert resposta.json()['nome'] == 'Teclado'
    assert resposta.json()['preco'] == 89.90
    assert resposta.json()['quantidade'] == 15

    app.dependency_overrides.clear()


def test_atualizar_produto_com_mock():
    db_mock = MagicMock()

    produto_existente = ProdutoDB(
        id=1,
        nome='Teclado',
        preco=89.90,
        quantidade=15
    )

    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente

    app.dependency_overrides[get_db] = lambda: db_mock

    produto_atualizado = {
        'nome': 'Teclado Mecânico',
        'preco': 129.90,
        'quantidade': 20
    }

    resposta = client.put('/produtos/1', json=produto_atualizado)

    assert resposta.status_code == 200
    assert db_mock.commit.called

    app.dependency_overrides.clear()


def test_excluir_produto_com_mock():
    db_mock = MagicMock()

    produto_existente = ProdutoDB(
        id=1,
        nome='Teclado',
        preco=89.90,
        quantidade=15
    )

    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente

    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/produtos/1')

    assert resposta.status_code == 200
    db_mock.delete.assert_called_once_with(produto_existente)
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()