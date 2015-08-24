# Introduction #

pydicom uses a Mercurial repository to do version tracking of code changes. Periodically, a particular revision is packaged into a Windows installer or source code tarball. However, the latest changes are in the repository -- bug fixes and new features that you could benefit from having.

Before checking in a new revision, a standard suite of tests is run to ensure the new code isn't "broken". There isn't much more testing done for the packaged versions, so you don't have anything to lose by going straight to the latest revision. And you can go back to a previous revision of the code if the latest one is causing troubles for you.

The starting point for Mercurial information is http://mercurial.selenic.com/. For Windows, your best bet might be TortoiseHG (http://bitbucket.org/tortoisehg/stable).

Below is a brief summary. For more details see the documentation for Mercurial or TortoiseHG, or the on-line book (http://hgbook.red-bean.com/)

  * Clone the repository (hg clone http://pydicom.googlecode.com/hg) to a folder on your local disk. Alternatively, you can create a user-clone online (http://code.google.com/p/pydicom/source/clones).
  * for the local clone, point python to the code:
    * Create a new file in a text editor. In it, put the following single line:
```
  c:\pydicom\source
```
> Alter the 'c:\pydicom' to whatever folder name you used above.
  * save the file as pydicom.pth (or any name ending in .pth) in c:\python25\lib\site-packages (or wherever site-packages is on your python version). Then when you type "import dicom", python will look at that location for a subdirectory called "dicom" and will find it and be able to import it.
  * to get the latest updates, cd to the local directory and type hg pull