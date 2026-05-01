# Boundary Confirmation v1 (Frozen)

Status: LOCKED
Owner: Bigchao

## Goal (Global)
把“沟通不漂移”产品化成强执行协议系统：在任意 Repo / Channel / Thread / 设备中，稳定保持主线，不因澄清对话改道；若偏航则自动阻断并拉回，且可审计、可复现。

## In-Scope（当前阶段）
1. 固化协议语义
   - Global 不可变（除非显式重定义）
   - Next 锁定，不可自动切换
   - 固定解锁口令
   - 双层解锁（口令 + Next-ID）
   - 漂移策略 fail-closed（A+B 阻断）
2. 固化输出契约
   - Goal / In-Scope / Out-of-Scope / Next(Locked) / To-Do(P0/P1/P2) / Drift Check(reason code + notes)
3. 固化评估北极星
   - 主指标：锁内回复率（口径 B：分母仅统计未出现解锁口令的回复）

## Out-of-Scope（当前明确不做）
- 非治理类业务功能开发
- 多人权限模型细化（当前仅 owner 解锁）
- 自然语言同义解锁
- 软提醒但不强执行方案

## Unlock Contract（Fixed）
Allowed phrases:
- 确认解锁
- 确认切阶段

Two-step required:
1) fixed phrase
2) target Next-ID

## Reply Contract（每轮必须）
每一轮回复末尾必须包含：
1. Global
2. In-Scope
3. Out-of-Scope
4. Next (Locked)
5. To-Do List (P0/P1/P2)
6. Drift Check (reason code + notes)

## Response ID Contract（新增）
每轮回复增加唯一编号用于引用：
- Format: `RID-YYYYMMDD-XXX`
- Example: `RID-20260501-001`
- 要求：同一线程内严格递增，不复用。

## Next (Locked)
冻结本文件作为后续规划与实现的唯一上游约束。

## Phase Switch Log
- Switched by owner Bigchao via two-step unlock
- Target Next-ID: NEXT-20260502-003
- Current locked action is tracked in `01_protocol/lock-state.current.json`
