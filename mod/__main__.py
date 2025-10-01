import sys
import mod

from sys import (exit, stderr)
from . import (packaging, staging, patch, artifacts)

args = []
flags = []

opts = {}
opt_name = None

for arg in sys.argv[1:len(sys.argv)]:
	if opt_name:
		opts[opt_name] = arg
		opt_name = None
		continue

	if arg[0].__eq__('-') and arg[1:] in []:
		opt_name = arg[1:]
		continue

	if arg[0].__eq__('-') and arg[1:] in ['v', 'q', 'i']:
		flags.append(arg[1:])
	else:
		args.append(arg)

if opt_name:
	print('Err: invalid args.', file=stderr)
	exit(1)

if 'v' in flags:
	if args or opts:
		print('Err: unknown.', file=stderr)
		exit(1)

	print(mod.version)
	exit()

if args[0].__eq__('make_client'):
	artifacts.fetch_if_not_exists('b1.7.3', 'client')
	staging.stage('client')
	patch.apply_client_patches()
	packaging.package('client')
	exit(0)

if args[0].__eq__('make_server'):
	artifacts.fetch_if_not_exists('b1.7.3', 'server')
	staging.stage('server')
	patch.apply_server_patches()
	packaging.package('server')
	exit(0)

if args[0].__eq__('make'):
	artifacts.fetch_if_not_exists('b1.7.3', 'client')
	artifacts.fetch_if_not_exists('b1.7.3', 'server')
	staging.stage('client')
	staging.stage('server')
	patch.apply_client_patches()
	patch.apply_server_patches()
	packaging.package('client')
	packaging.package('server')
	exit(0)
