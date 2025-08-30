import os
import shutil
import zipfile
import mod

from sys import (exit, stderr)

def stage(side):
	if not side in ('client', 'server'):
		exit(1)

	dir_path = os.path.join(mod.config.root_dir, f'stage/{side}')

	if not os.path.isdir(dir_path):
		os.makedirs(dir_path, exist_ok=True)

	if os.listdir(dir_path):
		for entry in os.listdir(dir_path):
			entry_path = os.path.join(dir_path, entry)

			if os.path.isfile(entry_path) or os.path.islink(entry_path):
				os.unlink(entry_path)
			elif os.path.isdir(entry_path):
				shutil.rmtree(entry_path)

	try:
		with zipfile.ZipFile(os.path.join(mod.config.root_dir, f'artifacts/b1.7.3_{side}.jar'), 'r') as zip:
			zip.extractall(dir_path)
	except zipfile.BadZipFile:
		print('Err: unknown.', file=stderr)
		exit(1)
