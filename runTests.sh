#!/bin/bash


# python3 -m unittest Tests.DbContentTests

# coverage run --source=./dbApi.py -m unittest Tests.DbApiTests

# Coverage doesn't work with cython files.
# Therefore, we don't run the BK Tree tests with it.
# python3 -m unittest Tests.BinaryConverterTests
# python3 -m unittest Tests.BKTreeTests

# coverage report
# coverage report --show-missing
# coverage erase

# python3 $(which nosetests) --exe --cover-package=dbApi --cover-package=dbPhashApi Tests.Test_PhashDbApi_Basic
# python3 $(which nosetests) --exe --with-coverage --cover-package=dbApi --cover-package=dbPhashApi Tests.Test_PhashDbApi_PHashStuff
# python3 $(which nosetests) --exe --cover-package=dbApi --cover-package=dbPhashApi Tests.Test_BKTree
# python3 $(which nosetests) --exe --with-coverage -s --cover-package=dbPhashApi Tests.Test_PhashDbApi_PHashStuff

# python3 $(which nosetests) --exe --with-coverage --cover-package=dbApi --cover-package=dbPhashApi Tests

if [ ! -d py3 ]; then
	python3 -m venv --without-pip py3
	wget https://bootstrap.pypa.io/get-pip.py
	./py3/bin/python get-pip.py
	rm get-pip.py
	# py3/bin/pip install zipfile./
	py3/bin/pip install rarfile
	py3/bin/pip install pylzma
	py3/bin/pip install nose
	py3/bin/pip install nose-cov
	py3/bin/pip install python-magic
fi


if [ ! -d py2 ]; then

	python2 -m virtualenv py2
	wget https://bootstrap.pypa.io/get-pip.py
	./py2/bin/python get-pip.py
	rm get-pip.py
	# py2/bin/pip install zipfile./
	py2/bin/pip install rarfile
	py2/bin/pip install pylzma
	py2/bin/pip install nose
	py2/bin/pip install nose-cov
	py2/bin/pip install python-magic

fi

source py3/bin/activate
python3 $(which nosetests) --with-coverage --exe --cover-package=UniversalArchiveInterface
coverage report --show-missing
coverage erase

source py2/bin/activate
python2 $(which nosetests) --with-coverage --exe --cover-package=UniversalArchiveInterface
coverage report --show-missing
coverage erase
