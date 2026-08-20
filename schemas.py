from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int




class FuncionarioBase(BaseModel):
    nome: str
    cargo: str
    departamento: str
    salario: float


class FuncionarioCreate(FuncionarioBase):
    pass


class FuncionarioResponse(FuncionarioBase):
    id: int


class Config:
    from_attributes = True
