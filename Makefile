# Set up an environment
.PHONEY: setup
setup: setup-python setup-pre-commit

.PHONE: setup-python
setup-python:
	uv run bash ./dev/setup.sh --deps "development"

.PHONE: setup-pre-commit
setup-pre-commit:
	uv run pre-commit install

# Build the package
build:
	uv run bash ./dev/build.sh

# Check all the coding style.
.PHONY: lint
lint:
	uv run pre-commit run --all-files

# Run the unit tests.
.PHONEY: test
test:
	uv run bash ./dev/test_python.sh

test-with-api:
	LIGHTDASH_API_KEY="..." LIGHTDASH_URL="..." bash ./dev/test_python.sh

.PHONEY: update-resources
update-resources:
	uv run bash ./dev/update_resources.sh
