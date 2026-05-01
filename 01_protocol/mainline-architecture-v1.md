# Mainline Architecture v1 (Structure Only, Frozen)

Status: DRAFT_FOR_CONFIRMATION
Linked Next-ID: NEXT-20260502-003

## 1) 为什么从 `01` 开始（而不是 `04`）
- 本仓库是新库，尚未建立已批准的多层编号体系。
- 以 `01_` 起始可表达“当前唯一主线层”，避免暗示存在未定义的 `02/03` 历史层。
- 编号用于治理可读性，不用于技术耦合；先从最小可解释集合开始。

## 2) 主线路总体结构（v1）

```text
01_protocol/
  boundary-confirmation-v1.md      # 已冻结：全局边界与锁规则
  lock-state.current.json          # 当前生效锁状态（Next-ID、阶段、解锁记录）
  mainline-architecture-v1.md      # 本文件：主线路架构定义（结构层）
```

说明：
- v1 只定义治理“骨架”，不引入执行脚本/schema/runtime。
- 新增层必须先经过 phase-switch 与 owner 确认。

## 3) 命名规则（v1）

### 3.1 目录命名
- 采用 `NN_name` 形式（`NN` 为两位数字）。
- 仅当需要新增同级治理层时，才允许创建 `02_*`。
- 禁止跳号创建（例如直接 `04_*`）。

### 3.2 文件命名
- 协议/确认类文档：`<topic>-v<major>.md`
  - 例：`boundary-confirmation-v1.md`
- 当前状态文件：`lock-state.current.json`
- 历史快照（若后续需要）：`lock-state.<timestamp>.json`

### 3.3 ID 命名
- Response ID：`RID-YYYYMMDD-XXX`（线程内递增）
- Next-ID：`NEXT-YYYYMMDD-XXX`
- 禁止混用 RID 与 NEXT。

## 4) 变更治理规则（v1）
- 任何改动 `Next (Locked)` 的行为都必须走双层解锁：
  1) 固定口令（确认解锁 / 确认切阶段）
  2) 目标 Next-ID
- 未解锁状态下，新增提议仅进入 To-Do，不得自动升格为 Next。
- 若发现偏航：默认 fail-closed（阻断并回拉）。

## 5) 主线推进方式（v1）
- 本阶段目标：先冻结“命名与分层治理”，再推进执行层。
- 每次仅允许一个锁定 Next。
- 通过条件：Owner 明确“确认通过”。

## 6) 非目标（本阶段不做）
- runtime drift guard 脚本实现
- schema 校验与自动化流水线
- 多人角色权限模型

---

## 冻结条件
当 Owner 确认本文通过后：
- 状态从 `DRAFT_FOR_CONFIRMATION` -> `FROZEN`
- 后续实现必须以本文件和 `boundary-confirmation-v1.md` 为双上游约束。
