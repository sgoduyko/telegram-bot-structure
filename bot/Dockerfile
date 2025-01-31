FROM python:3.9-alpine as temp

WORKDIR /telegram_bot

RUN apk add --no-cache gcc
COPY ../requirements.txt requirements.txt
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install  --upgrade pip &&  \
    /opt/venv/bin/pip install  -r requirements.txt


# final
FROM python:3.9-alpine

WORKDIR /telegram_bot
ENV PYTHONPATH=/telegram_bot

COPY --from=temp /opt/venv /opt/venv

COPY bot /telegram_bot/bot
COPY db /telegram_bot/db
COPY redis_db /telegram_bot/redis_db

CMD ["/opt/venv/bin/python", "-u", "bot/main.py"]
