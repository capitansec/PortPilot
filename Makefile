COMPOSE_FILE := docker-compose.dev.yaml
DB_SERVICE := postgres
DB_NAME := your_database_name
DDL_SCRIPT := path/to/your/ddl_script.sql

.PHONY: build up migrate

build:
	docker-compose -f $(COMPOSE_FILE) build

up:
	docker-compose -f $(COMPOSE_FILE) up -d

migrate:
	docker-compose run --rm initdb