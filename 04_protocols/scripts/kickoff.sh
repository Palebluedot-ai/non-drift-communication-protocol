#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE="$ROOT/04_protocols/state/lock_state.json"

if [[ ! -f "$STATE" ]]; then
  echo "lock_state.json not found: $STATE" >&2
  exit 1
fi

GLOBAL=$(python3 - "$STATE" <<'PY'
import json,sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    s=json.load(f)
print(s['global_goal'])
print(s['next_locked']['id'])
print(s['next_locked']['action'])
PY
)

GOAL=$(echo "$GLOBAL" | sed -n '1p')
NEXT_ID=$(echo "$GLOBAL" | sed -n '2p')
NEXT_ACTION=$(echo "$GLOBAL" | sed -n '3p')

cat <<EOF
Goal: $GOAL
In-Scope: <fill>
Out-of-Scope: <fill>
Next (Locked): $NEXT_ID - $NEXT_ACTION
To-Do List:
- P0:
- P1:
- P2:
Drift Check: OK (NO_DRIFT)

Unlock phrases:
- 确认解锁
- 确认切阶段

Two-step unlock:
1) fixed phrase
2) target Next-ID
EOF
