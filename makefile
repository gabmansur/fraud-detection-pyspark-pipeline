# Makefile

# This is like a list of shortcuts.
# Instead of typing long commands, just do:
#
#   make init        → setup .venv and install dependencies
#   make transform   → run the ETL pipeline (loads + transforms data)
#   make test        → run tests using pytest
#   make freeze      → save current packages to requirements.txt
#   make clean       → delete .pytest_cache and output files
#   make all         → clean + transform + test (full pipeline run)
#
# Use Git Bash to run these if you're on Windows.
# Example: right-click → Git Bash Here → type `make transform`
#
# -----------------------------

# Create a venv if needed
init:
	python -m venv .venv
	.venv\Scripts\activate && pip install -r requirements.txt

# Run transformation script
transform:
	.venv\Scripts\activate && python src/etl.py

# Run tests with pytest
test:
	.venv\Scripts\activate && pytest tests/

# Freeze dependencies
freeze:
	.venv\Scripts\activate && pip freeze > requirements.txt

# Clean artifacts
clean:
	rd /s /q artifacts || true
	rd /s /q .pytest_cache || true

# Re-run everything clean
all: clean transform test
