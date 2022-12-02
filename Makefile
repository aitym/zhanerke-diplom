DOCKER_COMPOSE = docker-compose -f ./docker-compose.yml
DOCKER_COMPOSE_PYTHON_EXEC = ${DOCKER_COMPOSE} exec python3
THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY: help build recreate start stop up ps psa logs down app

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

build:
	${DOCKER_COMPOSE} build

recreate:
	make down build up

restart:
	make down up

start:
	${DOCKER_COMPOSE} start

stop:
	${DOCKER_COMPOSE} stop

up:
	${DOCKER_COMPOSE} up -d --remove-orphans

ps:
	${DOCKER_COMPOSE} ps

psa:
	${DOCKER_COMPOSE} ps -a

logs:
	${DOCKER_COMPOSE} logs -f

down:
	${DOCKER_COMPOSE} down -v --remove-orphans

app:
	${DOCKER_COMPOSE_PYTHON_EXEC} bash
