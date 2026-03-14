FROM node:20-bookworm-slim AS client-build
WORKDIR /client
COPY client/package.json client/package-lock.json* ./
RUN npm ci
COPY client/ ./
RUN npm run build

FROM python:3.12-slim AS api-build
WORKDIR /wheels
RUN python -m pip install --upgrade pip wheel
COPY api/requirements.txt /tmp/requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r /tmp/requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY --from=api-build /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY api/ /app/api/
COPY --from=client-build /client/dist /app/api/static/client

WORKDIR /app/api

EXPOSE 8000
CMD ["gunicorn", "-c", "gunicorn_conf.py", "ecoroute_api.wsgi:application"]
