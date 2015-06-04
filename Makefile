##############################################
#
#  Makefile to install Python in virtualenv
#  with all dependencies for Wabbit.
#
##############################################

# The virtualenv's lib/ directory.
# If using a different Python version, edit here.
VENV_LIB = venv/lib/python2.7

# Path to the OpenCV library.
VENV_CV2 = $(VENV_LIB)/cv2.so

# Find cv2 library for the global Python installation.
GLOBAL_CV2 := $(shell /usr/bin/python -c 'import cv2; print(cv2)' | awk '{print $$4}' | sed s:"['>]":"":g)

# By default:
#  1) create Python virtualenv w/ OpenCV
#  2) install node.js
#  3) do a build
all: $(VENV_CV2) node build

# Link global cv2 library file inside the virtual environment.
$(VENV_CV2): $(GLOBAL_CV2) venv
	cp $(GLOBAL_CV2) $@

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -r requirements.txt
	ln -s venv/bin/python

test: $(VENV_CV2)
	. venv/bin/activate && python -c 'import cv2; print(cv2)'

COFFEE = node_modules/.bin/coffee
JADE = node_modules/.bin/jade

node: $(COFFEE) $(JADE)

$(COFFEE):
	npm install coffee-script

$(JADE):
	npm install jade

build: node
	$(JADE) --pretty -o templates/ src/jade/*.jade
	$(COFFEE) -o static/ -c src/coffee/*.coffee

clean: clean_py_node clean_build

clean_py_node:
	rm -rf venv
	rm -rf python
	rm -rf node_modules

clean_build:
	rm -rf templates
	rm -rf static/*.js
