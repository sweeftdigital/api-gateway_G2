# Makefile

.PHONY: help test coverage coverage-html

# Command to display available commands
help:
	@echo "Available commands:"
	@echo "  make test            - Run the tests without coverage"
	@echo "  make coverage        - Run the tests with coverage report in the terminal"
	@echo "  make coverage-html   - Run the tests with coverage report in HTML format"

# Command to just run the tests
test:
	docker compose run --rm api-gateway sh -c "pytest"

# Command to run tests with coverage report in the terminal
coverage:
	docker compose run --rm api-gateway sh -c 'pytest --cov=app --cov-report=term --cov-config=.coveragerc tests'

# Command to run tests with coverage report in HTML format
coverage-html:
	docker compose run --rm api-gateway sh -c 'pytest --cov=app --cov-report=html --cov-config=.coveragerc tests'
