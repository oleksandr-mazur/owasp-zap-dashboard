FROM python:3.10.10

RUN mkdir /app
WORKDIR /app
ADD requirements.txt .
RUN python -m pip install pip -U && python -m pip --no-cache-dir install -r requirements.txt
RUN useradd -m zap && chown -R zap:zap /app
COPY . .
USER zap

EXPOSE 8080/tcp

ENTRYPOINT ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--timeout", "60"]
