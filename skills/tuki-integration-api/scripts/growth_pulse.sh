#!/usr/bin/env bash
# Pulso de growth Tuki: snapshot + orders → resumen Markdown + JSON por corrida.
# Cron: docs/PULSO-GROWTH-CRON.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OUT_DIR="${GROWTH_PULSE_DIR:-$ROOT/data/pulses}"
STAMP="$(date -u +"%Y-%m-%dT%H-%M-%SZ")"

mkdir -p "$OUT_DIR"

snap_tmp="$(mktemp)"
ord_tmp="$(mktemp)"
cleanup() { rm -f "$snap_tmp" "$ord_tmp"; }
trap cleanup EXIT

bash "$SCRIPT_DIR/tuki_api.sh" snapshot 2>/dev/null >"$snap_tmp" || true
bash "$SCRIPT_DIR/tuki_api.sh" orders-summary 2>/dev/null >"$ord_tmp" || true

cp -f "$snap_tmp" "$OUT_DIR/snapshot-latest.json"
cp -f "$ord_tmp" "$OUT_DIR/orders-latest.json"
cp -f "$snap_tmp" "$OUT_DIR/snapshot-${STAMP}.json"
cp -f "$ord_tmp" "$OUT_DIR/orders-${STAMP}.json"

SUMMARY="$OUT_DIR/latest-growth-pulse.md"

if python3 "$SCRIPT_DIR/growth_pulse_summary.py" "$snap_tmp" "$ord_tmp" "$SUMMARY" "$STAMP" 2>/dev/null; then
  echo "Escrito: $SUMMARY"
  cat "$SUMMARY"
else
  echo "# Pulso de growth — error generando resumen" >"$SUMMARY"
  echo "Revisa $OUT_DIR/snapshot-latest.json y orders-latest.json" >>"$SUMMARY"
  cat "$SUMMARY"
  exit 1
fi
