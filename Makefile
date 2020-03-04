.PHONY: demo rebuild tests

demo:
	rm -rf demo
	printf "demo\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

test:
	set -e; cd docs; ablog build -T; cd ..

test1:
	set -e; cd docs; ablog build -b latex -T -d .doctrees -w _latex; cd ..

test2:
	set -e; cd docs; ablog build -T -b json; cd ..

test3:
	set -e; cd docs; ablog build -T -b pickle; cd ..

test4:
	set -e; mkdir -p test; cd test; printf "\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start; ablog build; cd ..; rm -rf test

test5:
	set -e; mkdir -p testablog; printf "testablog\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start; cd testablog; ablog build; cd ..; rm -rf testablog

tests: test test1 test2 test3 test4 test5
