#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公共技能池 · 技能卡校验器（本地与 CI 共用）

用法:
    python scripts/validate_pool_skill.py                 # 校验 pool/skills/*.yaml
    python scripts/validate_pool_skill.py <file> [<file>] # 校验指定文件

退出码: 0 全部通过 / 1 存在不合规 / 2 依赖或路径错误
"""
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("缺少 PyYAML，请先执行: pip install pyyaml\n")
    sys.exit(2)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_DIR = os.path.join(ROOT, "pool", "skills")

REQUIRED_FIELDS = [
    "id", "name", "apply_expert_ids", "fingerprint", "sample_count",
    "major_type", "conflict_signatures", "skill_text", "status",
    "owner", "unit", "created_at", "updated_at",
]
ID_RE = re.compile(r"^sk_[0-9a-f]{12}$")
MIN_SAMPLE = 10
MAX_TEXT = 4000
ALLOWED_MAJOR = {"success", "failure"}
ALLOWED_STATUS = {"candidate", "approved", "deprecated"}

# 脱敏粗筛：(规则名, 正则, 提示)
SENSITIVE_RULES = [
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "疑似手机号"),
    ("身份证", re.compile(r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[0-9Xx](?!\d)"), "疑似身份证号"),
    ("邮箱", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "疑似邮箱"),
    ("令牌", re.compile(r"(ghp_|gho_|ghu_|ghs_|github_pat_|sk-[A-Za-z0-9]{20,})"), "疑似访问令牌"),
    ("内网IP", re.compile(r"(?<!\d)(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?!\d)"), "疑似内网地址"),
    ("personal样本", re.compile(r"(?i)\bpersonal\b|personal[_\s-]?sample|私密样本"), "出现 personal 样本字样"),
]


def validate_file(path):
    errors, warns = [], []
    name = os.path.basename(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            card = yaml.safe_load(f)
    except Exception as e:
        return ["YAML 解析失败: %s" % e], warns
    if not isinstance(card, dict):
        return ["顶层必须是 YAML 映射（key: value），当前为 %s" % type(card).__name__], warns

    missing = [k for k in REQUIRED_FIELDS if k not in card or card.get(k) in (None, "")]
    if missing:
        errors.append("缺少字段: %s" % ", ".join(missing))

    cid = str(card.get("id") or "")
    if cid and not ID_RE.match(cid):
        errors.append("id 格式不符（应为 sk_ + 12 位小写十六进制）: %s" % cid)
    if cid and ID_RE.match(cid) and name != cid + ".yaml":
        errors.append("文件名须等于 id: 期望 %s.yaml，实际 %s" % (cid, name))

    try:
        sc = int(card.get("sample_count"))
    except Exception:
        sc = -1
        errors.append("sample_count 必须是整数")
    if 0 <= sc < MIN_SAMPLE:
        errors.append("sample_count=%d 低于发布门槛 %d" % (sc, MIN_SAMPLE))

    if card.get("major_type") and card["major_type"] not in ALLOWED_MAJOR:
        errors.append("major_type 只能为 success/failure: %s" % card["major_type"])
    if card.get("status") and card["status"] not in ALLOWED_STATUS:
        errors.append("status 只能为 candidate/approved/deprecated: %s" % card["status"])
    if card.get("unit") and card["unit"] != "pool":
        errors.append("公共池技能卡 unit 必须为 pool，实际 %s" % card["unit"])

    text = card.get("skill_text") or ""
    if not isinstance(text, str) or not text.strip():
        errors.append("skill_text 不能为空")
    elif len(text) > MAX_TEXT:
        errors.append("skill_text 超长（%d > %d 字符）" % (len(text), MAX_TEXT))

    experts = card.get("apply_expert_ids")
    if experts is not None and not isinstance(experts, list):
        errors.append("apply_expert_ids 必须是列表")
    sigs = card.get("conflict_signatures")
    if sigs is not None and not isinstance(sigs, list):
        errors.append("conflict_signatures 必须是列表")

    scan = "\n".join(str(card.get(k) or "") for k in ("skill_text", "source_note", "owner", "name"))
    for rule, rx, msg in SENSITIVE_RULES:
        m = rx.search(scan)
        if m:
            errors.append("%s：命中「%s」" % (msg, m.group(0)[:32]))

    return errors, warns


def main():
    args = sys.argv[1:]
    if args:
        files = args
    else:
        files = sorted(glob.glob(os.path.join(CARD_DIR, "*.yaml")))
    if not files:
        print("[OK] pool/skills/ 下暂无技能卡，跳过校验")
        return 0

    failed = 0
    for p in files:
        if not os.path.isfile(p):
            print("[ERR] 文件不存在: %s" % p)
            failed += 1
            continue
        errs, _ = validate_file(p)
        if errs:
            failed += 1
            print("[FAIL] %s" % os.path.basename(p))
            for e in errs:
                print("       - %s" % e)
        else:
            print("[PASS] %s" % os.path.basename(p))

    print("\nTOTAL=%d PASS=%d FAIL=%d" % (len(files), len(files) - failed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
