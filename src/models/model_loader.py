

import pickle
import logging
from pathlib import Path
from typing import Any,Tuple
import numpy as np 

logger = logging.getLogger(__name__)


class ModelLoader:
    """Carregador Singleton de modelos ML
     Garante que o modelo seja carregado apenas uma vez
    """
    _instance = None
    _model = None
    _model_path = None

    def __new__(cls):
        """Implementa padrão Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_model(self, model_path: Path) -> Any:
        '''Carrega o modelo ML do caminho especificado
        Args: model_path: Caminho pro arquivo .pkl
        return : Modelo Carregado
        '''

        if self._model is None:
            logger.info(f"Carregando modelo de {model_path}")

            if not model_path.exists():
                raise FileNotFoundError(f"Modelo não encontrado em {model_path}")
            
            with open(model_path,'rb' ) as f:
                self._model= pickle.load(f)

            self._model_path= model_path
            logger.info("Modelo carregado com sucesso")
        else:
            logger.info("Modelo já estava carregado, reutilizando")
        
        return self._model
    
    def predict(self,features: list[float])-> Tuple [int,float]:
        """Realizar a predição de fraude
        Args: features: lista de 12 valores float (Time, V1-V10, Amount)
        Returns : 
            Tupla (predição, probabilidade_fraude)
            -predição 0 (LEGITIMA) ou 1 (FRAUDULENTA)
            -probalidade_fraude: float entre 0 e 1
            """
        if self._model is None:
            raise RuntimeError("Modelo nao carregado, chame load_model() primeiro")
        
        #converter para formato numpy
        X= np.array([features])

        # Predição
        prediction = self._model.predict(X)[0]


        #probabilidade da classe FRAUDE (classe 1)
        probabilities = self._model.predict_proba(X)[0]
        fraud_probability = float(probabilities[1])  # Probabilidade de fraude

        logger.info(f"Predição: {prediction} ({'FRAUDULENTA' if prediction == 1 else 'LEGÍTIMA'}), Prob. Fraude: {fraud_probability:.4f}")
        return int(prediction), fraud_probability
    
    def get_model_info(self)-> dict:
        """retorna informações do modelo carregado"""
        if self._model is None:
            return{"loaded": False}            
            
        return {"loaded":True,
            "model_type": type(self._model).__name__,
            "model_path": str(self._model_path)}

