# Introduction #

pydicom is mainly concerned with getting at the DICOM data elements in files, but it is often desirable to view pixel data as an image. There are several options:
  * Use any of the many [DICOM viewer](http://www.dclunie.com/medical-image-faq/html/part8.html#DICOMFileConvertorsAndViewers) programs available
  * use pydicom with [matplotlib](http://matplotlib.sourceforge.net/)
  * use pydicom with the [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/)
  * use pydicom with python's Tkinter

# Using pydicom with matplotlib #
matplotlib is available at http://matplotlib.sourceforge.net/. It can take 2-d image information from Dataset.pixel\_array and display it. Here is an example:
```
>>> import dicom
>>> import pylab
>>> ds=dicom.read_file("CT_small.dcm")
>>> pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
<matplotlib.image.AxesImage object at 0x0162A530>
>>> pylab.show()
>>>
```
Thanks to Roy Keyes for pointing out how to do this.

# Using pydicom with Python Imaging Library (PIL) #
See the example file in the contrib directory:
http://code.google.com/p/pydicom/source/browse/source/dicom/contrib/pydicom_PIL.py

The key line is as follows, but the example file shows how to also adjust the window and level if available
```
im = Image.frombuffer(mode, size, ds.PixelData, "raw", mode, 0, 1)
im.show()
```

# Using pydicom with Tkinter #
The following contrib file shows a method for viewing images using Tkinter:
http://code.google.com/p/pydicom/source/browse/source/dicom/contrib/pydicom_Tkinter.py