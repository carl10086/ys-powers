"""共享配置：目录映射与安装策略"""

# 要安装的目录配置
# 格式: 源目录名 -> (目标子目录名, 策略)
# 策略: 'folder' = 文件夹级全量覆盖, 'file' = 文件级同名覆盖
DIRECTORIES = {
    "skills": ("skills", "folder"),
    "rules": ("rules", "file"),
    "commands": ("commands", "file"),
    "agents": ("agents", "folder"),
    "hooks": ("hooks", "file"),
    "references": ("references", "file")
}
