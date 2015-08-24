# Introduction #

Sequences are part of the DICOM standard, but they do complicate the structure of the data. Pydicom tries to make it as easy as possible to work with sequences, but you will still need to have a good understanding of the DICOM structure to navigate them. The PydicomUserGuide wiki page has an object model at the top which outlines the structure of DICOM objects. This is the way DICOM itself lays them out; pydicom has just translated the DICOM model directly into objects in python.

# Reading Sequence data #

This was covered in the PydicomUserGuide. For now, please refer to that page ... more details to be added here at some point.

One note: the examples below are using the new official DICOM keywords (as available in pydicom 0.9.7). The older "English plural" form of sequences has been deprecated.

# Creating a New Sequence #

When it comes to creating sequences, there is one key thing to remember:

---

> A sequence is a **list** of **datasets**.

---

I find it easiest to start at the bottom, so to speak, and create the datasets first, then make a list (Sequence) out of them, then assign that Sequence to the parent dataset.

Here is some code to show a brief example, adding a block sequence (with two items) to the first beam of an rtplan dataset 'plan\_ds':
```
>>> from dicom.sequence import Sequence 
>>> from dicom.dataset import Dataset 

>>> block_ds1 = Dataset() 
>>> block_ds1.BlockType = "APERTURE" 
>>> block_ds1.BlockName = "Block1" 

>>> block_ds2 = Dataset() 
>>> block_ds2.BlockType = "APERTURE" 
>>> block_ds2.BlockName = "Block2" 

>>> beam = Dataset() 
>>> # ... add beam data elements like BeamName, etc; these are skipped in this example
>>> plan_ds = Dataset()    # or read one in from a file, etc
>>> plan_ds.BeamSequence = Sequence([beam]) # starting from scratch here; will already exist if read from file
>>> plan_ds.BeamSequence[0].BlockSequence = Sequence([block_ds1, block_ds2]) 
>>> plan_ds.BeamSequence[0].NumberOfBlocks = 2 
```

(Note that pydicom does not check that the datasets have all the correct items in them -- that's up to you. Likewise for related data elements, like NumberOfBlocks above).

In the above code, plan\_ds.BeamSequence is a Sequence itself. But getting item 0 returns a _dataset_ (a sequence is a list of datasets!). So we can add a new _data element_ to that dataset in the usual way, by referring to it by name ('BlockSequence'). In this case the data element happens to be a Sequence type.

Note the square brackets in the argument to Sequence in the third last line, which creates the python list which is passed to the Sequence to initialize it. You could, of course, have created any python list with general python code, and then passed that list by name to Sequence() instead.

Once the Sequence is initialized, it can still be worked with, just like any python list:
```
>>> beam0 = plan_ds.BeamSequence[0]  # just for less typing
>>> print len(beam0.BlockSequence)
2
>>> block_ds3 = Dataset()  # new Dataset 
>>> # ... add data elements to it as above
>>> beam0.BlockSequence.append(block_ds3) # don't forget to update Number of Blocks data element
```

# Deleting a sequence item #

Deleting a sequence item works the same as with any python list, using python's built-in `del` statement:
```
>>> del plan_ds.BeamSequence[0].BlockSequence[1]
```