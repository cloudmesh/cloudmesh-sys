package=sys
UNAME=$(shell uname)
export ROOT_DIR=${PWD}/cloudmesh/rest/server
VERSION=`head -1 VERSION`

define banner
	@echo
	@echo "###################################"
	@echo $(1)
	@echo "###################################"
endef

source:
	cd ../cloudmesh-cmd5; make source
	$(call banner, "Install cloudmesh-sys")
	pip install -e . -U
	$(call banner, "cms help sys")
	cms help sys

clean:
	$(call banner, "CLEAN")
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	rm -rf dist
	find . -name '__pycache__' -delete
	find . -name '*.pyc' -delete
	rm -rf .tox
	rm -f *.whl

######################################################################
# PYPI
######################################################################


twine:
	pip install -U twine

dist:
	python setup.py sdist bdist_wheel
	twine check dist/*

patch: clean
	$(call banner, patch to testpypi)
	bumpversion --allow-dirty patch
	python setup.py sdist bdist_wheel
	git push origin master --tags
	twine check dist/*
	twine upload --repository testpypi https://test.pypi.org/legacy/ dist/*

release: clean dist
	$(call banner, release to pypi)
	bumpversion release
	python setup.py sdist bdist_wheel
	git push origin master --tags
	twine check dist/*
	twine upload dist/*

pip: patch
	pip install --index-url https://test.pypi.org/simple/ \
	    --extra-index-url https://pypi.org/simple cloudmesh-$(package)

log:
	$(call banner, log)
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push