wabbit
======

Use them's `SQLAlchemy <http://www.sqlalchemy.org>`_ to create 
a MySQL database and user, with full priviledges, ye hear.

All righty now, first get a hold of them's **wabbit** code:
::

  git clone --recursive http://github.com/vmlaker/wabbit 
  cd wabbit

Before yer start, you's goan need `SQLAlchemy <http://www.sqlalchemy.org>`_ (it's real neat stuff, trust me):
::

  pip install SQLAlchemy

Now then, go ahead and set things up, sonny:
::

  python ./create.py

And finally, tear them thangs down:
::

  python ./drop.py

Now wasn't that fun?
