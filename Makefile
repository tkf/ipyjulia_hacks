PROJECT = ipyjulia_hacks

.PHONY: test clean clean-pycache upload

## Testing
test:
	tox

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

## Upload to PyPI
upload:
	rm -rf dist/
	python setup.py sdist
	twine upload dist/*
