"""共享配置：目录映射与安装策略"""

# 要安装的目录配置
# 格式: 源目录名 -> (目标子目录名, 策略)
# 只安装 Matt 的稳定工程/通用能力，以及 ys-powers 的 eli。
DIRECTORIES = {
    "skills/engineering": ("skills", "skill-bucket"),
    "skills/productivity": ("skills", "skill-bucket"),
    "skills/eli": ("skills/eli", "folder"),
    "rules": ("rules", "file")
}
