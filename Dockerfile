# Thalos Prime v1.0 - Docker Container
# Multi-stage build for optimized image size

# Build stage
FROM python:3.12-slim as builder

WORKDIR /build

# Copy source files
COPY src/ ./src/
COPY tests/ ./tests/
COPY config/ ./config/
COPY create_thalos_bootstrap.sh ./

# Verify build
RUN python -m py_compile src/**/*.py && \
    chmod +x create_thalos_bootstrap.sh

# Production stage
FROM python:3.12-slim

LABEL maintainer="Thalos Prime Team"
LABEL version="1.0"
LABEL description="Thalos Prime - Deterministic System Framework"

WORKDIR /app

# Copy from builder
COPY --from=builder /build/src ./src
COPY --from=builder /build/config ./config
COPY --from=builder /build/create_thalos_bootstrap.sh ./

# Create directories
RUN mkdir -p /app/docs /app/tests

# Set Python path
ENV PYTHONPATH=/app/src

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.path.insert(0, '/app/src'); from core.cis import CIS; cis = CIS(); cis.boot(); status = cis.status(); sys.exit(0 if status['status'] == 'operational' else 1)"

# Default command
CMD ["python", "src/main.py", "--help"]

# Expose potential API port (for future web interface)
EXPOSE 8000

# Volume for persistence (optional)
VOLUME ["/app/data"]
