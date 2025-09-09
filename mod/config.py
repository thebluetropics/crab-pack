import tomllib, configparser
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

if not os.path.exists(path('config/features.conf')):
	shutil.copy(path('etc/config_template/features.conf'), path('config/features.conf'))

with open(os.path.join(root_dir, 'config', 'features.conf'), 'r') as file:
	conf = configparser.ConfigParser(delimiters=(':',))
	conf.read_file(file)

	for sec in conf.sections():
		for k, v in conf[sec].items():
			if v.__eq__('enabled'):
				_features.append(f'{sec}.{k}')

def is_feature_enabled(feature):
	return feature in _features
