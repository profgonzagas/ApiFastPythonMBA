"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import List

class MessageInput(BaseModel):
    """
    Schema para entrada de mensagem
    """
    text: str = Field(...,
                      min_length=1,
                      max_length=500,
                      description="Texto da mensagem"
                      )
    priority: int = Field(
        default=1,
        ge=1, #ge= greater equal
        le=5, #le= less equal
        description="Prioridade da mensagem (1-5)")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "text": "Esta é uma mensagem de teste.",
                "priority": 3
            }
        }

class MessageOutput(BaseModel):
    """
    Schema para saída de mensagem
    """
    original_text: str
    processed_text: str
    char_count: int
    word_count: int
    priority_label: str


class PredictionInput(BaseModel):
    """
    Schema de entrada para predição do modelo ML
    """
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Lista com exatamente 4 features numéricas"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }

class PredictionOutput(BaseModel):
    """
    Schema de saída da predição
    """
    prediction: int = Field(..., description="Classe predita")
    probability: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Probabilidade da predição"
    )
    model_version: str = Field(..., description="Versão do modelo")