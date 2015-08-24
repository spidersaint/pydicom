## Python 3 strategy ##

(Updated March 31, 2012)
I've been reading up on converting to python 3. Below are some notes of what seem to be the major steps and issues, and some good links. This is the start of a loose roadmap for converting pydicom to python 3.

### 1. Get some important bugs/features implemented ###
  1. Fix any remaining major bugs (done)
  1. Implement DICOM 'keywords' ([issue 53](https://code.google.com/p/pydicom/issues/detail?id=53)) (done)
  1. Test and release as pydicom 0.9.7 (done, although may need some fixes, especially re DS decimal type)
  1. Create a branch for pydicom on python <2.6. Only significant bug fixes will be merged to this branch. All new features in the main trunk (including the rest of the steps below) will not be compatible with python < 2.6. (trunk now has quite a number of commits with python >= 2.6 conversion)

Pydicom 0.9.7 will still run on python 2.4 to 2.7. For pydicom 0.9.8 and later, python >=2.6 will be required, as this greatly eases the transition to python 3.

### 2. "Improve your code with modern idioms"<sup>1</sup> ###

Go through reference `[1]` and do all the things it says. Some have already been done (use of _sorted_() where possible, key comparison). The most important ones that still remain:
  1. [Using context managers wherever possible](http://python3porting.com/improving.html#coding-with-context-managers), particularly the 'with open()' for file reading (deferred; it is rarely possible to make use of these in pydicom -- existing code working fine; will probably leave alone for now)
  1. Convert to the [new string formatting](http://python3porting.com/improving.html#advanced-string-formatting) (probably at least half done; still need to convert some tests)
  1. [More use of generators](http://python3porting.com/improving.html#yield-to-the-generators) where possible and [comprehensions](http://python3porting.com/improving.html#more-comprehensions).

### 3. Change as much code as possible to be common to both python >= 2.6 and python 3 ###

There are several good references for this, e.g. `[2, 3, 8]`, the steps below mostly follow `[2]`
  1. Run python2.6 with "-3" switch to see changes needed, which will include the following:
  1. Change the exception syntax.  (done)
  1. Convert to proper [absolute and relative imports](http://docs.python.org/whatsnew/2.5.html#pep-328) using _from__future__import absolute\_import_ (tried this but is not actually useful. Existing code already specifies full path to pydicom submodules, which is much easier to read and understand)
  1. Go through the code and [sort out bytes vs. strings](http://python3porting.com/preparing.html#separate-binary-data-and-strings). This is likely to be the most difficult step. In python 3, _str_ = unicode. Most of pydicom parsing will be in bytes; many data element values (text value, PN, etc) will be str (unicode). Can mark bytes literals with 'b' prefix `[5]`, string literals with 'u' prefix. There is also a _from__future__import unicode\_literals_ option `[6]` (? use it ?) (unicode\_literals tried, it is not the right path. See Unicode section below).
  1. Check out slicing issues `[3]`. `__getitem__` needs to handle slices, `__getslice__` no longer exists.

### 4. Use 2to3 in Distribute ###

2to3 should be able to [handle most of the conversions](http://lucumr.pocoo.org/2010/2/11/porting-to-python-3-a-guide#to3-through-distribute) remaining after the above steps. If necessary, custom converters could be written. If this does not work out, then would have to maintain two separate code branches. Or, could explore directly coding for python 3, and running 3to2 to convert back to python 2.
(2to3 has been run and bugs are being tamed one by one. Down to about 40-some when running the test suite)

## Update: Unicode strategy ##
March 31, 2012: After some experience trying various things with unicode, I think I understand the best/easiest way to do this. In a single phrase, it is: 'leave the strings in their native format'. In other words, let strings in python 2 be their normal strings, and let text strings in python 3 be unicode. A minimum of labelling (e.g. b"string") is needed for this. This works much better than forcing future unicode\_literals on python 2, as user code would need to convert to unicode to match. In other words, old code would break, and new code would be subject to constant vigilance over what is unicode and what isn't.

The "unicode sandwich" approach requires converting dicom data element text values (and even the VR string itself from the data element header) into unicode immediately after being read in, and converting them to bytes just before being written out to file. The repository changes are in the middle of this conversion now.

A really nice presentation by Ned Batchelder explains unicode and the "pro tips" for how to deal with it: http://nedbatchelder.com/text/unipain.html. Great idea there to use "fancy-text" generators as test strings that are readable as english but use exotic characters.


### References ###
  1. http://nedbatchelder.com/text/unipain.html  -- very nice unicode presentation from PyCon 2012
  1. http://python3porting.com/improving.html#improving-chapter
  1. http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/
  1. http://dabeaz.blogspot.com/2011/01/porting-py65-and-my-superboard-to.html. Walks through conversion of one project. Some good tips and tricks here, especially for exceptions and for slicing.
  1. http://docs.python.org/library/2to3.html#to3-reference
  1. http://docs.python.org/whatsnew/2.6.html#pep-3112-byte-literals
  1. http://stackoverflow.com/questions/809796/any-gotchas-using-unicode-literals-in-python-2-6
  1. http://peadrop.com/blog/2009/04/05/porting-your-code-to-python-3/. A bit older (April 2009) but a really nice explanation of the changes, why, and a side-by-side comparison of old and new behaviour. Reads well. Covers unicode, new I/O system, standard lib reorganization…
  1. http://docs.pythonsprints.com/python3_porting/py-porting.html.  _Very_ nice details about common code-based principles, including an interesting idea -- splitting version-dependent things into compat.two and compat.three modules, only one of which is imported depending on the python version.