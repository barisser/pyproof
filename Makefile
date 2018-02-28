VIRTENV = penv
PACKAGE = pyproof

$(VIRTENV):
	rm -rf $(VIRTENV)
	virtualenv $(VIRTENV)
	. $(VIRTENV)/bin/activate; pip install -e .

dist:
	python setup.py sdist

lint: $(VIRTENV) develop
	. $(VIRTENV)/bin/activate; pylint --rcfile=../../.pylintrc pyproof

test: $(VIRTENV) develop FORCE
	export PYTHONPATH=.; . $(VIRTENV)/bin/activate; py.test tests -vvv --cov pyproof --cov-report=term-missing

develop: $(VIRTENV)
	. $(VIRTENV)/bin/activate; pip install pylint pytest pytest-cov && pip install -e .

clean:
	rm -rf $(VIRTENV) dist $(PACKAGE).egg-info
	find . -name '*.pyc' -delete

FORCE: