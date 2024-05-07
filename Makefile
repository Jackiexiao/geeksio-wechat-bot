init_db:
	python -m src.models
dev:
	uvicorn src.main:app --reload --port 8012 --host 0.0.0.0

prd:
	uvicorn src.main:app --port 8012 --host 0.0.0.0

client:
	python client.py