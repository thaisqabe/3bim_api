from fastapi import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB
from models import FuncionarioDB

from schemas import ProdutoCreate, ProdutoResponse
from schemas import FuncionarioCreate, FuncionarioResponse

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine) # cria as tabelas, se ainda não existirem

app = FastAPI()

app.add_middleware(
 CORSMiddleware,
 allow_origins=['*'],
 # em produção, restringir para o domínio real do front-end
 allow_methods=['*'],
 allow_headers=['*'],
)


@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()


@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

@app.delete('/produtos/{produto_id}', status_code=200)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()
    return {'mensagem': 'Produto excluído!'}

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)
    return produto




@app.get('/funcionarios', response_model=list[FuncionarioResponse])
def listar_funcionarios(db: Session = Depends(get_db)):
    return db.query(FuncionarioDB).all()


@app.post('/funcionarios', response_model=FuncionarioResponse, status_code=201)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    novo_funcionario = FuncionarioDB(**funcionario.dict())
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)
    return novo_funcionario


@app.get('/funcionarios/{funcionario_id}', response_model=FuncionarioResponse)
def obter_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == funcionario_id).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    return funcionario


@app.delete('/funcionarios/{funcionario_id}', status_code=200)
def remover_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == funcionario_id).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    db.delete(funcionario)
    db.commit()
    return {'mensagem': 'Funcionário excluído!'}


@app.put('/funcionarios/{funcionario_id}', response_model=FuncionarioResponse)
def atualizar_funcionario(funcionario_id: int, dados: FuncionarioCreate, db: Session = Depends(get_db)):
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == funcionario_id).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    funcionario.nome = dados.nome
    funcionario.salario = dados.salario
    funcionario.cargo = dados.cargo
    funcionario.departamento = dados.departamento
    db.commit()
    db.refresh(funcionario)
    return funcionario
