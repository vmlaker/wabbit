wabbit
======

Use `SQLAlchemy <http://www.sqlalchemy.org>`_ to create 
a MySQL database and user with full privileges.

Before you start, you need SQLAlchemy:
::

  pip install SQLAlchemy

Ok now, first get the **wabbit** code:
::

  git clone --recursive http://github.com/vmlaker/wabbit 
  cd wabbit

Now then, go ahead and set things up:
::

  python ./create.py

And finally, tear stuff down:
::

  python ./drop.py

Fun, huh?
