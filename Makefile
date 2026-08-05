.PHONY: setup dev build test test-unit test-integration clean lint

setup:
	python -m venv venv
	./venv/Scripts/pip install -e packages/schemas -e packages/database -e packages/model-clients -r services/api-gateway/requirements.txt pytest httpx
	cd apps/web && npm install
	cd apps/admin && npm install

dev:
	python -m uvicorn services.api_gateway.main:app --reload --port 8000

test:
	pytest tests/

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

build:
	cd apps/web && npm run build
	cd apps/admin && npm run build

clean:
	rm -rf __pycache__ .pytest_cache dist build *.egg-info
