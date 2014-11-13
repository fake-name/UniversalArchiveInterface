UniversalArchiveInterface
=========================

API wrapper to allow seamless opening of many different compressed archive file
types from python with a consistent API.

Python has libraries for a wide variety of archives:
 - `*.zip` via `zipfile` (prepacked with python)
 - `*.rar` via `rarfile`
 - `*.7z` via `pylzma`

All of these libraries support a "zipfile like" interface. However, **none**
of them have a "zipfile *compatible*" interface. They all have just enough
bizarre quirks that code that is written for one will not work with another.

This library is intended to wrap all of these libraries, and present a
completely consistent interface, so the higher-level code does not have to care
what type of archive it's interfacing.

This was an outgrowth of my [MangaCMS](https://github.com/fake-name/MangaCMS/)
project, that I decided was sufficently generally useful on it's own
to warrant separate packaging.



API
---

Currently, the API is very simple, and only supports reading archive contents:

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
for fileName, fileContents in arch:
    print("filename '%s', filesize %s" % (fileName, len(fileContents)))

```

Lastly, there is also a `arch.close()` method, for manually closing and freeing
the open file-handles, though the destructor generally can handle this
automatically.

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


License:
BSD


