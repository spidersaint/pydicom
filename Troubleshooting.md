# Debugging #
pydicom uses the python logging package to create a lot of information, but this information is not normally shown. You can turn on the debugging information with the following lines:
```
import dicom
dicom.debug()
```
Turn it off again with `dicom.debug(False)`.

When debug logging is turned on, pydicom will print information as it reads each data element, including the address in the file for the start of each attribute. So if an exception is raised you can follow the lines and see exactly where things started to go wrong.
```
>>> ds=dicom.read_file("MR_small.dcm") # with debug mode on
Reading file '<open file 'MR_small.dcm', mode 'rb' at 0x010336B8>'
Reading preamble
0084: (0002, 0000) File Meta Information Group Length  UL: 190
0090: (0002, 0001) File Meta Information Version       OB: '\x00\x01'
009e: (0002, 0002) Media Storage SOP Class UID         UI: MR Image Storage
00c0: (0002, 0003) Media Storage SOP Instance UID      UI: 1.3.6.1.4.1.5962.1.1.4.1.1.20040826185059.5457
00f6: (0002, 0010) Transfer Syntax UID                 UI: Explicit VR Little Endian
...
```
This is almost identical to the string representation of a dataset (aside from the file address added at the start of each line) but nested items (sequences and sub-sequences, etc) will not be indented, and extra items like sequence delimiters will be shown.

# Hex dump #
Knowing the address of the trouble spot, you can either use a hex editor (On Windows I like Notepad++ and it's hex editor plugin), or pydicom has a hex dump module:
```
>>> from dicom.util.dump import filedump
>>> print filedump("MR_small.dcm", 0x00c0, 0x00f0)
00c0 : 02 00 03 00 55 49 2e 00 31 2e 33 2e 36 2e 31 2e  ....UI..1.3.6.1.
00d0 : 34 2e 31 2e 35 39 36 32 2e 31 2e 31 2e 34 2e 31  4.1.5962.1.1.4.1
00e0 : 2e 31 2e 32 30 30 34 30 38 32 36 31 38 35 30 35  .1.2004082618505
00f0 : 39 2e 35 34 35 37 02 00 10 00 55 49 14 00 31 2e  9.5457....UI..1.
```
filedump takes optional start and stop addresses.

Sometime the dumps can be quite large, so the dump script can also be used from a command line, and the output redirected to a file for viewing in a text editor:
```
C:\python25\lib\site-packages\dicom\test>python ..\util\dump.py MR_small.dcm > MR_small.dump
```

# Submitting Issues #
If you find a file that pydicom cannot read, please [enter an issue](http://code.google.com/p/pydicom/issues/entry) at the googlecode hosting site. If possible (i.e. the file can be publicly released), provide a link to or attach the DICOM file. If not, please use the techniques shown above to submit a debug of the read\_file call, and a hex dump of the area that failed, with any private information edited out.