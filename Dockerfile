FROM python:3.10.10

RUN useradd zap && mkdir /app && mkdir /app/db

# RUN python3.10 -m venv /app
WORKDIR /app

COPY --chown=zap requirements.txt .

RUN python3 -m pip install pip -U && python3 -m pip --no-cache-dir install -r requirements.txt
COPY --chown=zap . .
USER zap

EXPOSE 8080/tcp

ENTRYPOINT ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "60", "--log-level", "error"]
