import sys
import mod

from sys import exit, stderr
from . import config, packaging, staging, patch, artifacts

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

	if arg[0].__eq__('-') and arg[1:] in ['v', 'q', 'i', 'no_debug']:
		flags.append(arg[1:])
	else:
		args.append(arg)

if opt_name:
	print('Err: invalid args.', file=stderr)
	exit(1)

config.initialize(flags)
mod.version = config.get_version()

if 'v' in flags:
	if args or opts:
		print('Err: unknown.', file=stderr)
		exit(1)

	print(mod.version)
	exit()

if args[0].__eq__('package_client'):
	packaging.package('client')
	exit(0)

if args[0].__eq__('package_server'):
	packaging.package('client')
	exit(0)

if args[0].__eq__('make_client'):
	artifacts.ensure('b1.7.3', 'client')
	staging.stage('client')
	patch.apply_client_patches()
	packaging.package('client')
	exit(0)

if args[0].__eq__('make_server'):
	artifacts.ensure('b1.7.3', 'server')
	staging.stage('server')
	patch.apply_server_patches()
	packaging.package('server')
	exit(0)

if args[0].__eq__('make'):
	artifacts.ensure('b1.7.3', 'client')
	staging.stage('client')
	patch.apply_client_patches()
	packaging.package('client')
	artifacts.ensure('b1.7.3', 'server')
	staging.stage('server')
	patch.apply_server_patches()
	packaging.package('server')
	exit(0)
