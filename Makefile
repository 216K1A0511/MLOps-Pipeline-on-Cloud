# Gemini MLOps Pipeline Makefile

.PHONY: help setup install test train deploy run monitor clean

help:
	@echo "Gemini MLOps Pipeline Commands:"
	@echo "  make setup       - Initial project setup"
	@echo "  make install     - Install dependencies"
	@echo "  make test        - Run tests"
	@echo "  make train       - Run training pipeline"
	@echo "  make deploy      - Deploy API server"
	@echo "  make run         - Run complete pipeline"
	@echo "  make monitor     - Start monitoring"
	@echo "  make clean       - Clean generated files"

setup:
	@echo "Setting up Gemini MLOps Pipeline..."
	@mkdir -p data/{raw,processed,generated}
	@mkdir -p models/{registry,deployed}
	@mkdir -p logs reports
	@cp configs/gemini_config.example.yaml configs/gemini_config.yaml
	@echo "Please update configs/gemini_config.yaml with your Gemini API key"
	@echo "Setup complete!"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src

train:
	@read -p "Enter data path (or press enter for synthetic data): " data_path; \
	python -m src.pipeline.pipeline \
		--task-type classification \
		--data-path "$${data_path:-}" \
		--run-id "train_$$(date +%Y%m%d_%H%M%S)"

deploy:
	docker-compose up -d mlops-api
	@echo "API server running at http://localhost:8081"
	@echo "Health check: http://localhost:8081/health"

run:
	docker-compose up --build

monitor:
	python -m src.monitoring.performance_tracker --watch

clean:
	@echo "Cleaning generated files..."
	@rm -rf data/processed/* data/generated/*
	@rm -rf logs/* reports/*
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@echo "Clean complete!"

# Generate synthetic data
generate-data:
	python -c "
from src.training.gemini_finetuner import GeminiFinetuner
import os
gemini = GeminiFinetuner(api_key=os.getenv('GEMINI_API_KEY'))
schema = {
    'feature1': {'type': 'float', 'min': 0, 'max': 1},
    'feature2': {'type': 'integer', 'min': 0, 'max': 100},
    'feature3': {'type': 'categorical', 'categories': ['A', 'B', 'C']},
    'label': {'type': 'categorical', 'categories': ['Positive', 'Negative']}
}
df = gemini.generate_synthetic_data(schema, 1000)
df.to_csv('data/generated/synthetic_data.csv', index=False)
print('Generated 1000 synthetic samples')
"

# Quick test
quick-test:
	@echo "Running quick pipeline test..."
	@export GEMINI_API_KEY=$$(grep api_key configs/gemini_config.yaml | cut -d' ' -f2); \
	python -m src.pipeline.pipeline --task-type classification --run-id quick_test