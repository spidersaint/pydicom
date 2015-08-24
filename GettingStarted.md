# Introduction #

pydicom is a pure python package for parsing DICOM files (generally medical image files but also non-image files such as radiotherapy information). It is not meant as an image viewer (there are many of those) but is targeted to getting the DICOM data elements as python variables and altering them if desired, and being able to do so in your own code.

pydicom has a [license](http://code.google.com/p/pydicom/source/browse/source/dicom/license.txt) based on the MIT license.


# Installing #

To use pydicom 0.9.8, python 2.6 or greater is required (earlier versions of pydicom can run under python >=2.4). Pydicom 0.9.8 can also unofficially run under python 3.x. To try it, uncomment two lines as indicated in the setup.py file before running python3 setup.py install.

Note: in addition to the instructions below, pydicom can also be installed through the [Python(x,y)](http://www.pythonxy.com/) distribution, which can install python and a number of packages (including pydicom) at once.

Installing using Windows binary release:
  * install a recent python version such as [Activepython](http://activestate.com/activepython) or the version at the python web site (http://python.org/download/).
  * download and run the pydicom windows executable installer from the [Downloads](http://code.google.com/p/pydicom/downloads/list) tab.

Installing using [pip](http://pypi.python.org/pypi/pip):
  * at a command prompt (you may need `sudo` on linux):
> ` pip install pydicom `

Installing from source (all platforms):
  * download the source code from the [Downloads tab](http://code.google.com/p/pydicom/downloads/list) or [checkout the mercurial repository source](http://code.google.com/p/pydicom/source/checkout)
  * at a command line, change to the directory with the setup.py file
  * with admin privileges, run `python setup.py install`
    * could also use `python setup.py develop` to keep the installation in the download location
    * with some linux variants, for example, use `sudo python setup.py install`
    * with other linux variants you may have to `su` before running the command.

Installing on Mac
  * Mac users can always use pip or install from source as noted above
  * MacPorts portfiles (e.g. py26-pydicom) are available. This is maintained by other users and may not immediately be up to the latest release.

# Using pydicom #

Once installed, the package can be imported at a python command line or used in your own python program with `import dicom` (note the package name is `dicom`, not `pydicom` when used in code. See the [examples directory](http://code.google.com/p/pydicom/source/browse/#hg/source/dicom/examples) for both kinds of uses. Also see the PydicomUserGuide for more details of how to use the package.

# Documentation #

Documentation for pydicom can be found at:
  * the wiki at http://code.google.com/p/pydicom/w/list
  * doc strings in the code. View these directly in the source files, or use python's help function at the command line. For example:
```
>>> import dicom
>>> ds = dicom.read_file("CT_small.dcm")
>>> help(ds)
Help on Dataset in module dicom.dataset object:

class Dataset(__builtin__.dict)
 |  A Dataset is a collection (dictionary) of Dicom DataElement instances.
 |  
 |  Example of two ways to retrieve or set values:
 |  (1) dataset[0x10, 0x10].value --> patient's name
 |  (2) dataset.PatientName --> patient's name
 |  
...
```
  * in-line comments in the code.
  * example programs in the [examples directory](http://code.google.com/p/pydicom/source/browse/#hg/source/dicom/examples)

# Support #

Please join the [pydicom discussion group](http://groups.google.com/group/pydicom) to ask questions, give feedback, post example code for others -- in other words for any discussion about the pydicom code. New versions, major bug fixes, etc. will also be announced through the group.

# Next Step #

To start learning how to use pydicom, see the PydicomUserGuide.