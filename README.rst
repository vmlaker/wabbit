wabbit
======

Using `SQLAlchemy <http://www.sqlalchemy.org>`_ to create
a MySQL database and user, with full priviledges.

First get a hold of them wabbit codes:
::

  git clone --recursive http://github.com/vmlaker/wabbit 
  cd wabbit

Before you start, you're gonna need `SQLAlchemy <http://www.sqlalchemy.org>`_ (it's real neat stuff, trust me):
::

  pip install SQLAlchemy

Now then, go ahead and set things up:
::

  python ./create.py

Go ahead and add a couple timestamps:
::

  python ./test.py
  python ./test.py

And now tear them things down:
::

  python ./drop.py

Now, weren't that fun?
