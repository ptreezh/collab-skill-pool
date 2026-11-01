## 提交说明

**技能名**：

**一句话用途**：

## 发布门槛自查

- [ ] `sample_count ≥ 10`，实际为：
- [ ] 置信度 `confidence ≥ 0.6`，实际为：
- [ ] `status: candidate`（合并后由维护者置 approved）
- [ ] `unit: pool`
- [ ] 已运行 `python scripts/validate_pool_skill.py pool/skills/<文件名>.yaml` 且通过

## 脱敏确认（逐项勾选）

- [ ] 无真实客户名 / 公司名 / 人名
- [ ] 无手机号、身份证、邮箱、地址
- [ ] 无账号、令牌、密钥、内网 IP / 域名
- [ ] 无原始对话记录、无 personal 样本
- [ ] `skill_text` 已抽象为可公开复用的规则

## 来源说明（脱敏）

<!-- 只写来源类型，例如「脱敏自某电商团队客服复盘」，不要写具体客户 -->

## 冲突预检

- 本卡 `fingerprint`：
- 是否已检索池内同指纹/相近技能：是 / 否
- 若存在相近技能，说明差异：
