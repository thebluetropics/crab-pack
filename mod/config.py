import tomllib
import shutil
import os

from sys import (exit, stderr)
from json import load as load_json
from pathlib import Path

root_dir = str(Path(__file__).parent.parent.resolve(True))

def path(*path):
	return os.path.abspath(os.path.join(root_dir, *path))

is_debug = True

if os.path.exists(path('opts.json')):
	with open(path('opts.json'), 'r', encoding='utf-8') as file:
		opts = load_json(file)

		if 'is_debug' in opts and type(opts['is_debug']) is bool:
			is_debug = opts['is_debug']
		else:
			print('Err: unknown.', file=stderr)
			exit(1)

_ver = None

if not os.path.isfile(os.path.join(root_dir, 'mod.toml')):
	exit(1)

with open(os.path.join(root_dir, 'mod.toml'), 'rb') as file:
	_ver = tomllib.load(file)['mod']['version']

def get_version():
	return _ver

_features = []

if not os.path.exists(path('config')):
	os.makedirs(path('config'), exist_ok=True)

if not os.path.exists(path('config/features.toml')):
	shutil.copy(path('etc/config_template/features.toml'), path('config/features.toml'))

with open(os.path.join(root_dir, 'config', 'features.toml'), 'rb') as file:
	toml = tomllib.load(file)

	if 'features' in toml and type(toml['features']) is dict:
		for k, v in toml['features'].items():
			if type(v) is bool:
				if v: _features.append(k)
			else:
				print('Err: unknown.', file=stderr)
				exit(1)
	else:
		print('Err: unknown.', file=stderr)
		exit(1)

def is_feature_enabled(feature):
	return feature in _features
