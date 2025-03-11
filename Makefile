# Variables
PYTHON=python3
SCRIPTS_DIR=$(shell pwd)

# Colors for better output
GREEN=\033[0;32m
NC=\033[0m # No Color

.PHONY: help
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: organize-download
organize-download: ## Organize all files in the Download dir and clear the root dir
	$(PYTHON) organize-download/main.py $(ARGS)

.PHONY: check-env
check-env: ## Check if all required packages are installed
	@echo "${GREEN}Checking environment...${NC}"
	$(PYTHON) -c "import sys; import pkg_resources; pkg_resources.require(open('requirements.txt').readlines())"

.PHONY: install-deps
install-deps: ## Install required dependencies
	@echo "${GREEN}Installing dependencies...${NC}"
	pip install -r requirements.txt