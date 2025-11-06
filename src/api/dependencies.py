


from src.models.model_loader import ModelLoader

_model_loader= ModelLoader()

def get_model_loader() -> ModelLoader:
    """ Retorna instancia do ModelLoader"""

    return _model_loader
