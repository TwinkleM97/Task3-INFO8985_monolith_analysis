#!/bin/bash

echo "Setting OpenTelemetry environment variables..."
export OTEL_LOGS_EXPORTER=none
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf  # Force HTTP instead of gRPC
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export FLASK_APP=app.py

echo "Starting Flask app with OpenTelemetry instrumentation..."
opentelemetry-instrument \
  --logs_exporter otlp \
  --metrics_exporter otlp \
  --traces_exporter otlp \
  --service_name monolith-analysis \
 python -m flask run -p 5000

