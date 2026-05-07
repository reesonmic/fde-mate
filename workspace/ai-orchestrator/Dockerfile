# --- Builder stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# 使用国内 pip 镜像安装 poetry
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ poetry==1.8.0

COPY pyproject.toml poetry.lock* ./

# 配置 poetry 使用国内 PyPI 镜像并安装
RUN poetry config virtualenvs.create false && \
    poetry config installer.parallel false && \
    poetry config repositories.aliyun https://mirrors.aliyun.com/pypi/simple/ && \
    (poetry install --no-root --only=main --no-interaction --no-ansi --no-lock 2>/dev/null || \
     poetry install --no-root --only=main --no-interaction --no-ansi)

# --- Production image ---
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY app ./app

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1

EXPOSE 8090

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8090/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090", "--workers", "2"]
