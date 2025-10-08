import urllib.request
import os
import shutil
import zipfile, sys

from pathlib import Path
from sys import (exit, stderr)

project_dir = str(Path(__file__).parent.parent.resolve(True))

def requires_dir(*segments):
	path = os.path.join(project_dir, *segments)

	if not os.path.exists(path):
		os.makedirs(path, exist_ok=True)

requires_dir('out', 'python-3.13.2')

embeddable_distribution_file = os.path.join(project_dir, 'out', 'python-3.13.2', 'python-3.13.2-embed-amd64.zip')

if not os.path.exists(embeddable_distribution_file):
	with urllib.request.urlopen(f'https://www.python.org/ftp/python/3.13.2/python-3.13.2-embed-amd64.zip', timeout=16) as res:
		with open(embeddable_distribution_file, 'wb') as file:
			file.write(res.read())

requires_dir('out', 'target', 'windows-x86_64')

target_path = os.path.join(project_dir, 'out', 'target', 'windows-x86_64')

if os.listdir(target_path):
	for entry in os.listdir(target_path):
		entry_path = os.path.join(target_path, entry)

		if os.path.isfile(entry_path) or os.path.islink(entry_path):
			os.unlink(entry_path)
		elif os.path.isdir(entry_path):
			shutil.rmtree(entry_path)

if not os.path.exists(os.path.join(target_path, 'python-3.13.2')):
	os.mkdir(os.path.join(target_path, 'python-3.13.2'))

try:
	with zipfile.ZipFile(embeddable_distribution_file, 'r') as zip:
		zip.extractall(os.path.join(target_path, 'python-3.13.2'))
except zipfile.BadZipFile:
	print('Err: unknown.', file=stderr)
	exit(1)

with open(os.path.join(target_path, 'python-3.13.2', 'python313._pth'), 'w', encoding='utf-8') as file:
	file.write(
		'\r\n'.join(['python313.zip', '..', '.'])
	)

shutil.copytree(
	os.path.join(project_dir, 'mod'),
	os.path.join(target_path, 'mod'),
	ignore=shutil.ignore_patterns('__pycache__', '*.pyc')
)
shutil.copytree(
	os.path.join(project_dir, 'modmaker'),
	os.path.join(target_path, 'modmaker'),
	ignore=shutil.ignore_patterns('__pycache__', '*.pyc')
)
shutil.copytree(os.path.join(project_dir, 'assets'), os.path.join(target_path, 'assets'))
shutil.copytree(os.path.join(project_dir, 'class_files'), os.path.join(target_path, 'class_files'))
shutil.copytree(os.path.join(project_dir, 'deps'), os.path.join(target_path, 'deps'))
shutil.copy(os.path.join(project_dir, 'mod.json'), os.path.join(target_path, 'mod.json'))
shutil.copy(os.path.join(project_dir, 'LICENSE'), os.path.join(target_path, 'LICENSE'))

if not os.path.exists(os.path.join(target_path, 'config')):
	os.mkdir(os.path.join(target_path, 'config'))

shutil.copy(os.path.join(project_dir, 'etc', 'config_template', 'features.json'), os.path.join(target_path, 'config', 'features.json'))

with open(os.path.join(target_path, 'make.bat'), 'w', encoding='utf-8') as file:
	file.write(
		'\r\n'.join(['@echo off', '.\\python-3.13.2\\python.exe -m mod -no_debug make'])
	)

if not os.path.exists(os.path.join(target_path, 'lib')):
	os.mkdir(os.path.join(target_path, 'lib'))

shutil.copy(os.path.join(project_dir, 'c_libs', 'assets', 'lib', 'assets.dll'), os.path.join(target_path, 'lib', 'assets.dll'))

requires_dir('dist')

with zipfile.ZipFile(os.path.join(project_dir, 'dist', 'windows-x86_64.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
	for root, _, files in os.walk(target_path):
		for file in files:
			abs_path = os.path.join(root, file)
			rel_path = os.path.relpath(abs_path, target_path)
			zipf.write(abs_path, rel_path)
