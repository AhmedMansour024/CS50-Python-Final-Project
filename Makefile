# Variables
ENV_NAME = project		# environment folder name if you want to change it
PYTHON = python

# Define default task
.PHONY: all
all: install

# Create virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv $(ENV_NAME)

# Install dependencies and upgrade pip using python -m pip
.PHONY: install
install: venv
	$(ENV_NAME)\Scripts\python -m pip install --upgrade pip
	$(ENV_NAME)\Scripts\python -m pip install -r requirements.txt

# Run the Python project using the environment
.PHONY: run
run:
	$(ENV_NAME)\Scripts\python main.py

# Clean up the environment
.PHONY: clean
clean:
	rm -rf $(ENV_NAME)
