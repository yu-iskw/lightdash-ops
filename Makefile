FLIT_VERSION := 3.7.1


# Set up an environment
.PHONEY: setup
setup: setup-python setup-pre-commit

.PHONE: setup-python
setup-python:
	bash ./dev/setup.sh --flit-version $(FLIT_VERSION)

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
