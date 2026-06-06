.DEFAULT_GOAL := help

YS_POWERS_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON := uv run --python 3.12 python

.PHONY: help sync-html global-install local-install update-global update-local uninstall-global uninstall-local opencli-install opencli-uninstall

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
	@echo "  make opencli-install   安装 opencli skills 到当前项目"
	@echo "  make opencli-install project-dir=/path/to/project"
	@echo "                         安装 opencli skills 到指定项目"
	@echo "  make opencli-uninstall 卸载 opencli skills"
	@echo ""
	@echo "快捷变量："
	@echo "  project-dir= 或 p=     指定目标项目目录（local 范围）"
	@echo ""
	@echo "自动检测："
	@echo "  uninstall local 未指定 project-dir 时，若在非 ys-powers 项目"
	@echo "  且该项目存在 .claude/settings.local.json，则自动卸载当前项目"
	@echo ""
	@echo "安装策略："
	@echo "  global: skills/commands/agents/rules/hooks 复制到 ~/.claude/"
	@echo "  local:  同上，但复制到 <project-dir>/.claude/"
	@echo "  hooks 注入 settings.json (global) 或 settings.local.json (local)"

sync-html:
	$(PYTHON) scripts/sync_html_anything.py

global-install:
	$(PYTHON) $(YS_POWERS_ROOT)/install/install.py install global

local-install:
	@if [ -n "$(project-dir)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py install local --target $(project-dir); \
	elif [ -n "$(p)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py install local --target $(p); \
	else \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py install local; \
	fi

update-global:
	$(PYTHON) $(YS_POWERS_ROOT)/install/install.py update global

update-local:
	@if [ -n "$(project-dir)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py update local --target $(project-dir); \
	elif [ -n "$(p)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py update local --target $(p); \
	else \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py update local; \
	fi

uninstall-global:
	$(PYTHON) $(YS_POWERS_ROOT)/install/install.py uninstall global

uninstall-local:
	@if [ -n "$(project-dir)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py uninstall local --target $(project-dir); \
	elif [ -n "$(p)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py uninstall local --target $(p); \
	else \
		$(PYTHON) $(YS_POWERS_ROOT)/install/install.py uninstall local; \
	fi

opencli-install:
	@if [ -n "$(project-dir)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/opencli-skills.py install $(project-dir); \
	elif [ -n "$(p)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/opencli-skills.py install $(p); \
	else \
		$(PYTHON) $(YS_POWERS_ROOT)/install/opencli-skills.py install .; \
	fi

opencli-uninstall:
	@if [ -n "$(project-dir)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/opencli-skills.py uninstall $(project-dir); \
	elif [ -n "$(p)" ]; then \
		$(PYTHON) $(YS_POWERS_ROOT)/install/opencli-skills.py uninstall $(p); \
	else \
		$(PYTHON) $(YS_POWERS_ROOT)/install/opencli-skills.py uninstall .; \
	fi
