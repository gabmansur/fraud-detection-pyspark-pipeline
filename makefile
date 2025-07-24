# Cross-platform Makefile for local development & CI
# Automatically selects correct Python path

ifeq ($(OS),Windows_NT)
	PYTHON := .venv\Scripts\python.exe
	PIP := .venv\Scripts\pip.exe
	JUPYTER := .venv\Scripts\jupyter.exe
	MKDIR := if not exist
	RM := rmdir /s /q
else
	PYTHON := .venv/bin/python
	PIP := .venv/bin/pip
	JUPYTER := .venv/bin/jupyter
	MKDIR := mkdir -p
	RM := rm -rf
endif

help:  ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

init:  ## Create virtual environment & install dependencies
	test -d .venv || python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

fake:  ## Generate fake transaction data
	$(PYTHON) scripts/generate_fake_data.py

transform:  ## Run ETL pipeline
	$(PYTHON) src/etl.py

fraud:  ## Apply fraud detection rules
	$(PYTHON) scripts/fraud_detection.py

visualize:  ## Generate transaction distribution plots
	$(PYTHON) src/visualize.py artifacts/output.csv

report:  ## Generate HTML report from notebook
	$(JUPYTER) nbconvert --to html --execute notebooks/final_report.ipynb --output artifacts/final_report.html

notebook:  ## (Optional) Generate notebook dynamically
	.venv/bin/python scripts/generate_notebook.py

test:  ## Run unit tests with Pytest
	PYTHONPATH=. $(PYTHON) -m pytest tests/

freeze:  ## Freeze current environment into requirements.txt
	$(PIP) install pipreqs
	$(PYTHON) -m pipreqs . --force

clean:  ## Remove artifacts, output, and caches
	$(RM) artifacts .pytest_cache __pycache__ */__pycache__ output

prepare:  ## Create necessary folders
	$(MKDIR) output && $(MKDIR) output/suspicious_transfers && $(MKDIR) artifacts

run:  ## Run full pipeline (prepare + init + fake + transform + fraud + visualize)
	make prepare init fake transform fraud visualize

all:  ## Clean, run full pipeline, test, and generate report
	make clean run test report
