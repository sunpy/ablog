.PHONY: demo rebuild tests

demo:
	rm -rf demo
	printf "demo\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

test:
	cd docs; ablog build -T

test1:
	cd docs; ablog build -b latex -T -d .doctrees -w _latex

test2:
	cd docs; ablog build -T -b json

test3:
	cd docs; ablog build -T -b pickle

test4:
	mkdir -p test; cd test; printf "\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start; ablog build

test5:
	mkdir -p test; cd test; printf "ablog\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start; cd ablog; ablog build

tests: test test1 test2 test3 test4 test5
