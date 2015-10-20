.PHONY: demo install rebuild release test docs

demo:
	rm -rf demo
	printf "demo\nABlog\nABlog Team\nhttp://ablog.readthedocs.org" | ablog start

install:
	pip install -U --no-deps --force-reinstall .

docs:
	export PYTHONPATH="$(shell pwd)"; echo $$PYTHONPATH; cd docs; ablog build -a -P

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

release:
	python setup.py register
	python setup.py sdist upload

test:
	cd docs; ablog build -T
	cd docs; ablog build -b latex -T -d .doctrees -w _latex
	cd docs; ablog build -T -b json
	cd docs; ablog build -T -b pickle
	mkdir -p test; cd test; printf "\nABlog\nABlog Team\nhttp://ablog.readthedocs.org" | ablog start; ablog build
	mkdir -p test; cd test; printf "ablog\nABlog\nABlog Team\nhttp://ablog.readthedocs.org" | ablog start; cd ablog; ablog build
