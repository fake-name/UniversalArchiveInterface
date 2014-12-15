
import unittest

import logging

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)

# logger = logging.getLogger('Main')
# logger.addHandler(ch)


import UniversalArchiveInterface as uai


TEST_PATH_ZIP       = './Tests/testfiles/test_good.zip'
TEST_PATH_7Z        = './Tests/testfiles/test_good.7z'
TEST_PATH_RAR       = './Tests/testfiles/test_good.rar'

TEST_PATH_BAD_ZIP   = './Tests/testfiles/test_bad.zip'
TEST_PATH_BAD_7Z    = './Tests/testfiles/test_bad.7z'
TEST_PATH_BAD_RAR   = './Tests/testfiles/test_bad.rar'

TEST_NOT_AN_ARCH    = './Tests/testfiles/test.txt'


class TestDecompression(unittest.TestCase):


	def verify_archive(self, arch):

		files = list(arch.getFileList())
		self.assertEqual(['test.txt'], files)

		fcont = arch.read('test.txt')
		self.assertEqual(fcont, b'test ok')

		fhandle = arch.open('test.txt')
		self.assertEqual(fhandle.read(), b'test ok')

		for fName, fCont in arch:
			self.assertEqual((fName, fCont.read()), ('test.txt', b'test ok'))


	def test_zip_fpath(self):
		fpath = TEST_PATH_ZIP
		arch = uai.ArchiveReader(archPath=fpath)
		self.verify_archive(arch)

		arch.close()

	def test_zip_fcont(self):
		with open(TEST_PATH_ZIP, "rb") as fp:
			zcont = fp.read()

		arch = uai.ArchiveReader(fileContents=zcont)
		self.verify_archive(arch)

		arch.close()

	def test_7z_fpath(self):
		fpath = TEST_PATH_7Z
		arch = uai.ArchiveReader(archPath=fpath)
		self.verify_archive(arch)

		arch.close()

	def test_7z_fcont(self):
		with open(TEST_PATH_7Z, "rb") as fp:
			zcont = fp.read()

		arch = uai.ArchiveReader(fileContents=zcont)
		self.verify_archive(arch)

		arch.close()

	def test_rar_fpath(self):
		fpath = TEST_PATH_RAR
		arch = uai.ArchiveReader(archPath=fpath)
		self.verify_archive(arch)

		arch.close()

	def test_rar_fcont(self):
		with open(TEST_PATH_RAR, "rb") as fp:
			zcont = fp.read()

		arch = uai.ArchiveReader(fileContents=zcont)
		self.verify_archive(arch)

		arch.close()


	# Verify the corrupt archives are really corrupt,
	# and we're failing in the correct place (by looking at the raised
	# error message)
	def test_bad_zip_fpath(self):
		fpath = TEST_PATH_BAD_ZIP

		with self.assertRaises(uai.CorruptArchive) as cm:
			uai.ArchiveReader(archPath=fpath)
		self.assertEqual('File is not a valid zip archive!',
							str(cm.exception)
						)

	def test_bad_zip_fcont(self):
		with open(TEST_PATH_BAD_ZIP, "rb") as fp:
			zcont = fp.read()

		with self.assertRaises(uai.CorruptArchive) as cm:
			uai.ArchiveReader(fileContents=zcont)
		self.assertEqual('File is not a valid zip archive!',
							str(cm.exception)
						)

	def test_bad_7z_fpath(self):
		fpath = TEST_PATH_BAD_7Z

		with self.assertRaises(uai.CorruptArchive) as cm:
			uai.ArchiveReader(archPath=fpath)
		self.assertEqual('File is not a valid 7z archive!',
							str(cm.exception)
						)

	def test_bad_7z_fcont(self):
		with open(TEST_PATH_BAD_7Z, "rb") as fp:
			zcont = fp.read()

		with self.assertRaises(uai.CorruptArchive) as cm:
			uai.ArchiveReader(fileContents=zcont)
		self.assertEqual('File is not a valid 7z archive!',
							str(cm.exception)
						)

	def test_bad_rar_fpath(self):
		fpath = TEST_PATH_BAD_RAR

		with self.assertRaises(uai.CorruptArchive) as cm:
			reader = uai.ArchiveReader(archPath=fpath)
			for dummy_1, dummy_2 in reader:
				pass
		self.assertEqual('Corrupt Rar archive!',
							str(cm.exception)
						)

	def test_bad_rar_fcont(self):
		with open(TEST_PATH_BAD_RAR, "rb") as fp:
			zcont = fp.read()

		with self.assertRaises(uai.CorruptArchive) as cm:
			reader = uai.ArchiveReader(fileContents=zcont)
			for dummy_1, dummy_2 in reader:
				pass
		self.assertEqual('Corrupt Rar archive!',
							str(cm.exception)
						)



	def test_not_an_archive_fpath(self):
		fpath = TEST_NOT_AN_ARCH

		with self.assertRaises(uai.NotAnArchive) as cm:
			uai.ArchiveReader(archPath=fpath)
		self.assertEqual("Tried to create ArchiveReader on a non-archive file! File type: 'text/plain'",
							str(cm.exception)
						)

	def test_not_an_archive_fcont(self):
		with open(TEST_NOT_AN_ARCH, "rb") as fp:
			zcont = fp.read()

		with self.assertRaises(uai.NotAnArchive) as cm:
			uai.ArchiveReader(fileContents=zcont)
		self.assertEqual("Tried to create ArchiveReader on a non-archive file! File type: 'text/plain'",
							str(cm.exception)
						)


	def test_is_archive(self):

		self.assertEqual(uai.ArchiveReader.isArchive(TEST_PATH_RAR), True)
		self.assertEqual(uai.ArchiveReader.isArchive(TEST_PATH_ZIP), True)
		self.assertEqual(uai.ArchiveReader.isArchive(TEST_PATH_7Z), True)

		with open(TEST_PATH_RAR, "rb") as fp:
			rcont = fp.read()
		with open(TEST_PATH_ZIP, "rb") as fp:
			zcont = fp.read()
		with open(TEST_PATH_7Z, "rb") as fp:
			scont = fp.read()

		self.assertEqual(uai.ArchiveReader.bufferIsArchive(rcont), True)
		self.assertEqual(uai.ArchiveReader.bufferIsArchive(zcont), True)
		self.assertEqual(uai.ArchiveReader.bufferIsArchive(scont), True)

	def test_is_not_archive(self):
		self.assertEqual(uai.ArchiveReader.isArchive(TEST_NOT_AN_ARCH), False)

		with open(TEST_NOT_AN_ARCH, "rb") as fp:
			ncont = fp.read()

		self.assertEqual(uai.ArchiveReader.bufferIsArchive(ncont), False)


	def test_no_archive(self):

		with self.assertRaises(uai.NotAnArchive) as cm:
			reader = uai.ArchiveReader()

