FROM python:3.12-slim

ARG TARGETARCH
ARG TYPST_VERSION=0.15.1
ARG SUPERCRONIC_VERSION=0.2.33

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl git poppler-utils tzdata xz-utils fonts-liberation \
 && rm -rf /var/lib/apt/lists/*

RUN case "$TARGETARCH" in arm64) T=aarch64 ;; *) T=x86_64 ;; esac \
 && curl -fsSL "https://github.com/typst/typst/releases/download/v${TYPST_VERSION}/typst-${T}-unknown-linux-musl.tar.xz" \
    | tar -xJ -C /tmp \
 && mv /tmp/typst-*/typst /usr/local/bin/typst \
 && typst --version

RUN case "$TARGETARCH" in arm64) S=arm64 ;; *) S=amd64 ;; esac \
 && curl -fsSL -o /usr/local/bin/supercronic \
    "https://github.com/aptible/supercronic/releases/download/v${SUPERCRONIC_VERSION}/supercronic-linux-${S}" \
 && chmod +x /usr/local/bin/supercronic

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /usr/local/bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    TZ=America/New_York

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN uv sync --no-dev --extra dashboard

CMD ["supercronic", "/app/docker/crontab"]
