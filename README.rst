wabbit
======

Something with
`SQLAlchemy <http://www.sqlalchemy.org>`_, 
`OpenCV <http://docs.opencv.org>`_,
`MPipe <http://vmlaker.github.io/mpipe>`_,
and `Flask <http://flask.pocoo.org>`_.
::

  pip install SQLAlchemy
  pip install mpipe
  pip install Flask
  git clone --recursive http://github.com/vmlaker/wabbit 
  cd wabbit
  python ./create.py
  python ./record.py 0 640 480 30
  python ./dump.py
  python ./prune.py -60
  python ./dump.py
  python ./drop.py


Also:
::

  python ./serve.py
