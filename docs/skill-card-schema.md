# 技能卡格式规范（pool/skills/*.yaml）

本仓的每张技能卡是一份**可直接挂载生效的专家技能**。字段与「协同进化后台 / Git 仓库模式」完全一致，便于在企业私有仓与公共仓之间迁移。

## 一、完整字段

```yaml
id: sk_a1b2c3d4e5f6        # 必填。sha1(unit + name + apply_expert_ids + fingerprint) 前12位，格式 sk_[0-9a-f]{12}
name: 客服话术冷启动模板      # 必填。技能名，20 字以内
apply_expert_ids:           # 必填。适用专家（对应专家包内 agents/<name>.md 的专家标识）
  - ex-customer-service
fingerprint: fp-8f31ad      # 必填。场景指纹（去版本号后的语义指纹），用于冲突预检
sample_count: 12            # 必填。支撑该技能的样本数，须 ≥ 10
major_type: success         # 必填。success（成功经验） | failure（失败教训）
conflict_signatures:        # 必填。强互斥签名；与池内既有卡冲突时不得合并
  - sig-clash-001
skill_text: |               # 必填。技能正文（提示词/规则），≤ 4000 字符
  当用户问「新店怎么起量」时……
status: candidate           # 必填。candidate | approved | deprecated
owner: member-hz-a          # 必填。贡献者标识（不要写真实姓名/手机号）
unit: pool                  # 必填。公共池固定为 pool（企业私有仓写 orgs/<unit>）
created_at: "2026-10-27"    # 必填
updated_at: "2026-11-01"    # 必填
license: CC-BY-4.0          # 建议。技能文本许可
source_note: 脱敏自某电商团队客服复盘   # 建议。来源说明（不得含客户名）
```

## 二、文件命名

- 文件名必须等于 `<id>.yaml`，例如 `sk_a1b2c3d4e5f6.yaml`；
- 一个 PR 一个技能卡（便于审核与回滚）。

## 三、校验规则（CI 强制）

`scripts/validate_pool_skill.py` 检查：

1. YAML 可解析、字段齐全、类型正确；
2. `id` 符合 `sk_[0-9a-f]{12}`，且与文件名一致；
3. `sample_count ≥ 10`、`major_type ∈ {success,failure}`、`status ∈ {candidate,approved,deprecated}`；
4. `unit == pool`；
5. `skill_text` 非空且 ≤ 4000 字符；
6. **脱敏粗筛**：不得出现手机号、18 位身份证、邮箱、`ghp_/gho_/sk-` 等令牌形态、内网 IP、`personal` 字样；
7. 同一 `fingerprint` 在池内重复时告警（人工判定是否冲突）。

粗筛只拦明显泄露，**最终脱敏由维护者在 PR 中人工确认**。

## 四、与协同后台的对应关系

| 公共仓 | 协同后台 |
|---|---|
| PR 提交 | `POST /collab/approvals/apply` |
| 维护者合并 | `POST /collab/approvals/{id}/decide`（approve） |
| `status: approved` | 状态机 approved |
| `git log` | `GET /collab/audit` |
| PR 模板门槛 | 发布门槛 `confidence≥0.6 且 sample≥10` |
