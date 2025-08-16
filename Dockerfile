# multi-stage: build into a virtualenv, then use a small python runtime
FROM python:3.11-slim AS builder
WORKDIR /build

# create venv and use it for installs
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# install build dependencies, then app requirements and also adds curl for testing the vulnerability
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc curl \
 && python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get remove -y build-essential gcc \
 && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# copy app source
WORKDIR /build/app
COPY . /build/app

# ---- Runtime ----
FROM python:3.11-slim AS runtime
# copy venv and app from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/app /app

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 8000

# use uvicorn from the venv entrypoint (no explicit "python -m")
CMD ["uvicorn", "app.chatbot:app", "--host", "0.0.0.0", "--port", "8000"]