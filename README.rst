wabbit
======

Just learning `SQLAlchemy <http://www.sqlalchemy.org>`_.
::

  pip install SQLAlchemy
  pip install mpipe
  git clone --recursive http://github.com/vmlaker/wabbit 
  cd wabbit
  python ./create.py
  python ./record.py 0 640 480 3
  python ./dump.py
  python ./prune.py 1
  python ./dump.py
  python ./drop.py
