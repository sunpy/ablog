install:
	pip install -U --no-deps --force-reinstall .
rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

