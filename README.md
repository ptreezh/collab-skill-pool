# collab-skill-pool · 企业智能体公共技能池

面向「智能体学习型组织 2.0」的**公共技能池公开仓**：任何使用「专家越用越聪明·经验萃取师」的用户都可以**只读获取**这里的公共技能；想贡献技能的用户通过 **Pull Request** 提交，经维护者审核合并后对所有人生效。

## 一、这个仓库解决什么

| 用户类型 | 使用方式 |
|---|---|
| 个人 / 非机构用户，想获得优秀公共技能 | 只读：`git clone` 或由萃取师 `pool-pull` 拉取，**无需自建仓库** |
| 想贡献自己萃取出的技能 | 从你自己的仓库或本地 `pr-skill` 分支向本仓发起 PR，维护者审核合并 |
| 企业 / 团队内部协同 | 使用「企业AI经验库·安装官」搭建**私有仓或内网后台**，本仓仅作为公共池的只读上游 |

**隐私红线（重要）**
- 本仓只接收**已脱敏**、**用户明确标记为可公开共享**的技能卡；
- 禁止上传原始对话、personal 样本、客户真名、账号凭据、内网地址、未公开的业务数据；
- 技能卡正文（`skill_text`）一旦合并即公开，提交前请自行确认不含敏感信息。

## 二、目录结构

```
pool/skills/           # 唯一生效目录：公共技能卡（*.yaml）
meta/pool.yaml         # 池元信息：维护者、发布门槛、版本
docs/skill-card-schema.md   # 技能卡字段规范
contrib/README.md      # 贡献流程与脱敏自查清单
scripts/validate_pool_skill.py  # 技能卡校验器（本地 + CI 共用）
examples/skill-card.example.yaml # 示例卡（不生效，仅供参照）
.github/               # PR 模板 + 自动校验工作流
```

## 三、发布门槛（与协同后台一致）

| 门槛 | 要求 |
|---|---|
| 样本量 | `sample_count ≥ 10` |
| 置信度 | PR 描述注明 `confidence ≥ 0.6`，维护者核对 |
| 状态 | 合并前为 `candidate`，合并后由维护者置 `approved` |
| 冲突 | `conflict_signatures` 不得与池内既有卡强冲突 |
| 格式 | 通过 `scripts/validate_pool_skill.py` 校验（CI 强制） |

> CI 工作流已作为模板放在 `ci/validate.yml`。启用方式：仓库 owner 具备 `workflow` 权限后，将其复制到 `.github/workflows/validate.yml` 并提交即可。未启用前请本地运行 `python scripts/validate_pool_skill.py` 自检。

## 四、只读获取

```bash
git clone https://github.com/ptreezh/collab-skill-pool.git
```

或在萃取师对话中输入 `pool-pull`，自动拉取 `pool/skills/` 下的公共技能卡并导入本地技能清单。

## 五、贡献流程

1. Fork 本仓，在 `pool/skills/` 新增一张技能卡（文件名 `sk_<12位hex>.yaml`）；
2. 本地运行校验：`python scripts/validate_pool_skill.py pool/skills/你的卡.yaml`；
3. 按 `.github/PULL_REQUEST_TEMPLATE.md` 填写 PR：样本量、置信度、脱敏确认；
4. 维护者审核（必要时要求补充样本或脱敏）；
5. 合并后置 `status: approved`，全量用户下次 `pool-pull` 即生效。

## 六、许可

- 仓库结构与脚本：MIT（见 `LICENSE`）；
- `pool/skills/` 下的技能卡文本：CC BY 4.0，投稿即表示同意以该许可公开共享。

## 七、维护者

- 维护者：仓库 owner（当前 `ptreezh`）
- 审核响应：建议 5 个工作日内处理 PR
- 撤回：技能作者可提交 PR 将 `status` 改为 `deprecated` 或请求移除
