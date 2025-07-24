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

# Run unit tests
test:
	PYTHONPATH=. $(PYTHON) -m pytest tests/

# Full pipeline
run: prepare init fake transform fraud visualize

# Create necessary folders
prepare:
	$(MKDIR) output && $(MKDIR) output/suspicious_transfers && $(MKDIR) artifacts

# Create virtual environment and install requirements
init:
	test -d .venv || python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Generate fake transaction data
fake:
	$(PYTHON) scripts/generate_fake_data.py

# Run ETL logic
transform:
	$(PYTHON) src/etl.py

# Apply fraud detection rules
fraud:
	$(PYTHON) scripts/fraud_detection.py

# Visualize results
visualize:
	$(PYTHON) src/visualize.py artifacts/output.csv

# Generate notebook report
report:
	$(JUPYTER) nbconvert --to html --execute notebooks/final_report.ipynb --output artifacts/final_report.html

notebook:
	.venv/bin/python scripts/generate_notebook.py

# Freeze dependencies
freeze:
	$(PIP) install pipreqs
	$(PYTHON) -m pipreqs . --force

# Clean artifacts and outputs
clean:
	$(RM) artifacts .pytest_cache __pycache__ */__pycache__ output

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'


# All-in-one
all: clean run test report
