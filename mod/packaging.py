import zipfile
import os
import mod

from sys import (exit, stderr)

def package(side):
	if not side in ("client", "server"):
		exit(1)

	if not os.path.exists(mod.config.path("jars")):
		os.mkdir(mod.config.path("jars"))

	for file_name in os.listdir(mod.config.path("jars")):
		if side in file_name:
			os.remove(mod.config.path("jars", file_name))

	with zipfile.ZipFile(mod.config.path("jars", f"crabpack-{mod.version}-{side}.jar"), "w", zipfile.ZIP_DEFLATED) as zipf:
		for root, _, files in os.walk(mod.config.path(f"stage/{side}")):
			for file in files:
				absolute_file_path = os.path.join(root, file)
				rel_path = os.path.relpath(absolute_file_path, start=mod.config.path(f"stage/{side}"))
				zipf.write(absolute_file_path, arcname=rel_path)
