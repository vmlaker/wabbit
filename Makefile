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

# By default, build OpenCV and install node.
all: $(VENV_CV2) node

# Link global cv2 library file inside the virtual environment.
$(VENV_CV2): $(GLOBAL_CV2) venv
	cp $(GLOBAL_CV2) $@

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -r requirements.txt

test: $(VENV_CV2)
	. venv/bin/activate && python -c 'import cv2; print(cv2)'

COFFEE = node_modules/.bin/coffee
JADE = node_modules/.bin/jade

node: $(COFFEE) $(JADE)
	$(JADE) --pretty -o templates/ src/*.jade
	$(COFFEE) -o static -c src/*.coffee

$(COFFEE):
	npm install coffee-script

$(JADE):
	npm install jade

clean:
	rm -rf venv
	rm -rf node_modules
