

# ROOT_NAME = $(notdir $(shell pwd))
# BASENAME_ROOT = $(shell pwd)
# MAIN_BIN = $(ROOT_NAME)
# SPEC_FILE = "$(MAIN_BIN).spec"
# MAIN_FILE = "main.py"


test:
	pytest -vv -x -rP --color=yes

	# durations is to print all durations for every called func
tests:
	pytest -vv -x -rP --color=yes --durations=0

lint:
	pylint --load-plugins pylint_django -j 4 `ls -R|grep .py$|xargs`

clean:
	rm -rfv __pycache__
	rm -rfv build
	rm -rfv dist
	rm -rfv $(SPEC_FILE)
	rm -rfv .pytest_cache


mypy:
	mypy --install-types .


cov:
	# run
	coverage run -m pytest -vv -x -rP --color=yes
	# create html report
	coverage html
	# create badge for readme
	coverage-badge -f -o static/img/coverage/coverage.svg

	# create docs badge for readme
# 	docstr-coverage core --badge static/img/coverage/docs.svg
# 	docstr-coverage --accept-empty # make sure exits with code 0 to not ruin my make; this will always give exit code 1

	# open coverage results in browser
	firefox htmlcov/index.html &


pub:
	poetry publish --build