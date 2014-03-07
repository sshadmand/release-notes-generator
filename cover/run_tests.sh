rm -Rf .coverage
/usr/local/bin/coverage --omit="*/Library/*" -x /usr/local/bin/nosetests tests/
open htmlcov/index.html