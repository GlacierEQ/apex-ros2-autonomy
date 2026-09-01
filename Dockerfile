# Stage 1: Build & Setup
FROM ros:humble as base
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pytest \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/apex_autonomy
COPY src/ ./src/
COPY tests/ ./tests/
COPY config/ ./config/
COPY launch/ ./launch/
COPY simulation/ ./simulation/

# Stage 2: Test Runner
FROM base as test-runner
ENV PYTHONPATH=/opt/apex_autonomy/src
CMD ["pytest", "tests/", "-v"]
