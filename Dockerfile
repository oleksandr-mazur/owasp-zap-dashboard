FROM python:3.10.10

# RUN mkdir /app && mkdir /app/db

# RUN groupadd --gid 2000 zap \
#   && useradd --uid 2000 --gid zap --shell /bin/bash --create-home zap \
#   && mkdir /app && chown -R zap:zap /app


RUN useradd zap && mkdir /app && mkdir /app/db


# RUN python3.10 -m venv /app
WORKDIR /app

COPY --chown=zap requirements.txt .

RUN python3 -m pip install pip -U && python3 -m pip --no-cache-dir install -r requirements.txt
COPY --chown=zap . .
USER zap

EXPOSE 8080/tcp

ENTRYPOINT ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "60"]
