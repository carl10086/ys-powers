"""共享配置：目录映射与安装策略"""

# 当前只安装 Matt 的 skills 与 ys-powers 的 eli。旧版 rules 不再自动安装。
# 格式: 源目录名 -> (目标子目录名, 策略)
DIRECTORIES = {
    "skills/engineering": ("skills", "skill-bucket"),
    "skills/productivity": ("skills", "skill-bucket"),
    "skills/eli": ("skills/eli", "folder")
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
