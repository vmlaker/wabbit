##############################################
#
#  Makefile to install Python in virtualenv
#  with all dependencies for Wabbit.
#
##############################################

# Version of Twitter Bootstrap.
BOOTSTRAP_VER = 3.3.2

# The virtualenv's lib/ directory.
# If using a different Python version, edit here.
VENV_LIB = venv/lib/python2.7

# Path to the OpenCV library.
VENV_CV2 = $(VENV_LIB)/cv2.so

# Find cv2 library for the global Python installation.
GLOBAL_CV2 := $(shell /usr/bin/python -c 'import cv2; print(cv2)' | awk '{print $$4}' | sed s:"['>]":"":g)

# All CSS files to be built.
CSS_OUT = style.css

# By default:
#  1) create Python virtualenv w/ OpenCV
#  2) install node.js
#  3) do a build
#  4) get Bootstrap
#  5) build CSS files
all: $(VENV_CV2) node build bootstrap link_bootstrap $(CSS_OUT)

# Link global cv2 library file inside the virtual environment.
$(VENV_CV2): $(GLOBAL_CV2) venv
	cp $(GLOBAL_CV2) $@

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -r requirements.txt
	ln -f -s venv/bin/python

test: $(VENV_CV2)
	. venv/bin/activate && python -c 'import cv2; print(cv2)'

# Download the Bootstrap tarball, unzip and link at top level.
bootstrap:
	wget -c https://github.com/twbs/bootstrap/archive/v$(BOOTSTRAP_VER).zip
	unzip v$(BOOTSTRAP_VER).zip
	ln -f -s bootstrap-$(BOOTSTRAP_VER) bootstrap

link_bootstrap:
	mkdir -p static/css
	mkdir -p static/js
	ln -sf ../../bootstrap/dist/css/bootstrap.min.css static/css
	ln -sf ../../bootstrap/dist/js/bootstrap.min.js static/js

# Rule to buid CSS files out of templates.
%.css: src/css/%.css.in
	./python src/py/dotin.py $< > static/css/$@

COFFEE = node_modules/.bin/coffee
JADE = node_modules/.bin/jade

node: $(COFFEE) $(JADE)

$(COFFEE):
	npm install coffee-script

$(JADE):
	npm install jade

build: node
	$(JADE) --pretty -o templates/ src/jade/*.jade
	$(COFFEE) -o static/js/ -c src/coffee/*.coffee

clean: clean_bootstrap clean_py_node clean_build

clean_bootstrap:
	rm -f static/css/bootstrap.min.css
	rm -f static/js/bootstrap.min.js
	rm -rf bootstrap-$(BOOTSTRAP_VER)
	rm -rf bootstrap

clean_py_node:
	rm -rf venv
	rm -rf python
	rm -rf node_modules

clean_build:
	rm -rf templates
	rm -rf static/js/

# In addition to "clean", remove the downloaded tarball.
clean2: clean
	rm -rf v$(BOOTSTRAP_VER).zip
