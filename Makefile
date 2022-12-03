PYTHON_EXEC = python3
PIP_EXEC = pip3
THIS_FILE := $(lastword $(MAKEFILE_LIST))

.PHONY: help run install save

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

run:
	$(PYTHON_EXEC) main.py

install:
	$(PIP_EXEC) install --upgrade pip
	$(PIP_EXEC) install --user -r requirements.txt

save:
	$(PIP_EXEC) freeze >> requirements.txt
