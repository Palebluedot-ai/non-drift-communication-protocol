# Global / In-Scope Lock Protocol v1

## Purpose
Turn anti-drift communication from habit into enforceable protocol.

## Core Rules
1. **Global is immutable** unless explicitly redefined.
2. **Next (Locked) is immutable** unless explicit unlock + phase switch succeeds.
3. Clarification questions **do not** imply approval to switch Next.
4. To-Do items are backlog only; **never auto-promote** to Next.

## Required Reply Frame (fixed order)
1. Goal
2. In-Scope
3. Out-of-Scope
4. Next (Locked)
5. To-Do List (P0/P1/P2)
6. Drift Check (reason code + notes)

## Unlock Policy (fixed phrases only)
Allowed phrases:
- `确认解锁`
- `确认切阶段`

Two-step unlock:
1. Valid phrase appears.
2. Target Next-ID provided and validated.

Without both steps, switch is rejected.

## Drift Policy
Fail-closed blocking (A+B):
- Block before final generation/publish when drift detected.

## North Star Metric
Primary KPI: **Lock-in Reply Rate (Definition B)**
- Numerator: replies that keep the same Next while unlocked phrase not present.
- Denominator: all replies where unlock phrase is absent.

## Reason Codes (MVP)
- DRIFT_GLOBAL_MUTATION
- DRIFT_NEXT_MUTATION_WITHOUT_UNLOCK
- DRIFT_SCOPE_VIOLATION
- DRIFT_MISSING_TEMPLATE_FIELD
- DRIFT_TODO_PROMOTED_AS_NEXT
- DRIFT_UNLOCK_PHRASE_INVALID
- DRIFT_UNLOCK_ACTOR_INVALID
- DRIFT_CHANNEL_STATE_MISMATCH
