import tomllib, configparser
import shutil
import os

from sys import (exit, stderr)
from pathlib import Path

import json
from json import load as load_json

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

if not os.path.isfile(os.path.join(root_dir, 'mod.json')):
	print('Err: unknown.', file=stderr)
	exit(1)

with open(os.path.join(root_dir, 'mod.json'), 'r', encoding='utf-8') as file:
	mod_info = load_json(file)
	_ver = mod_info['version']

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

if not os.path.exists(path('config', 'features.json')):
	shutil.copy(path('etc', 'config_template', 'features.json'), path('config', 'features.json'))

with open(os.path.join(root_dir, 'config', 'features.json'), 'r', encoding='utf-8') as file:
	file = json.load(file)

	for feature in file['enabled_features']:
		_features.append(feature)

def is_one_of_features_enabled(features):
	for x in features:
		if x in _features:
			return True

	return False

def is_feature_enabled(feature):
	return feature in _features
