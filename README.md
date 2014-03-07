Release Notes Generator
===============

Pulls JIRA issues for publication to Twitter and GetSatisfaction

Environment Setup
-----------------

First, make sure you have pip installed:

	sudo easy_install pip

Then install remaining requirements for pip:

	sudo pip install -r requirements.txt

Testing
-------

To run test suite:

    #> nosetests tests --with-coverage --cover-html

 [optional: --nocapture to allow std out to orint to screen.]

Results will be located in:

	$ cover/index.html

If there are packages that need omission or other settings use .coveragerc

Mock documentation found at:

	http://mock.readthedocs.org/en/latest/

Testing
-------

To run the tests:

    $ .....

To add tests see the `Commands` section earlier in this
README.


Contributing
------------

1. Fork it.
2. Create a branch (`git checkout -b my_project`)
3. Commit your changes (`git commit -am "Added Stuff"`)
4. Push to the branch (`git push origin my_project`)
5. Create an [Issue][1] with a link to your branch
6. Enjoy a refreshing Diet Coke and wait


[r2h]: http://github.com/socialize
[r2hc]: http://github.com/
[1]: http://github.com/socialize/issues

