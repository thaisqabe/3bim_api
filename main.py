from fastapi import FastAPI

app = FastAPI()

@app.get('/')  #@ decorator

def raiz():
    return {'mensagem': 'Minha primeira API em FastAPI!'}

@app.get('/sobre')
def sobre():
    return {'mensagem': 'Página sobre o site'}