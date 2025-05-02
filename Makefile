.PHONY: build test lint clean run

build:
	@echo "Building project (Python no build needed)"

test:
	python -m pytest -v

lint:
	flake8 minesweeper.py

run:
	python minesweeper.py

clean:
	rm -rf __pycache__/ .pytest_cache/

docker-build:
	docker build -t minesweeper:latest .

docker-run: docker-build
	docker run -it minesweeper:latest
