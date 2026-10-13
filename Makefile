PYTHON ?= python3
NOTEBOOKS = $(PYTHON) docs/tools/notebooks.py
DOCS_ENV = DOCS_PYTHON=$(shell $(PYTHON) -c "import sys; print(sys.executable)")

.PHONY: docs-install docs-notebooks docs-dev docs-build docs-preview docs-clean

docs-install:
	$(PYTHON) -m pip install -r docs/requirements.txt
	cd docs && npm ci

docs-notebooks:
	$(NOTEBOOKS) execute
	$(NOTEBOOKS) convert --strict

docs-dev:
	cd docs && $(DOCS_ENV) DOCS_VALIDATE_LINKS=false npm run dev

docs-build:
	cd docs && $(DOCS_ENV) npm run build && npm run check:mdx

docs-preview:
	cd docs && npm run preview

docs-clean:
	$(NOTEBOOKS) clean
	rm -rf docs/dist docs/.astro
