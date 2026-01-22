FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

COPY . /app

WORKDIR /app/backend

EXPOSE 8000

RUN cd /app/backend && \
    chmod +x ./run.sh

CMD ["bash", "/app/backend/run.sh"]


