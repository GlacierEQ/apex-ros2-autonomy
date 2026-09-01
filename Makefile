.PHONY: test lint docker-build docker-test

test:
	PYTHONPATH=src pytest tests/ -v

lint:
	python3 -m py_compile src/**/*.py

docker-build:
	docker build -t apex-ros2-autonomy:latest .

docker-test:
	docker run --rm apex-ros2-autonomy:latest
