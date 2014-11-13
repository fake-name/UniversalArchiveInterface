
import setuptools
from distutils.core import setup
import sys
setup(
	# Application name:
	name="UniversalArchiveInterface",

	# Version number (initial):
	version="0.0.1",

	# Application author details:
	author="Connor Wolf	",
	author_email="github@imaginaryindustries.com",

	# Packages
	packages=["UniversalArchiveInterface"],

	# Details
	url="https://github.com/fake-name/UniversalArchiveInterface",

	#
	# license="LICENSE.txt",
	description="Multi-archive-format API wrapper.",

	long_description=open("README.md").read(),

	# Dependent packages (distributions)
	install_requires=[
		"python-magic",
		"rarfile",
		"pylzma"
	],
)
