
"""
Aplicação FastAPI principal
"""
import logging
from fastapi import FastAPI, HTTPException, Depends
from src.data.schemas import CalculatorInput, CalculatorOutput
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from  src.models.model_loader import ModelLoader
from pathlib import Path
from src.api.dependencies import get_model_loader
from src.data.schemas import TransactionInput, FraudPredictionOutput

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    #STARTUP
    logger.info("API iniciando")
    model_loader = get_model_loader()
    logger.info("Loader criado")
    model_loader.load_model(Path("artifacts/models/fraud_detection_model.pkl"))
    logger.info("Modelo carregado! API pronta.")


    yield

    logger.info("API encerrando")




# Criar instância do FastAPI
app = FastAPI(lifespan=lifespan,
    title="ML MODEL API",
    version="1.0.0",
    description="API para servir o modelo de Machine Learning"
)

logger.info("API iniciada com sucesso")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """
    Endpoint raiz - mensagem de boas-vindas
    """
    return {"message": "API de ML está no ar!"}

# Adicionar endpoint:
@app.post("/calcular", response_model=CalculatorOutput)
def calcular(entrada: CalculatorInput):
    """
    Realiza operações matemáticas básicas
    """
    logger.info(f"Recebida requisição de cálculo: {entrada.numero1} {entrada.operacao} {entrada.numero2}")

    num1 = entrada.numero1
    num2 = entrada.numero2
    op = entrada.operacao
    
    if op == "+":
        resultado = num1 + num2
    elif op == "-":
        resultado = num1 - num2
    elif op == "*":
        resultado = num1 * num2
    elif op == "/":
        if num2 == 0:
            logger.warning("Tentativa de divisão por zero")
            return CalculatorOutput(
                resultado=0,
                operacao=op,
                expressao=f"Erro: divisão por zero"
            )
        resultado = num1 / num2
    else:
        logger.error(f"Operação inválida: {op}")
        return CalculatorOutput(
            resultado=0,
            operacao=op,
            expressao=f"Operação inválida: {op}"
        )
    
    expressao = f"{num1} {op} {num2} = {resultado}"
    
    return CalculatorOutput(
        resultado=resultado,
        operacao=op,
        expressao=expressao
    )

# Função auxiliar para determinar nível de risco
def get_risk_level(probability: float) -> str:
    """Determina nível de risco baseado na probabilidade"""
    if probability < 0.3:
        return "BAIXO"
    elif probability < 0.7:
        return "MÉDIO"
    else:
        return "ALTO"

@app.post("/predict", response_model=FraudPredictionOutput)
def predict_fraud(
        transaction: TransactionInput,
        model_loader: ModelLoader = Depends (get_model_loader)):
    
    """Deteta Fraude"""
    logger.info (f"Analise de transaçao : Amount={transaction.Amount}")

    try:
        # Extrair features como lista (ordem importa!)
        features = [
            transaction.Time,
            transaction.V1, transaction.V2, transaction.V3, transaction.V4, transaction.V5,
            transaction.V6, transaction.V7, transaction.V8, transaction.V9, transaction.V10,
            transaction.Amount
        ]
        
        # Fazer predição
        prediction, fraud_probability = model_loader.predict(features)
        
        # Determinar label e risk level
        prediction_label = "FRAUDULENTA" if prediction == 1 else "LEGÍTIMA"
        risk_level = get_risk_level(fraud_probability)
        
        logger.info(f"✅ Resultado: {prediction_label} (prob: {fraud_probability:.4f}, risco: {risk_level})")
        
        return FraudPredictionOutput(
            prediction=prediction,
            prediction_label=prediction_label,
            fraud_probability=fraud_probability,
            risk_level=risk_level,
            model_version="1.0.0"
        )
    
    except Exception as e:
        logger.error(f"❌ Erro na predição: {e}", exc_info=True)
        raise

