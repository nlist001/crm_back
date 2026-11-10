pip install uv
uv pip install -e .


source venv/bin/activate
uvicorn app.main:app --reload