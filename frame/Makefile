PKG_NAME=rango-frame


.PHONY: all build clean install uninstall test dist-test


all: build


build:
	python setup.py sdist


uninstall:
	pip uninstall -y $(PKG_NAME)


install: build
	pip install --upgrade dist/$(PKG_NAME)-*.tar.gz


test:
	python -m unittest discover


clean:
	rm -rf dist *.egg-info


dist-test:
	cd /tmp && python -m unittest discover -s $(PKG_NAME)

