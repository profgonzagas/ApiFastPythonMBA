from pathlib import Path

#Diretorios
BASE_DIR = Path(__file__).parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DATA_DIR = ARTIFACTS_DIR / "data"
MODEL_DIR = ARTIFACTS_DIR / "model"
LOGS_DIR = BASE_DIR / "logs"

# API
API_TITLE = "ML Model API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para servir modelo de Machine Learning"

# Modelo
MODEL_PATH = MODEL_DIR / "model.pkl"
MODEL_VERSION = "1.0.0"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"