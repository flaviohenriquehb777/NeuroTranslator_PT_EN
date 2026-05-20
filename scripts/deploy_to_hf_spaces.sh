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
cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

if command -v curl >/dev/null 2>&1; then
  WHOAMI_JSON="$(curl -fsSL -H "Authorization: Bearer ${HF_TOKEN}" "https://huggingface.co/api/whoami-v2" || true)"
  if [[ -z "${WHOAMI_JSON}" ]]; then
    echo "HF_TOKEN inválido (whoami falhou). Gere um novo token com permissões Write em https://huggingface.co/settings/tokens e atualize o secret HF_TOKEN no GitHub."
    exit 1
  fi
  TOKEN_USER="$(WHOAMI_JSON="${WHOAMI_JSON}" python3 - <<'PY'
import json, os, sys
try:
    data=json.loads(os.environ["WHOAMI_JSON"])
    print((data.get("name") or data.get("user") or "").strip())
except Exception:
    print("")
PY
)"
  if [[ -n "${TOKEN_USER}" && "${TOKEN_USER}" != "${HF_USER}" ]]; then
    echo "Aviso: o HF_TOKEN parece pertencer a '${TOKEN_USER}', mas o Space alvo é '${HF_USER}'. Gere o token no usuário dono do Space e atualize o secret."
  fi
fi

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
if ! git push "https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/${HF_SPACE}" main; then
  echo "Falha ao fazer push no Space. Causas mais comuns:"
  echo "1) HF_TOKEN sem permissão Write/Admin"
  echo "2) HF_TOKEN de outro usuário (não é o owner do Space)"
  echo "3) Space errado ou você não é colaborador dele"
  echo "Ajuste o token em https://huggingface.co/settings/tokens e atualize o secret HF_TOKEN no GitHub."
  exit 1
fi
cd - >/dev/null
