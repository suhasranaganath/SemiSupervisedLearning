import os, sys
from pathlib import Path, PurePosixPath

from lib_utils import projconfig
from lib_utils import nltkconfig

if __name__ == '__main__':
	reporoot = projconfig.getRepoRoot()
	print(f"{reporoot=}")
	datafolder = projconfig.getDataFolder()
	print(f"{datafolder=}")
	print(nltkconfig.getDataFolder())
