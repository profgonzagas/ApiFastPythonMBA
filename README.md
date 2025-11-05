# ML Model API (FastAPI)

Small FastAPI application exposing an ASGI `app` in `src/api/main.py`.

How to run (Windows, PowerShell):

1. Activate the virtual environment:

```powershell
.\\venv\\Scripts\\Activate
```

2. Install dependencies (if needed):

```powershell
python -m pip install -r requirements.txt
```

3. Run the app with Uvicorn:

```powershell
uvicorn src.api.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.
