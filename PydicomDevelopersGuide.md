
---

This is a **DRAFT** version of a high-level discussion of how pydicom works for those interested in contributing to pydicom's development. If you are interested in _using_ pydicom, see the PydicomUserGuide.

This is very rough, but it's a start. It is based on version 0.9.3. The source code itself can provide the details. The idea here is to outline the overall flow and point to the source code files involved with these steps.

There may be some code reorganization or re-factoring after 0.9.3 which changes some of the details below.

---


# How pydicom reads DICOM files: #

## DicomFileLike ##
All DICOM file reading in pydicom is done using a DicomFileLike object (filebase.py).  DicomFileLike objects have the standard python file methods, read, write, close, seek, tell. They also understand big-endian vs. little-endian byte orders, and will transparently read DICOM tags, and short or long integers correctly accounting for byte order. There are variants of this object for real files on disk, and for files in memory (used for deflated files, a form of compression).

The following assumes that a file on disk is being read. The details for other types are essentially the same.

## read\_file() ##
The DicomFileLike object instance is created from the file name passed to read\_file() (filereader.py). From there,  it is passed around to all the functions that need it. First it is used to read the DICOM preamble (if present), then the file meta info (a standard dataset for all DICOM files, with an explicit length) (function read\_dataset()). Then the actual dataset is read (read\_dataset() again, but with unknown length).

## read\_dataset() ##
DICOM datasets are composed of DICOM data elements. Thus the function read\_dataset() essentially just calls read\_data\_element() until there are no more (either by known length, by reaching a delimiter tag, or end of file).

## read\_data\_element() ##
read\_data\_element() first reads the DICOM tag, value representation (VR), and length of the data element. The last part of the data element is the value, and this is where the meat of the problem is. pydicom calls different readers for different kinds of values: which one to call is determined from a dictionary mapping the VR to readers. Most VRs map to one of a few distinct readers -- one for number values (binary numbers), one for single string values, and one for multiple-string values (can have multiple values separated by backslash). There are some other readers for special kinds of values. The number reader is also passed a string representing the type to read -- float, long, short, etc.

The read-in values for tag, VR and value are packaged together into a DataElement instance (dataelem.py). Dataelement.value is handled as a python property, so setting the value triggers the `_setvalue` method, which converts values to python types (through `_convert` and `_convert_value` functions). For example, DICOM  "string" numbers (like IS, DS) are converted into proper numeric variables in python, and UI types are converted to a UID class instance (UID.py).

## read\_sequence(), read\_sequence\_item() ##
Some data elements can be a Sequence type (VR of "SQ"). In DICOM files, a sequence is a list of datasets. So read\_sequence() calls read\_sequence\_item(), which, after dealing with sequence delimiters, calls read\_dataset() for each item. Any of these datasets could contain another sequence, so there is a recursion relationship.

## Dataset ##
All of the data elements read are collected into a Dataset instance (dataset.py). Dataset is a class derived from python's dict. By doing so, pydicom takes advantage of this familiar and sophisticated data structure. A dict maps unique keys to values. This is a natural fit for DICOM, which maps unique tags to data elements. So pydicom stores the DICOM tag as the key, and the DataElement instance as the value. pydicom could have just stored the data element value itself, but storing a DataElement instance allows us to also store the original VR, and helpful information (for debugging etc) like the file position at which the item was read.

So far, that allows access to items for a Dataset ds using the tag number:
```
>>> data_el = ds[0x00100010]
>>> type(data_el)
<class 'dicom.dataelem.DataElement'>
>>> data_el.VR
'PN'
>>> data_el.name
"Patient's Name"
>>> data_el.value
"Smith^John"
```

However, pydicom adds "magic" to provide another, simpler (for human readers) syntax. We rarely want anything other than the data element's value, and we would rather access it by name than by tag number, so pydicom provides access such as:
```
>>> ds.PatientsName
"Smith^John"
```

This is done by having `__getattr__` and `__setattr__` "magic methods" for the Dataset class (dataset.py). These intercept any attempt to get or set by name, and check whether that name corresponds to a DICOM tag. If so, the corresponding dictionary entry is returned or set.

# The Road Not Traveled -- Design Decisions #

pydicom could have allowed access by name in a number of different ways:

NOT pydicom! --    ds["Patient's Name"]   OR   ds["PatientsName"]  OR ds.get\_value("Patient's Name")

But the method actually chosen has the simplest syntax, acting as if the name were a member of the dataset instance. The single dot is a lot less obtrusive than the brackets or a whole function name, particularly when nested items are called, e.g.: `ds.Beams[0].ControlPoints[0].BLDPositions[1].LeafJawPositions` is long enough without _any_ extra brackets or other unnecessary cruft.

The dot access is consistent with using dir() to see what items are available. This is also useful for auto-completion used in editing environments, Ipython, etc.

Why not use only names? Why also allow access by tag number? The quick answer is that there might not always _be_ a name -- for example with private tags the "name" may only be known to the vendor. Another example: in future DICOM standards new dictionaries may have items that pydicom doesn't know about yet. Making tag numbers the fundamental storage mechanism also leaves open the possibility of non-English names for speakers of other languages.

Why not actually created members? pydicom could have done something equivalent to `ds.PatientsName = ds[0x00100010].value` for each item after the file was read in. In this case there wouldn't be any "magic" methods needed. The value would be stored as a real python member of the object. Why not do this instead of the magic methods `__getattr__` etc? Problem is, having data in two places means you have to be _very_ careful to make sure any change to one is replicated to the other. So every time a value was set by either method, it would have to be copied to the other. If it was ever missed, this would lead to very strange bugs in user code. It just made sense to have a single copy of the data. A few magic method definitions would handle pointing to the value when necessary, with no risk of the two getting out of sync.