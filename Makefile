DOCKER_CMD=docker exec -it portalnoticias

build:
	docker-compose up -d

upgrade-pip:
	${DOCKER_CMD} pip install --upgrade pip

setup: upgrade-pip
	${DOCKER_CMD} pip install -r requirements-local.txt

flake8:
	${DOCKER_CMD} flake8 --exclude=venv,tests,migrations .

test:
	${DOCKER_CMD} pytest tests

bash:
	${DOCKER_CMD} sh

run:
	${DOCKER_CMD} python api/app.py

start: run

migrate-init:
	${DOCKER_CMD} python api/manager.py db init

migrate:
	${DOCKER_CMD} python api/manager.py db migrate

migrate-apply:
	${DOCKER_CMD} python api/manager.py db upgrade

downgrade:
	${DOCKER_CMD} python api/manager.py db downgrade -1

seed:
	${DOCKER_CMD} python api/manager.py seed

