# Contributing to pydicom #

Every open source project reaches a stage where, in order to thrive, it needs more developers and contributors.
I released pydicom hoping others would find it useful, and there has been much more interest than I had anticipated. It was my first open source project, so I'm learning as I go. And a next step should be to open it up for more people to get involved. By doing so it has a much better chance of staying actively maintained and not becoming obsolete over time. Plus all users can benefit from others' fixes, enhancements, or example code.

Below are listed some starter ideas for those interested in contributing. Of course, you could also clone the repository and work on some major changes if you are so inclined.

## Ways to start contributing: ##
  * contribute programs that _use_ pydicom to do something useful. These will go in the `contrib` directory.
  * issue fixes -- work on an "easy" or "medium" item (I've labelled them) on the [issues list](http://code.google.com/p/pydicom/issues) and supply a patch.
  * DICOM files -- DICOM file types that are not already represented are welcome, particularly any that illustrate bugs in the code. See more details in the section below.
  * documentation -- if you find anything lacking in the documentation, point it out. Even better, write something and submit it.

## Contributing DICOM files ##
  * Contributed files must not contain any confidential information of any kind. This of course includes patient information, but you should also consider other items -- see [this discussion](http://groups.google.com/group/pydicom/browse_thread/thread/4d58cdfddbacb688/58c711de0a19f4e1) for more ideas about this.
  * the testfiles directory is distributed with the code, so files there must be quite small (preferably image size has been greatly reduced)
  * there isn't a home yet for big files, but perhaps we can collect some and figure out where to put them later, especially if there are ones that illustrate problems with the code

## How to submit a contribution ##
  * for an item on the issues list, edit the issue, describe your changes in the comment box, and give instructions on where to find the repository clone that the changes can be pulled from
  * similary, to contribute a (small) DICOM file, edit [issue 5](http://code.google.com/p/pydicom/issues/detail?id=5) and attach the file.
  * for big DICOM files, contact me directly (darcymason .at. gmail.com) and we'll work out a way to transfer them

## License of Contributions ##
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in pydicom becomes part of the pydicom project and shall be under the terms and conditions of the [pydicom license](http://code.google.com/p/pydicom/source/browse/source/dicom/license.txt).