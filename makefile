SERVICE_NAME=back-end
DOCKER_COMPOSE=docker-compose

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

build:
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d

ps:
	$(DOCKER_COMPOSE) ps

clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d

shell:
	docker exec -it brain-agriculture-backend bash

run-fastapi:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8007
