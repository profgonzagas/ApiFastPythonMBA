from pydantic import BaseModel, Field
from typing import List

class CalculatorInput(BaseModel):
    """ Entrada de operações matemáticas"""
    numero1: float=Field(..., description="Primeiro número")
    numero2: float=Field(..., description="Segundo número")
    operacao: str=Field(..., description="Operação matemática: +,-,*,/")

    class Config:
        json_schema_extra={
            "example":{
                "numero1": 10.5,
                "numero2": 2.0,
                "operacao": "+"
            }
        }

class CalculatorOutput(BaseModel):
    """ Saída de operações matemáticas"""
    resultado: float
    operacao:str
    expressao:str

class TransactionInput(BaseModel):
     """
    Entrada para detecção de fraude em transações
    """
     Time: float = Field(..., ge=0, description="Segundos desde primeira transação do dia")
     V1: float = Field(..., description="Componente principal 1")
     V2: float = Field(..., description="Componente principal 2")
     V3: float = Field(..., description="Componente principal 3")
     V4: float = Field(..., description="Componente principal 4")
     V5: float = Field(..., description="Componente principal 5")
     V6: float = Field(..., description="Componente principal 6")
     V7: float = Field(..., description="Componente principal 7")
     V8: float = Field(..., description="Componente principal 8")
     V9: float = Field(..., description="Componente principal 9")
     V10: float = Field(..., description="Componente principal 10")
     Amount: float = Field(..., ge=0, description="Valor da transação (R$)")

     class Config:
        json_schema_extra = {
            "example": {
                "Time": 50013.74,
                "V1": -2.58,
                "V2": 0.26,
                "V3": -0.23,
                "V4": -0.25,
                "V5": -2.35,
                "V6": -1.63,
                "V7": -0.10,
                "V8": 1.67,
                "V9": -0.89,
                "V10": -0.60,
                "Amount": 64.26
            }
        }
class FraudPredictionOutput(BaseModel):
       """Resultado da análise de fraude"""
       prediction: int = Field(..., description="0=LEGÍTIMA, 1=FRAUDULENTA")
       prediction_label: str = Field(..., description="Label em português")
       fraud_probability: float = Field(..., ge=0, le=1, description="Probabilidade de fraude (0-1)")
       risk_level: str = Field(..., description="BAIXO, MÉDIO ou ALTO")
       model_version: str = "1.0.0"