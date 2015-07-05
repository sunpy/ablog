

.PHONY: demo install rebuild release

demo:
	rm -rf demo
	printf "demo\nABlog\nABlog Team\nhttp://ablog.readthedocs.org" | ablog start

install:
	pip install -U --no-deps --force-reinstall .

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

release:
	python setup.py register
	python setup.py sdist upload
