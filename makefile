# Cross-platform Makefile for local development & CI
# Automatically selects correct Python path

ifeq ($(OS),Windows_NT)
	PYTHON := .venv\Scripts\python.exe
	PIP := .venv\Scripts\pip.exe
	JUPYTER := .venv\Scripts\jupyter.exe
	RM := del /q
else
	PYTHON := .venv/bin/python
	PIP := .venv/bin/pip
	JUPYTER := .venv/bin/jupyter
	RM := rm -rf
endif

# Run unit tests
test:
	PYTHONPATH=. $(PYTHON) -m pytest tests/

# Full pipeline (setup + transform + fraud detection + visualization)
run: prepare init transform fraud visualize

# Create necessary output folders if missing
prepare:
	mkdir -p output output/suspicious_transfers artifacts
	
# Create virtual environment and install dependencies
init:
	test -d .venv || python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run ETL logic
transform:
	$(PYTHON) src/etl.py

# Apply fraud detection rules
fraud:
	$(PYTHON) scripts/fraud_detection.py

# Generate visualizations using most recent fake data
visualize:
	$(PYTHON) src/visualize.py artifacts/output.csv

# Execute final notebook and export HTML report
report:
	$(JUPYTER) nbconvert --to html --execute notebooks/final_report.ipynb --output artifacts/final_report.html

# Save frozen requirements to file
freeze:
	$(PIP) install pipreqs
	.venv/bin/pipreqs . --force

# Remove generated files
clean:
	$(RM) artifacts .pytest_cache __pycache__ */__pycache__ output

# Generate realistic fake transactions
fake:
	$(PYTHON) scripts/generate_fake_data.py

# Clean, reprocess, retest, replot
all: clean transform test visualize