UniversalArchiveInterface  [![Build Status](https://travis-ci.org/fake-name/UniversalArchiveInterface.svg?branch=master)](https://travis-ci.org/fake-name/UniversalArchiveInterface)
=========================

API wrapper to allow seamless opening of many different compressed archive file
types from python with a consistent API.

Tested on python 2.7 and Python 3.4.

Python has libraries for a wide variety of archives:  

 - `*.zip` via `zipfile` (prepacked with python)
 - `*.rar` via `rarfile`
 - `*.7z` via `pylzma`

All of these libraries support a "zipfile like" interface. However, **none**
of them have a "zipfile *compatible*" interface (well, excepting `zipfile` 
itself). They all have just enough bizarre quirks that code that is written for 
one will not work with another.

This library is intended to wrap all of these libraries, and present a
completely consistent interface, so the higher-level code does not have to care
what type of archive it's interfacing.

This was an outgrowth of my [MangaCMS](https://github.com/fake-name/MangaCMS/)
project, that I decided was sufficently generally useful on it's own
to warrant separate packaging.

Additional dependencies:
`python-magic` - For determining file-types.


API
---

Currently, the API is very simple, and only supports reading archive contents:
This will *probably* not change, due to the legal difficulties involved in
modifying `*.rar` files (the `.rar` file format is proprietary, and anything
other then decompressing them arguably requires a WinRar license. The
decompression code has been freely released.).

```
>>> import UniversalArchiveInterface as uar
>>> arch = uar.ArchiveReader(archPath='/path/to/archive.zip')
(or)
>>> arch = uar.ArchiveReader(fileContents={archive-contents-buffer})
```

The `ArchiveReader` class supports only a few methods:

```

>>> arch.getFileList()
['dir1/file1', 'dir1/file2', 'dir2/file3', 'file4']

>>> arch.open('dir1/file1')
<buffer object>

>>> arch.read('dir1/file1')
<file-contents>

```

The `ArchiveReader` class is also iterable:

```
for fileName, fileHandle in arch:
    print("filename '%s', filesize %s" % (fileName, len(fileHandle.read())))

```

Lastly, there is also a `arch.close()` method, for manually closing and freeing
the open file-handles, though the destructor generally can handle this
automatically.


The `ArchiveReader` class also provides two `staticMethods`:

 - `ArchiveReader.isArchive(filepath):`
 - `ArchiveReader.bufferIsArchive(buffer):`

Both return `True` if the passed path/buffer-contents is an archive the
library can handle, and false otherwise.

File type identification is via the `python-magic` library, which does not care
about file-extension.

### Exceptions

All archive-format-specific exceptions are caught, and re-raised as generic
exceptions. UniveralArchiveInterface defines three exceptions:

 - `ArchiveError` - Base exception
	 - `CorruptArchive` - Archive is corrupt
	 - `NotAnArchive` - Passed file is not an archive.

`ArchiveError` is the parent-exception of `CorruptArchive` and `NotAnArchive`. 
`NotAnArchive` is raised when an archiveReader is instantiated on a file or 
buffer that is not actually an archive. `CorruptArchive` is raised when an 
archiveReader is instantiated on or access a corrupt archive.

Note that `CorruptArchive` can potentially be raised in multiple circumstances: 
when the archiveReader is instantiated, when the file-listing is generated, or 
when a file is actually accessed. 

---

Notes:

`getFileList()` will only ever return valid archive-internal file-paths. This
was one of the major problem sources that initially led to this libraries'
creation: `rarfile` returns both files and directories when used as an
iterable, while `zipfile` does not. The `rarfile` library also returns paths
with double-back-slashes (`\\`) instead of single forward slashes (`/`) for
path separators, though it accepts and works fine with forward-slash delimiters.
Therefore, the iterator internally replaces all double-backslashes in `rarfile`
internal paths with forward-slashes.


TODO:
Better test coverage. Right now, it's about 60% covered.
Most of the not-covered parts are the rar handling (I can't create test-rars easily:
rar is a proprietary format, and 7zip can't create them), and exception handling.
Almost all exceptions are caught, a logging message is emitted, and then the
exception is re-raised as a single exception type (generally `ValueError`), but
this is currently not well-tested. I need to corrupt some archives and write tests around
those corruped archives.

License:
BSD


