#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "Goal:",
    "In-Scope:",
    "Out-of-Scope:",
    "Next (Locked):",
    "To-Do List:",
    "Drift Check:",
]

REASON = {
    "OK": "NO_DRIFT",
    "MISSING": "DRIFT_MISSING_TEMPLATE_FIELD",
    "NEXT": "DRIFT_NEXT_MUTATION_WITHOUT_UNLOCK",
    "GLOBAL": "DRIFT_GLOBAL_MUTATION",
    "TODO": "DRIFT_TODO_PROMOTED_AS_NEXT",
    "UNLOCK": "DRIFT_UNLOCK_PHRASE_INVALID",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def has_required_fields(text: str):
    missing = [x for x in REQUIRED_FIELDS if x not in text]
    return missing


def parse_next_id(text: str):
    m = re.search(r"NEXT-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}", text)
    return m.group(0) if m else None


def unlock_phrase_present(text: str, phrases):
    return any(p in text for p in phrases)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True, help="lock_state.json path")
    ap.add_argument("--draft", required=True, help="draft text file path")
    ap.add_argument("--target-next-id", default="", help="required when unlocking")
    args = ap.parse_args()

    state = load_json(args.state)
    draft = Path(args.draft).read_text(encoding="utf-8")

    missing = has_required_fields(draft)
    if missing:
        print(json.dumps({"ok": False, "code": REASON["MISSING"], "notes": f"missing: {missing}"}, ensure_ascii=False))
        return 2

    # Global immutability quick check
    if state["global_goal"] not in draft:
        print(json.dumps({"ok": False, "code": REASON["GLOBAL"], "notes": "global_goal mismatch"}, ensure_ascii=False))
        return 3

    current_next = state["next_locked"]["id"]
    draft_next = parse_next_id(draft)

    phrases = state["unlock"]["phrases"]
    unlock_used = unlock_phrase_present(draft, phrases)

    if draft_next and draft_next != current_next:
        if not unlock_used:
            print(json.dumps({"ok": False, "code": REASON["NEXT"], "notes": f"next changed {current_next} -> {draft_next} without unlock"}, ensure_ascii=False))
            return 4
        # two-step unlock requires explicit target-next-id
        if state["unlock"].get("two_step_required", True):
            if not args.target_next_id or args.target_next_id != draft_next:
                print(json.dumps({"ok": False, "code": REASON["UNLOCK"], "notes": "two-step unlock failed: target-next-id missing or mismatch"}, ensure_ascii=False))
                return 5

    # Prevent TODO auto-promotion wording
    if "To-Do" in draft and "auto-promote" in draft.lower():
        print(json.dumps({"ok": False, "code": REASON["TODO"], "notes": "todo promoted automatically"}, ensure_ascii=False))
        return 6

    print(json.dumps({"ok": True, "code": REASON["OK"], "notes": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
