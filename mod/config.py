import shutil
import os, json

from sys import (exit, stderr)
from pathlib import Path

project_dir = str(Path(__file__).parent.parent.resolve(True))

def path(*path):
	return os.path.abspath(os.path.join(project_dir, *path))

is_debug = True
_ver = None

def get_version():
	return _ver

_features = []

def is_one_of_features_enabled(features):
	for x in features:
		if x in _features:
			return True

	return False

def is_feature_enabled(feature):
	return feature in _features

def initialize(flags):
	global is_debug, _ver

	if 'no_debug' in flags:
		is_debug = False

	if not os.path.isfile(os.path.join(project_dir, 'mod.json')):
		print('Err: unknown.', file=stderr)
		exit(1)

	with open(os.path.join(project_dir, 'mod.json'), 'r', encoding='utf-8') as file:
		mod_info = json.load(file)
		_ver = mod_info['version']

	if os.path.exists(os.path.join(project_dir, 'config', 'features.json')):
		with open(os.path.join(project_dir, 'config', 'features.json'), 'r', encoding='utf-8') as file:
			file = json.load(file)

			for feature in file['enabled_features']:
				_features.append(feature)
