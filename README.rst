wabbit
======

Webcam snapshot recorder and web server,
put together with
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

For the server, first customize your installation by
editing files ``wabbit.wsgi`` and ``wabbit.cfg``.
Then, deploy the service and restart httpd: 
::

  npm install coffee-script
  coffee -o static -c main.coffee
  python deploy.py /var/www/html/wabbit
  systemctl restart httpd.service

The app is visible at http://localhost/wabbit.
