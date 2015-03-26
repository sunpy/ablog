

.PHONY: demo install rebuild

install:
	pip install -U --no-deps --force-reinstall .

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

demo:
	rm -rf demo
	printf "demo\nABlog\nABlog Team\nhttp://ablog.readthedocs.org" | ablog start