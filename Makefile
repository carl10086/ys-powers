.DEFAULT_GOAL := help

YS_POWERS_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: help sync-html global-install local-install update-global update-local uninstall-global uninstall-local

help:
	@echo "ys-powers Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make help              显示此帮助信息"
	@echo "  make global-install    安装到 ~/.claude/（全局生效）"
	@echo "  make local-install     安装到当前目录 ./.claude/（当前项目）"
	@echo "  make local-install project-dir=/path/to/project"
	@echo "                         安装到指定项目目录"
	@echo "  make update-global     更新全局安装"
	@echo "  make update-local      更新本地安装"
	@echo "  make uninstall-global  卸载全局安装"
	@echo "  make uninstall-local   卸载本地安装"
	@echo "  make sync-html         同步 html-anything 上游更新"
	@echo ""
	@echo "安装策略："
	@echo "  global: skills/commands/agents/rules/hooks 复制到 ~/.claude/"
	@echo "  local:  同上，但复制到 <project-dir>/.claude/"
	@echo "  hooks 注入 settings.json (global) 或 settings.local.json (local)"

sync-html:
	python3 scripts/sync_html_anything.py

global-install:
	python3 $(YS_POWERS_ROOT)/install/install.py install global

local-install:
	@if [ -n "$(project-dir)" ]; then \
		python3 $(YS_POWERS_ROOT)/install/install.py install local --target $(project-dir); \
	else \
		python3 $(YS_POWERS_ROOT)/install/install.py install local; \
	fi

update-global:
	python3 $(YS_POWERS_ROOT)/install/install.py update global

update-local:
	@if [ -n "$(project-dir)" ]; then \
		python3 $(YS_POWERS_ROOT)/install/install.py update local --target $(project-dir); \
	else \
		python3 $(YS_POWERS_ROOT)/install/install.py update local; \
	fi

uninstall-global:
	python3 $(YS_POWERS_ROOT)/install/install.py uninstall global

uninstall-local:
	@if [ -n "$(project-dir)" ]; then \
		python3 $(YS_POWERS_ROOT)/install/install.py uninstall local --target $(project-dir); \
	else \
		python3 $(YS_POWERS_ROOT)/install/install.py uninstall local; \
	fi
