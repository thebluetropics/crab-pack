import zipfile
import os
import mod

from sys import (exit, stderr)

def package(side):
	if not side in ('client', 'server'):
		print('Err: failed to package.', file=stderr)
		exit(1)

	if not os.path.exists(mod.config.path('dist')):
		os.mkdir(mod.config.path('dist'))

	for file_name in os.listdir(mod.config.path('dist')):
		if side in file_name:
			os.remove(mod.config.path('dist', file_name))
			break

	with zipfile.ZipFile(mod.config.path('dist', f'crabpack-{mod.version}-{side}.jar'), 'w', zipfile.ZIP_DEFLATED) as zipf:
		for root, _, files in os.walk(mod.config.path('stage', side)):
			for file in files:
				absolute_file_path = os.path.join(root, file)
				rel_path = os.path.relpath(absolute_file_path, start=mod.config.path('stage', side))
				zipf.write(absolute_file_path, arcname=rel_path)
