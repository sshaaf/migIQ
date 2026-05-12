# Makefile for Project Tracker Agent
#
# Usage:
#   make help              - Show this help message
#   make setup             - Install dependencies
#   make test              - Run all tests (unit + integration)
#   make test-unit         - Run unit tests only
#   make test-integration  - Run integration tests (requires .env.test)
#   make test-integration-json - Run integration tests with JSON output
#   make env-setup         - Create .env.test from template
#   make clean             - Clean up Python cache files

.PHONY: help setup test test-unit test-integration test-integration-json env-setup clean lint

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

# Directories
TEST_DIR := tests
INTEGRATION_TEST_DIR := $(TEST_DIR)/integration
INTEGRATION_TEST_SCRIPT := $(INTEGRATION_TEST_DIR)/test_github_integration.py

# Environment files
ENV_TEST := .env.test
ENV_TEST_EXAMPLE := .env.test.example

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)Project Tracker Agent - Makefile Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  1. make setup          # Install dependencies"
	@echo "  2. make env-setup      # Create .env.test from template"
	@echo "  3. Edit .env.test with your GitHub credentials"
	@echo "  4. make test-integration  # Run integration tests"

setup: ## Install Python dependencies
	@echo "$(CYAN)Installing dependencies...$(NC)"
	$(PIP) install -r ../../requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

env-setup: ## Create .env.test from template
	@if [ -f "$(ENV_TEST)" ]; then \
		echo "$(YELLOW)⚠ .env.test already exists, skipping...$(NC)"; \
		echo "$(YELLOW)  Delete it first if you want to recreate from template$(NC)"; \
	else \
		if [ ! -f "$(ENV_TEST_EXAMPLE)" ]; then \
			echo "$(RED)✗ Error: .env.test.example not found$(NC)"; \
			exit 1; \
		fi; \
		cp $(ENV_TEST_EXAMPLE) $(ENV_TEST); \
		echo "$(GREEN)✓ Created .env.test from template$(NC)"; \
		echo "$(YELLOW)⚠ Remember to edit .env.test with your GitHub credentials:$(NC)"; \
		echo "  - TRACKER_GITHUB_TOKEN=ghp_your_token_here"; \
		echo "  - TRACKER_GITHUB_ORGANIZATION=your-org-or-username"; \
	fi

env-check: ## Check if .env.test exists and is configured
	@if [ ! -f "$(ENV_TEST)" ]; then \
		echo "$(RED)✗ Error: .env.test not found$(NC)"; \
		echo "$(YELLOW)Run 'make env-setup' to create it from template$(NC)"; \
		exit 1; \
	fi
	@if ! grep -q "^TRACKER_GITHUB_TOKEN=" $(ENV_TEST) || grep -q "^TRACKER_GITHUB_TOKEN=ghp_your_token_here" $(ENV_TEST); then \
		echo "$(YELLOW)⚠ Warning: TRACKER_GITHUB_TOKEN not configured in .env.test$(NC)"; \
		echo "$(YELLOW)  Please edit .env.test and set your GitHub token$(NC)"; \
		exit 1; \
	fi
	@if ! grep -q "^TRACKER_GITHUB_ORGANIZATION=" $(ENV_TEST) || grep -q "^TRACKER_GITHUB_ORGANIZATION=your-org-or-username" $(ENV_TEST); then \
		echo "$(YELLOW)⚠ Warning: TRACKER_GITHUB_ORGANIZATION not configured in .env.test$(NC)"; \
		echo "$(YELLOW)  Please edit .env.test and set your organization$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ .env.test is configured$(NC)"

test: test-unit test-integration ## Run all tests (unit + integration)

test-unit: ## Run unit tests
	@echo "$(CYAN)Running unit tests...$(NC)"
	@if command -v pytest >/dev/null 2>&1; then \
		$(PYTHON) -m pytest $(TEST_DIR) --ignore=$(INTEGRATION_TEST_DIR) -v; \
	else \
		echo "$(YELLOW)⚠ pytest not installed, running tests individually...$(NC)"; \
		for test_file in $(TEST_DIR)/test_*.py; do \
			echo "$(CYAN)Running $$test_file...$(NC)"; \
			$(PYTHON) -m py_compile $$test_file && echo "$(GREEN)✓ Syntax OK$(NC)" || exit 1; \
		done; \
	fi

test-integration: env-check ## Run integration tests with .env.test
	@echo "$(CYAN)Running integration tests...$(NC)"
	@echo "$(YELLOW)This will make real API calls to GitHub$(NC)"
	@$(PYTHON) $(INTEGRATION_TEST_SCRIPT)
	@if [ $$? -eq 0 ]; then \
		echo "$(GREEN)✓ Integration tests passed$(NC)"; \
	else \
		echo "$(RED)✗ Integration tests failed$(NC)"; \
		exit 1; \
	fi

test-integration-json: env-check ## Run integration tests with JSON output
	@echo "$(CYAN)Running integration tests (JSON output)...$(NC)"
	@$(PYTHON) $(INTEGRATION_TEST_SCRIPT) --json

test-integration-keep: env-check ## Run integration tests and keep test project
	@echo "$(CYAN)Running integration tests (keeping test project)...$(NC)"
	@echo "$(YELLOW)Test project will NOT be deleted after test$(NC)"
	@TEST_KEEP_PROJECT=true $(PYTHON) $(INTEGRATION_TEST_SCRIPT)

test-syntax: ## Check Python syntax for all files
	@echo "$(CYAN)Checking Python syntax...$(NC)"
	@find trackers -name "*.py" -exec $(PYTHON) -m py_compile {} \; && echo "$(GREEN)✓ All files have valid syntax$(NC)"
	@find $(TEST_DIR) -name "*.py" -exec $(PYTHON) -m py_compile {} \; && echo "$(GREEN)✓ All test files have valid syntax$(NC)"

lint: ## Run linting (if available)
	@echo "$(CYAN)Running linting...$(NC)"
	@if command -v pylint >/dev/null 2>&1; then \
		pylint trackers/ $(TEST_DIR)/; \
	elif command -v flake8 >/dev/null 2>&1; then \
		flake8 trackers/ $(TEST_DIR)/; \
	else \
		echo "$(YELLOW)⚠ No linter found (install pylint or flake8)$(NC)"; \
		echo "$(YELLOW)  Running syntax check instead...$(NC)"; \
		$(MAKE) test-syntax; \
	fi

clean: ## Clean up Python cache files
	@echo "$(CYAN)Cleaning up...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned up Python cache files$(NC)"

rate-limit: env-check ## Check GitHub API rate limit
	@echo "$(CYAN)Checking GitHub API rate limit...$(NC)"
	@. ./$(ENV_TEST) && \
		curl -s -H "Authorization: Bearer $$TRACKER_GITHUB_TOKEN" \
		https://api.github.com/rate_limit | \
		$(PYTHON) -m json.tool | \
		grep -A 4 "graphql" || echo "$(RED)✗ Failed to check rate limit$(NC)"

validate-token: env-check ## Validate GitHub token has required permissions
	@echo "$(CYAN)Validating GitHub token...$(NC)"
	@. ./$(ENV_TEST) && \
		response=$$(curl -s -H "Authorization: Bearer $$TRACKER_GITHUB_TOKEN" https://api.github.com/user); \
		echo "$$response" | $(PYTHON) -c 'import sys, json; data=json.load(sys.stdin); print("✓ Token valid for user:", data.get("login", "unknown"))' || \
		echo "$(RED)✗ Token validation failed$(NC)"
	@echo "$(YELLOW)Note: Check token scopes at https://github.com/settings/tokens$(NC)"
	@echo "$(YELLOW)Required scopes: repo, project$(NC)"

ci: ## Run tests in CI mode (for CI/CD pipelines)
	@echo "$(CYAN)Running CI test suite...$(NC)"
	$(MAKE) test-syntax
	@if [ -f "$(ENV_TEST)" ]; then \
		$(MAKE) test-integration; \
	else \
		echo "$(YELLOW)⚠ Skipping integration tests (.env.test not found)$(NC)"; \
	fi

install-dev: ## Install development dependencies
	@echo "$(CYAN)Installing development dependencies...$(NC)"
	$(PIP) install pytest pylint flake8 black mypy
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

format: ## Format code with black (if installed)
	@if command -v black >/dev/null 2>&1; then \
		echo "$(CYAN)Formatting code with black...$(NC)"; \
		black trackers/ $(TEST_DIR)/; \
		echo "$(GREEN)✓ Code formatted$(NC)"; \
	else \
		echo "$(YELLOW)⚠ black not installed$(NC)"; \
		echo "$(YELLOW)  Run 'make install-dev' to install development tools$(NC)"; \
	fi

watch: ## Watch for file changes and run tests (requires entr)
	@if command -v entr >/dev/null 2>&1; then \
		echo "$(CYAN)Watching for changes...$(NC)"; \
		find trackers $(TEST_DIR) -name "*.py" | entr -c $(MAKE) test-unit; \
	else \
		echo "$(RED)✗ entr not installed$(NC)"; \
		echo "$(YELLOW)  Install with: brew install entr (macOS) or apt-get install entr (Linux)$(NC)"; \
	fi

.PHONY: all
all: setup test ## Setup and run all tests
