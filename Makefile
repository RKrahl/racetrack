PYTHON   = python


build:
	$(PYTHON) setup.py build


sdist:
	$(PYTHON) setup.py sdist


clean:
	rm -f *~ racetrack/*~
	rm -rf build

distclean: clean
	rm -f MANIFEST
	rm -f racetrack/*.pyc
	rm -rf racetrack/__pycache__
	rm -rf dist


.PHONY: build sdist clean distclean
