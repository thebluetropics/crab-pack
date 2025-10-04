import urllib.request
import os
import mod

from sys import exit, stderr

_lookup = [
	{
		'id': ('b1.7.3', 'client'),
		'url': 'https://piston-data.mojang.com/v1/objects/43db9b498cb67058d2e12d394e6507722e71bb45/client.jar',
		'sha256': 'af1fa04b8006d3ef78c7e24f8de4aa56f439a74d7f314827529062d5bab6db4c',
		'size': 1465375
	},
	{
		'id': ('b1.7.3', 'server'),
		'url': 'https://vault.omniarchive.uk/archive/java/server-beta/b1.7/b1.7.3.jar',
		'sha256': '033a127e4a25a60b038f15369c89305a3d53752242a1cff11ae964954e79ba4d',
		'size': 503100
	},
	{
		'id': ('b1.8.1', 'client'),
		'url': 'https://piston-data.mojang.com/v1/objects/6b562463ccc2c7ff12ff350a2b04a67b3adcd37b/client.jar',
		'sha256': '3a61a9cb5b8b6cade30a8bfe21f6793122c7349d0c3bbe1cd0fc2a93add36f4a',
		'size': 1995166
	}
]

def ensure(version, side_name):
	artifacts_dir = mod.config.path('jars')

	if not os.path.exists(artifacts_dir):
		os.mkdir(artifacts_dir)

	file_path = os.path.join(artifacts_dir, f'{version}_{side_name}.jar')

	if not os.path.exists(file_path):
		entry = None

		for e in _lookup:
			if e['id'].__eq__((version, side_name)):
				entry = e

		with urllib.request.urlopen(entry['url'], timeout=30) as response:
			with open(file_path, 'wb') as file:
				file.write(response.read())
