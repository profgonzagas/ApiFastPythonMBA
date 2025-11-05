"""
Aplicação FastAPI principal
"""
from fastapi import FastAPI, HTTPException
from src.data.schemas import MessageInput, MessageOutput, PredictionInput, PredictionOutput

# Criar instância do FastAPI
app = FastAPI(
    title="ML MODEL API",
    version="1.0.0",
    description="API para servir o modelo de Machine Learning"
)


@app.get("/")
def root():
    """
    Endpoint raiz - mensagem de boas-vindas
    """
    return {"message": "API de ML está no ar!"}

@app.get("/health")
def health_check():
    """
    Health check - verifica se API está funcionando
    """
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/echo")
def echo_message(message: str):
    """
    Retorna a mesma mensagem recebida
    """
    return {
        "received": message,
        "length": len(message),
        "upper": message.upper()
    }

@app.get("/item/{item_id}")
def get_item(item_id: int):
    """
    Busca item por ID
    """
    # Simulando base de dados
    items = {
        1: {"name": "Mouse", "price": 50.0},
        2: {"name": "Teclado", "price": 150.0},
        3: {"name": "Monitor", "price": 800.0}
    }

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado")
    
    return items[item_id]

@app.get("/sobre")
def sobre():
    """
    Informações sobre o desenvolvedor
    """
    return {
        "nome": "Ana Silva",
        "motivo": "Quero colocar modelos ML em produção",
        "linguagem_principal": "Python",
        "hobby": "Fotografia"
        }


@app.post("/process-message", response_model=MessageOutput)
def process_message(message: MessageInput):
    """
    Processa mensagem com validação Pydantic
    """
    processed = message.text.upper()
    char_count = len(message.text)
    word_count = len(message.text.split())
    priority_labels = {
        1: "Baixa",
        2: "Média-Baixa",
        3: "Média",
        4: "Média-Alta",
        5: "Alta"
    }
    priority_label = priority_labels[message.priority]

    return MessageOutput(
        original_text=message.text,
        processed_text=processed,
        char_count=char_count,
        word_count=word_count,
        priority_label=priority_label
    )

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """
    Endpoint de predição (placeholder)
    Na próxima aula conectaremos com modelo real!
    """
    # Por enquanto, retorno fake
    return PredictionOutput(
        prediction=0,
        probability=0.95,
        model_version="1.0.0"
    )