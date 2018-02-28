
develop:
	virtualenv penv && . penv/bin/activate && python setup.py install && pip install -e .

test:
	pytest tests