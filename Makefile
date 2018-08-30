PROJECT = ipyjulia_hacks

.PHONY: all test clean clean-pycache doc inject-readme update-init upload

all: test doc

## Testing
test:
	tox
	PYJULIA_TEST_REBUILD=yes tox -e py2

test-cov: test-cov-py3

test-cov-%:
	tox -e $* -- --cov $(PROJECT)
	$(MAKE) coverage-report-$*

coverage-report: coverage-report-py3

coverage-report-%:
	.tox/$*/bin/coverage combine .coverage
	.tox/$*/bin/coverage report
	.tox/$*/bin/coverage html --directory $(PWD)/.tox/$*/tmp/cov_html

clean: clean-pycache
	rm -rf src/*.egg-info .tox MANIFEST

clean-pycache:
	find src -name __pycache__ -o -name '*.pyc' -print0 \
		| xargs --null rm -rf

## Documentation
doc: inject-readme
	tox -e doc -- -W

update-init: inject-readme
	git commit --message "Update src/$(PROJECT)/__init__.py" \
		-- src/$(PROJECT)/__init__.py

## Inject content of README.rst to the docstring of __init__.py.
inject-readme: src/$(PROJECT)/__init__.py
src/$(PROJECT)/__init__.py: README.rst
	sed '1,/^"""$$/d' $@ > $@.tail
	rm $@
	echo '"""' >> $@
	cat README.rst >> $@
	echo '"""' >> $@
	cat $@.tail >> $@
	rm $@.tail
# Note that sed '1,/^"""$/d' prints the lines after the SECOND """
# because the first """ appears at the first line.

## Upload to PyPI
upload:
	rm -rf dist/
	python setup.py sdist
	twine upload dist/*
