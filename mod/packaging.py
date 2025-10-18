import zipfile
import os
import mod

from sys import (exit, stderr)

def package(side):
	if side not in ('client', 'server'):
		print('Err: failed to package.', file=stderr)
		exit(1)

	dist = mod.config.path('dist')
	stage = mod.config.path('stage', side)

	out_name = f'crabpack-{mod.version}-{side}.jar'
	out_path = os.path.join(dist, out_name)

	os.makedirs(dist, exist_ok=True)

	for file_name in os.listdir(dist):
		if side in file_name:
			os.remove(os.path.join(dist, file_name))
			break

	all_files = []
	for root, _, files in os.walk(stage):
		for file in files:
			all_files.append(os.path.join(root, file))

	if not all_files:
		exit(1)

	total = len(all_files)

	bar_width = 20

	with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
		for i, absolute_file_path in enumerate(all_files, 1):
			relative_path = os.path.relpath(absolute_file_path, start=stage)
			zip_file.write(absolute_file_path, arcname=relative_path)

			progress = i / total
			filled = int(bar_width * progress)
			bar = '█' * filled + '▁' * (bar_width - filled)
			print(f'\rPackaging {out_name} {bar} {i}/{total} {progress * 100:5.1f}%', end='', flush=True)
