FLIT_VERSION := 3.7.1


# Set up an environment
.PHONEY: setup
setup: setup-python setup-pre-commit

.PHONE: setup-python
setup-python:
	bash ./dev/setup.sh --flit-version "$(FLIT_VERSION)" --flit-deps "all"
	# typer-cli doesn't work with newer typer version because of the version constraints
	# And we can't add dependencies to GitHub repositories in pyproject.toml.
	# So we need to install it independently.
	# https://github.com/tiangolo/typer-cli/pull/120
	pip install -U "git+https://github.com/Patarimi/typer-cli"

.PHONE: setup-pre-commit
setup-pre-commit:
	pre-commit install

# Build the package
build:
	flit build

# Check all the coding style.
.PHONY: lint
lint:
	pre-commit run --all-files
	bash dev/lint_python.sh

# Run the unit tests.
.PHONEY: test
test:
	bash ./dev/test_python.sh

.PHONEY: update-resources
update-resources:
	bash ./dev/update_resources.sh
