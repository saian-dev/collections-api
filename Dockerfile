FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

RUN addgroup --system nonroot \
 && adduser --system --ingroup nonroot nonroot

ENV UV_NO_DEV=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_TOOL_BIN_DIR=/usr/local/bin

WORKDIR /app


COPY pyproject.toml uv.lock /app/
RUN uv sync --locked --no-install-project

COPY . /app
RUN uv sync --locked


COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nonroot

ENV PYTHONPATH="${PYTHONPATH}:/app/src"
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uv", "run", "python", "src/main.py"]
