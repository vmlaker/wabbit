.. image:: static/logo.png

wabbit
======

My trusty little webcam snapshot recorder and viewer web app.
Check out a live installation at http://vmlaker.org/wabbit.

Wabbit is written in Python,
with a little bit of `CoffeeScript <http://coffeescript.org>`_
for the web page.
Camera interaction is run with `OpenCV <http://docs.opencv.org>`_.
Image processing workflow is implemented using
`MPipe <http://vmlaker.github.io/mpipe>`_.
Database is accessed via `SQLAlchemy <http://www.sqlalchemy.org>`_,
with MySQL as the database engine.
The web app itself runs on `Flask <http://flask.pocoo.org>`_.

Start by getting all the necessary codes to run Wabbit:
::

  pip install -r requirements.txt
  npm install coffee-script
  git clone --recursive http://github.com/vmlaker/wabbit 

Additionally, you will need the aforementioned softwares,
with Python bindings where applicable. 
To run the web app on Apache HTTPD, you're gonna need mod_wsgi.

Test the camera:
::

  cd wabbit
  python src/create.py
  python src/record.py 10
  python src/dump.py
  python src/prune.py -60
  python src/dump.py
  python src/drop.py

Compile the front end (from CoffeeScript to JavaScript):
::

  coffee -o static -c src/main.coffee

Customize your app by editing files ``wabbit.wsgi`` and ``wabbit.cfg``.
Then deploy to your web server. For Apache HTTPD
(assuming your ``DocumentRoot`` is ``/var/www/html/wabbit``)
do this:
::

  python src/deploy.py /var/www/html/wabbit

Configure your web server, then restart:
::

  systemctl restart httpd.service
