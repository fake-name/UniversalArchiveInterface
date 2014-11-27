#!/usr/bin/python
# -*- coding: utf-8 -*-

import magic
import zlib

import zipfile
import rarfile
import tempfile
import io

import logging
import traceback
import py7zlib
import contextlib

class ArchiveError(Exception):
	pass

class CorruptArchive(ArchiveError):
	pass

class NotAnArchive(ArchiveError):
	pass
logPath = "Main.ArchTool"
logger = logging.getLogger(logPath)

# Decorator that catches errors, does some logging, and then re-raises the error.
def logErrors(func):
	def caughtFunc(self, *args, **kwargs):
		try:
			return func(self, *args, **kwargs)

		except TypeError:
			logger.error("Empty Archive Directory? Path = %s", self.archPath)
			raise

		except CorruptArchive:
			logger.error("Corrupt Archive: ")
			logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				logger.error("%s", tbLine)
			raise
		except NotAnArchive:
			logger.error("File is not an archive: ")
			logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				logger.error("%s", tbLine)
			raise

		except rarfile.PasswordRequired:
			logger.error("Archive password protected: ")
			logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				logger.error("%s", tbLine)
			raise


		except zlib.error:
			logger.error("Archive password protected: ")
			logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				logger.error("%s", tbLine)
			raise

		except (KeyboardInterrupt, SystemExit, GeneratorExit):
			raise

		except:
			logger.error("Unknown error in archive iterator: ")
			logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				logger.error("%s", tbLine)
			raise
	return caughtFunc


class ArchiveReader(object):

	fp = None

	@logErrors
	def __init__(self, archPath=None, fileContents=None):

		self.archPath = archPath

		self.tempfile = None

		if archPath:
			self.fType = magic.from_file(archPath, mime=True).decode("ascii")
		elif fileContents:
			self.fType = magic.from_buffer(fileContents, mime=True).decode("ascii")
		else:
			raise ValueError("You must pass either an archive file path or the contents of an\
				archive to the constructor!")

		if self.fType == 'application/x-rar':
			if fileContents:
				# Because rar is a shitty proprietary compression format,
				# it can't be used in normal libraries, and the legal
				# libraries only operate on real files. Therefore,
				# create a temp-file.
				self.tempfile = tempfile.NamedTemporaryFile()
				self.tempfile.write(fileContents)
				self.tempfile.flush()
				self.archPath = self.tempfile.name
			self.archHandle = rarfile.RarFile(self.archPath) # self._iterRarFiles()
			self.archType = "rar"
		elif self.fType == 'application/zip':
			try:
				if fileContents:  # Use pre-read fileContents whenever possible.
					self.archHandle = zipfile.ZipFile(io.BytesIO(fileContents))
				else:
					self.archHandle = zipfile.ZipFile(self.archPath) # self._iterZipFiles()

				self.archType = "zip"
			except zipfile.BadZipfile:
				raise CorruptArchive("File is not a valid zip archive!")

		elif self.fType == 'application/x-7z-compressed':
			try:
				if fileContents:  # Use pre-read fileContents whenever possible.
					self.archHandle = py7zlib.Archive7z(io.BytesIO(fileContents))
				else:
					self.fp = open(archPath, "rb")
					self.archHandle = py7zlib.Archive7z(self.fp) # self._iterZipFiles()

				self.archType = "7z"

			except py7zlib.ArchiveError:
				raise CorruptArchive("File is not a valid 7z archive!")
		else:
			raise NotAnArchive("Tried to create ArchiveReader on a non-archive file! File type: '%s'" % self.fType)

	def __del__(self):
		# If we had to create a temp-file, close it, so it'll be deleted.
		if self.tempfile:
			self.tempfile.close()

		# something somewhere isn't closing properly, making shit leak all over the place (I think?)
		# Anyways, try to close all the things manually
		try:
			self.close()
		except Exception:
			pass

	@staticmethod
	def isArchive(filepath):
		fType = magic.from_file(filepath, mime=True).decode("ascii")
		return fType in ['application/x-rar', 'application/zip', 'application/x-7z-compressed']

	@staticmethod
	def bufferIsArchive(buffer):
		fType = magic.from_buffer(buffer, mime=True).decode("ascii")
		return fType in ['application/x-rar', 'application/zip', 'application/x-7z-compressed']


	@logErrors
	def getFileList(self):
		if self.archType == "rar":
			for item in self._getRarFileList():
				yield item
		elif self.archType == "zip":
			for item in self._getZipFileList():
				yield item
		elif self.archType == "7z":
			for item in self._get7zFileList():
				yield item
		else:
			raise ValueError("Not a known archive type. Wat")


	# Close an open archive.
	def close(self):
		# 7z files don't maintain their own file pointers
		if self.archType != "7z":
			self.archHandle.close()

		if self.fp:
			self.fp.close()

	# Open internal path `internalPath`, return a file-like object.
	@logErrors
	def open(self, internalPath):
		if self.archType == '7z':
			return self.archHandle.getmember(internalPath)
		else:
			return self.archHandle.open(internalPath)

	# Return the file contents of item at path `internalPath` as a
	# Binary string.
	@logErrors
	def read(self, internalPath):
		if self.archType == '7z':
			fp = self.archHandle.getmember(internalPath)
			content = fp.read()

			# It returns a file-like object, but it doesn't' have a
			# close() method. Wat?
			del fp
			return content
		else:
			return self.archHandle.read(internalPath)

	def __iter__(self):
		if self.archType == "rar":
			for item in self._iterRarFiles():
				yield item
		elif self.archType == "zip":
			for item in self._iterZipFiles():
				yield item
		elif self.archType == "7z":
			for item in self._iter7zFiles():
				yield item
		else:
			raise ValueError("Not a known archive type. Wat")

	@logErrors
	def _iter7zFiles(self):
		names = self._get7zFileList()
		for name in names:
			tempFp = self.archHandle.getmember(name)
			yield name, tempFp

	@logErrors
	def _iterZipFiles(self):
		names = self._getZipFileList()
		for name in names:
			with self.archHandle.open(name) as tempFp:
				yield name, tempFp

	# Exceptions here aren't being caught in the `@logErrors` decorator properly
	# Not sure why, yet.
	@logErrors
	def _iterRarFiles(self):
		names = self._getRarFileList()
		for name in names:
			try:
				with self.archHandle.open(name) as tempFp:
					name = name.replace("\\", "/")

					# Because rarfile does no checking until we
					# actually read the file, read the file into
					# a temporary buffer, and yield that
					tempFp = io.BytesIO(tempFp.read())
					yield name, tempFp
			except rarfile.BadRarFile:
				raise CorruptArchive("Corrupt Rar archive!")

	@logErrors
	def _getZipFileList(self):
		names = self.archHandle.namelist()

		# Sometimes, the namelist *somehow* returns the same file
		# TWICE. No idea what the fuck is going on, it led to some
		# VERY confusing bugs. Anyways, use a set to prevent dupes.
		ret = set()
		for name in names:
			if not name.endswith("/"):
				ret.add(name)

		ret = list(ret)
		ret.sort()
		return ret

	@logErrors
	def _getRarFileList(self):
		names = self.archHandle.namelist()
		ret = []
		for name in names:
			if not self.archHandle.getinfo(name).isdir():
				ret.append(name)

		return ret

	@logErrors
	def _get7zFileList(self):
		names = self.archHandle.getnames()
		return names

