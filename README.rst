wabbit
======

Something put together with
`MPipe <http://vmlaker.github.io/mpipe>`_,
`OpenCV <http://docs.opencv.org>`_,
`CoffeeScript <http://coffeescript.org>`_,
`SQLAlchemy <http://www.sqlalchemy.org>`_, 
and `Flask <http://flask.pocoo.org>`_.
::

  pip install -r requirements.txt
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
