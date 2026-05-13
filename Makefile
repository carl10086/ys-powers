.PHONY: sync-html global-install local-install update-global update-local uninstall-global uninstall-local

YS_POWERS_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

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
