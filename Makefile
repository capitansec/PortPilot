COMPOSE_FILE := docker-compose.yaml
DB_SERVICE := postgres
DDL_SCRIPT := ./Migrations/initial-migration.sql

.PHONY: build up migrate down develop

build:
	docker-compose -f $(COMPOSE_FILE) build

up:
	docker-compose -f $(COMPOSE_FILE) up -d

migrate:
	docker-compose run --rm initdb

down:
	docker-compose -f $(COMPOSE_FILE) down

develop:
	docker-compose -f $(COMPOSE_FILE) up -d rabbitmq elasticsearch postgres redis #pp-worker