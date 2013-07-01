wabbit
======

Something put together with
`SQLAlchemy <http://www.sqlalchemy.org>`_, 
`OpenCV <http://docs.opencv.org>`_,
`MPipe <http://vmlaker.github.io/mpipe>`_,
`CoffeeScript <http://coffeescript.org>`_,
and `Flask <http://flask.pocoo.org>`_.
::

  pip install SQLAlchemy
  pip install mpipe
  pip install Flask
  git clone --recursive http://github.com/vmlaker/wabbit 
  cd wabbit
  python create.py
  python record.py 0 640 480 30
  python dump.py
  python prune.py -60
  python dump.py
  python drop.py


Also:
::

  npm install coffee-script
  coffee -o static -c main.coffee
  python serve.py
