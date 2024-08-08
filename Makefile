.PHONY: demo rebuild tests

demo:
	rm -rf demo && mkdir demo
	printf "demo\nABlog\nABlog Team\nhttps://ablog.readthedocs.io/" | ablog start

rebuild:
	cd docs; watchmedo shell-command --patterns='*.rst' --command='ablog build' --recursive

test:
	set -e; cd docs; git clean -xfd; ablog build -T -W; git clean -xfd; cd ..

test1:
	set -e; cd docs; git clean -xfd; ablog build -T -W -b json; git clean -xfd; cd ..

test2:
	set -e; cd docs; git clean -xfd; ablog build -T -W -b pickle; git clean -xfd; cd ..

test3:
	set -e; mkdir -p test; cd test; git clean -xfd; printf "\nABlog\nABlog Team\nhttps://ablog.readthedocs.io/" | ablog start; ablog build -W; cd ..; rm -rf test

test4:
	set -e; mkdir -p testablog; cd testablog; git clean -xfd; printf "\nABlog\nABlog Team\nhttps://ablog.readthedocs.io/" | ablog start; ablog build -W; cd ..; rm -rf testablog

test5:
	set -e; cd docs; git clean -xfd; ablog build -W -b latex -T -d .doctrees -w _latex; git clean -xfd; cd ..

tests: test test1 test2 test3 test4 test5
