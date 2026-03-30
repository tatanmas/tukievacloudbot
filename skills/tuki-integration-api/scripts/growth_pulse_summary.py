#!/usr/bin/env python3
"""Lee snapshot + orders JSON y escribe Markdown de pulso. Sin dependencias extra."""
import json
import sys
from pathlib import Path


def fmt_val(v):
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def main():
    if len(sys.argv) < 4:
        print(
            "Uso: growth_pulse_summary.py <snapshot.json> <orders.json> <out.md> [stamp_utc]",
            file=sys.stderr,
        )
        sys.exit(1)
    snap_path, ord_path, out_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    stamp = sys.argv[4] if len(sys.argv) > 4 else ""

    s = json.loads(snap_path.read_text(encoding="utf-8"))
    o = json.loads(ord_path.read_text(encoding="utf-8"))

    lines = [
        "# Pulso de growth — Tuki",
        f"**Generado (UTC):** {stamp}",
        "",
        "## Plataforma",
    ]
    plat = s.get("platform") or {}
    if plat:
        lines.append(f"- Deploy: {plat.get('deployed_at', 'n/d')}")
        lines.append(f"- Uptime: {plat.get('uptime_display', 'n/d')}")
        lines.append(
            f"- DB / Redis: {plat.get('database_ok')} / {plat.get('redis_ok')}"
        )
    else:
        lines.append("- (sin platform)")
    lines += ["", "## Inventario (counts)"]
    counts = s.get("counts") or {}
    if counts:
        for k, v in sorted(counts.items()):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- (sin counts)")
    lines += ["", "## Actividad hoy (proxy)"]
    act = s.get("activity_today") or {}
    if act:
        for k, v in sorted(act.items()):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- (sin activity_today)")
    lines += ["", "## Órdenes (no sandbox)"]
    ond = o.get("orders_non_sandbox_not_deleted") or {}
    if ond:
        for k, v in sorted((ond.get("by_status") or {}).items()):
            lines.append(f"- {k}: {v}")
        lines.append(f"- Total: {ond.get('total', 0)}")
    else:
        lines.append("- (sin datos)")
    lines += ["", "## Revenue elegible"]
    rev = o.get("revenue_eligible") or {}
    if rev:
        for k, v in sorted(rev.items()):
            lines.append(f"- {k}: {fmt_val(v)}")
    else:
        lines.append("- (sin datos)")
    lines += [
        "",
        "---",
        "*JSON: `data/pulses/snapshot-latest.json`, `orders-latest.json`*",
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
