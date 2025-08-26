import sys
import mod

from sys import (exit, stderr)
from operator import eq
from . import (packaging, staging, patch, artifacts)

if not len(sys.argv).__eq__(2):
	exit(1)

_, mode = sys.argv

if mode.__eq__("version"):
	print(mod.version)
	exit()

if not mode in (
	"stage_client",
	"stage_server",
	"patch_client",
	"patch_server"
	"package_client",
	"package_server",
	"make_client",
	"make_server",
	"make"
):
	print("Err: unsupported mode of operation.", file=stderr)
	exit(1)

if eq(mode, "stage_client"):
	artifacts.fetch_if_not_exists("b1.7.3", "client")
	staging.stage("client")
	exit(0)

if eq(mode, "stage_server"):
	artifacts.fetch_if_not_exists("b1.7.3", "server")
	staging.stage("server")
	exit(0)

if eq(mode, "patch_client"):
	patch.apply_client_patches()
	exit(0)

if eq(mode, "patch_server"):
	patch.apply_server_patches()
	exit(0)

if eq(mode, "package_client"):
	packaging.package("client")
	exit(0)

if eq(mode, "package_server"):
	packaging.package("server")
	exit(0)

if eq(mode, "make_client"):
	artifacts.fetch_if_not_exists("b1.7.3", "client")
	staging.stage("client")
	patch.apply_client_patches()
	packaging.package("client")
	exit(0)

if eq(mode, "make_server"):
	artifacts.fetch_if_not_exists("b1.7.3", "server")
	staging.stage("server")
	patch.apply_server_patches()
	packaging.package("server")
	exit(0)

if eq(mode, "make"):
	artifacts.fetch_if_not_exists("b1.7.3", "client")
	artifacts.fetch_if_not_exists("b1.7.3", "server")
	staging.stage("client")
	staging.stage("server")
	patch.apply_client_patches()
	patch.apply_server_patches()
	packaging.package("client")
	packaging.package("server")
	exit(0)
