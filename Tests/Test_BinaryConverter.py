
import unittest



import UniversalArchiveInterface as uai


TEST_PATH_ZIP       = './Tests/testfiles/test_good.zip'
TEST_PATH_7Z        = './Tests/testfiles/test_good.7z'

TEST_PATH_BAD_ZIP   = './Tests/testfiles/test_bad.zip'
TEST_PATH_BAD_7Z    = './Tests/testfiles/test_bad.7z'


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


	# Verify the corrupt archives are really corrupt
	def test_bad_zip_fpath(self):
		fpath = TEST_PATH_BAD_ZIP
		self.assertRaises(ValueError, uai.ArchiveReader, archPath=fpath)

	def test_bad_zip_fcont(self):
		with open(TEST_PATH_BAD_ZIP, "rb") as fp:
			zcont = fp.read()
		self.assertRaises(ValueError, uai.ArchiveReader, fileContents=zcont)

	def test_bad_7z_fpath(self):
		fpath = TEST_PATH_BAD_7Z
		self.assertRaises(ValueError, uai.ArchiveReader, archPath=fpath)

	def test_bad_7z_fcont(self):
		with open(TEST_PATH_BAD_7Z, "rb") as fp:
			zcont = fp.read()
		self.assertRaises(ValueError, uai.ArchiveReader, fileContents=zcont)

