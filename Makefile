.PHONY: demo rebuild tests

demo:
	rm -rf demo
	printf "demo\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

test:
	set -e; cd docs; ablog build -T -W; git clean -xfd; cd ..

test1:
	set -e; cd docs; ablog build -T -W -b json; git clean -xfd; cd ..

test2:
	set -e; cd docs; ablog build -T -W -b pickle; git clean -xfd; cd ..

test3:
	set -e; mkdir -p test; cd test; printf "\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start; ablog build -W; cd ..; rm -rf test

test4:
	set -e; mkdir -p testablog; cd testablog; printf "\nABlog\nABlog Team\nhttps://ablog.readthedocs.org" | ablog start; ablog build -W; cd ..; rm -rf testablog

tests: test test1 test2 test3 test4
