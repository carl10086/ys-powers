"""共享配置：skill 来源与安装目标"""

# Source 目录按来源分层；runtime 一律扁平安装到 .claude/skills/<skill-name>/。
DIRECTORIES = {
    "skills/matt/engineering": ("skills", "skill-bucket"),
    "skills/matt/productivity": ("skills", "skill-bucket"),
    "skills/pstack": ("skills", "skill-bucket"),
    "skills/local": ("skills", "skill-bucket"),
}

# global install/update 时清理旧版 ys-powers 在目标目录留下的已登记能力。
# 只按 renames.json 中的明确旧名删除，不删除整个目标目录。
GLOBAL_LEGACY_TARGETS = {
    "skills": "skills",
    "commands": "commands",
    "agents": "agents",
    "references": "references",
    "hooks": "hooks",
    "rules": "rules"
}
