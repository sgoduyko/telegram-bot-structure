BOT_CONTAINER_NAME = telegram-bot


migrations:
	docker exec -it $(BOT_CONTAINER_NAME) sh -c ". /opt/venv/bin/activate && cd /telegram_bot/db && alembic revision --autogenerate"

upgrade_migrations:
	docker exec -it $(BOT_CONTAINER_NAME) sh -c ". /opt/venv/bin/activate && cd /telegram_bot/db && alembic upgrade head"

downgrade_1_migration:
	docker exec -it $(BOT_CONTAINER_NAME) sh -c ". /opt/venv/bin/activate && cd /telegram_bot/db && alembic downgrade -1"

format_code_style:
	isort .
	black .
	# autoflake . --exclude "db/models"  # не получается настроить игнорирование db/models/__init__.py


format_code_typing:
	mypy  .
