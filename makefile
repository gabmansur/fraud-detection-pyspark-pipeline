# Makefile

# Shortcut list for local development.
#
#   make init        → Set up virtual env + install dependencies
#   make transform   → Run ETL pipeline (load + transform)
#   make fraud       → Run fraud detection rules
#   make visualize   → Run visualization script
#   make test        → Run unit tests
#   make freeze      → Export current dependencies to requirements.txt
#   make report      → Export executed notebook as HTML
#   make clean       → Delete all generated files and caches
#   make run         → Full pipeline (init + transform + fraud + visualize)
#   make all         → Clean + transform + test + visualize (no install)
#
# -----------------------------

# Use bash-friendly paths for WSL/Linux

# Run tests with correct PYTHONPATH
test:
	PYTHONPATH=. .venv/bin/python -m pytest tests/

# Full pipeline (setup + ETL + fraud detection + visualizations)
run: init transform fraud visualize

# Setup virtual environment and install dependencies
init:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

# Run the ETL script
transform:
	.venv/bin/python src/etl.py

# Run fraud detection logic
fraud:
	.venv/bin/python src/fraud_rules.py

# Generate visualizations
visualize:
	.venv/bin/python src/visualize.py

# Run and export final report notebook
report:
	.venv/bin/jupyter nbconvert --to html --execute notebooks/final_report.ipynb --output artifacts/final_report.html

# Export current dependencies
freeze:
	.venv/bin/pip freeze > requirements.txt

# Remove generated files and caches
clean:
	rm -rf artifacts .pytest_cache __pycache__ */__pycache__ output

# Clean + ETL + tests + visualization (no init)
all: clean transform test visualize