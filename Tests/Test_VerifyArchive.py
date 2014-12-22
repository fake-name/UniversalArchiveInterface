
import unittest

import logging

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)

# logger = logging.getLogger('Main')
# logger.addHandler(ch)


import UniversalArchiveInterface as uai


TEST_PATH_ZIP       = './Tests/testfiles/test_good_L.zip'
TEST_PATH_7Z        = './Tests/testfiles/test_good_L.7z'
TEST_PATH_RAR       = './Tests/testfiles/test_good_L.rar'

TEST_PATH_BAD_ZIP   = './Tests/testfiles/test_bad_L.zip'
TEST_PATH_BAD_7Z    = './Tests/testfiles/test_bad_L.7z'
TEST_PATH_BAD_RAR   = './Tests/testfiles/test_bad_L.rar'

TEST_NOT_AN_ARCH    = './Tests/testfiles/test.txt'


class TestDecompression(unittest.TestCase):

	def test_verifyZip_1(self):

		fpath = TEST_PATH_ZIP

		ar = uai.ArchiveReader(archPath=fpath)
		self.assertTrue(ar.verify())

	def test_verifyRar_1(self):

		fpath = TEST_PATH_RAR

		ar = uai.ArchiveReader(archPath=fpath)
		self.assertTrue(ar.verify())

	def test_verify7z_1(self):

		fpath = TEST_PATH_7Z

		ar = uai.ArchiveReader(archPath=fpath)
		self.assertTrue(ar.verify())


	def test_verifyZip_2(self):

		fpath = TEST_PATH_BAD_ZIP

		ar = uai.ArchiveReader(archPath=fpath)
		self.assertFalse(ar.verify())

	def test_verifyRar_2(self):

		fpath = TEST_PATH_BAD_RAR

		ar = uai.ArchiveReader(archPath=fpath)
		self.assertFalse(ar.verify())

	def test_verify7z_2(self):

		fpath = TEST_PATH_BAD_7Z

		ar = uai.ArchiveReader(archPath=fpath)
		self.assertFalse(ar.verify())
