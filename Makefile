.PHONY: install dev fmt lint test test-py test-rs build run demo clean

PY ?= python3

install:
	$(PY) -m pip install -e '.[dev]'

dev: install
	pre-commit install || true

fmt:
	ruff check --fix src tests
	cd ingest-rs && cargo fmt

lint:
	ruff check src tests
	cd ingest-rs && cargo fmt --all -- --check
	cd ingest-rs && cargo clippy --all-targets -- -D warnings

test: test-py test-rs

test-py:
	pytest -q

test-rs:
	cd ingest-rs && cargo test --all-features

build:
	$(PY) -m build
	cd ingest-rs && cargo build --release

run:
	hikara scan

demo:
	hikara demo investigate

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache htmlcov coverage.xml
	cd ingest-rs && cargo clean
