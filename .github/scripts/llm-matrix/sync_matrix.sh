#!/usr/bin/env bash

set -euo pipefail

# Downloads generated LLM performance matrix CSVs from the GCS bucket populated by
# the Kibana `kibana-evals-security-matrix` Buildkite pipeline and copies them into
# the docs source tree.
#
# Required env:
#   MATRIX_GCS_BUCKET   GCS bucket name (no gs:// prefix).
# Optional env:
#   MATRIX_DOMAIN       Source prefix domain (default: security).
#   MATRIX_PREFIX       'latest' (serverless/weekly) or a Stack version (default: latest).
#   DEST_DIR            Destination directory for the CSVs.

BUCKET_NAME="${MATRIX_GCS_BUCKET:?MATRIX_GCS_BUCKET is required}"
MATRIX_DOMAIN="${MATRIX_DOMAIN:-security}"
MATRIX_PREFIX="${MATRIX_PREFIX:-latest}"
DEST_DIR="${DEST_DIR:-solutions/security/ai/agent-builder-llm-performance-matrix}"

SRC="gs://${BUCKET_NAME}/${MATRIX_DOMAIN}/${MATRIX_PREFIX}"

mkdir -p "$DEST_DIR"

for f in proprietary-models.csv open-source-models.csv; do
  echo "Downloading ${SRC}/${f} -> ${DEST_DIR}/${f}"
  gsutil cp "${SRC}/${f}" "${DEST_DIR}/${f}"
  echo "OUTPUT_CSV_PATH=${DEST_DIR}/${f}"
done

echo "Synced LLM matrix CSVs from ${SRC} into ${DEST_DIR}"
