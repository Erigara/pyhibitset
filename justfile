# Use with https://github.com/casey/just

# Show available recipes
default:
    @just --list

# Create the virtualenv
venv:
    python3 -m venv venv

# Compile extension and install into the venv
build-dev:
    pip install .

# Install dependencies for tests
install-dev-dependencies:
    #!/usr/bin/env bash
    # Activate venv to install dependencies into venv
    . venv/bin/activate
    pip install pip-tools
    pip-sync requirements/requirements-dev.txt

# Combine venv and install-dev-dependencies recipes
setup: venv install-dev-dependencies

# Run tests
test:
    -flake8 tests/
    -black --check tests/
    -pytest tests/