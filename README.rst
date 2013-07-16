wabbit
======

Webcam image snapshot recorder and web app.
Put together with
`MPipe <http://vmlaker.github.io/mpipe>`_,
`OpenCV <http://docs.opencv.org>`_,
`CoffeeScript <http://coffeescript.org>`_,
`SQLAlchemy <http://www.sqlalchemy.org>`_, 
and `Flask <http://flask.pocoo.org>`_.

Install requirements and get Wabbit:
::

  pip install -r requirements.txt
  npm install coffee-script
  git clone --recursive http://github.com/vmlaker/wabbit 

Test drive:
::

  cd wabbit
  python src/create.py
  python src/record.py 5
  python src/dump.py
  python src/prune.py -60
  python src/dump.py
  python src/drop.py

Customize your app by editing files 
``wabbit.wsgi`` and ``wabbit.cfg``,
and deploy to your web server:
::

  coffee -o static -c src/main.coffee
  python src/deploy.py /var/www/html/wabbit

Configure your web server.
Then restart the server:
::

  systemctl restart httpd.service

Edit file ``wabbit.cron`` and then schedule the jobs:
::

  crontab wabbit.cron
 
The app is visible at http://localhost/wabbit.
