#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN não definido"
  exit 1
fi

HF_SPACE="${HF_SPACE:-Flaviohb7/neurotranslator-api}"
HF_USER="${HF_USER:-${HF_SPACE%%/*}}"
VERSION="${VERSION:-dev}"

TMP_DIR="$(mktemp -d)"
git clone "https://huggingface.co/spaces/${HF_SPACE}" "${TMP_DIR}"

find "${TMP_DIR}" -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf {} +

cp -r "src/api/." "${TMP_DIR}/"
if [[ -f "docs/metrics.json" ]]; then
  mkdir -p "${TMP_DIR}/docs"
  cp "docs/metrics.json" "${TMP_DIR}/docs/metrics.json"
fi
if [[ -f "docs/metrics_badge.svg" ]]; then
  mkdir -p "${TMP_DIR}/docs"
  cp "docs/metrics_badge.svg" "${TMP_DIR}/docs/metrics_badge.svg"
fi

cd "${TMP_DIR}"
git config user.email "flaviohenriquehb777@outlook.com"
git config user.name "Flávio Henrique"
git add .
git commit -m "Deploy v${VERSION} - $(date '+%Y-%m-%d %H:%M')" || true
git push "https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/${HF_SPACE}" main
cd - >/dev/null

rm -rf "${TMP_DIR}"
