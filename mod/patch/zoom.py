import mod, shutil, zipfile, os

def apply(side_name):
	if not mod.config.is_feature_enabled('zoom'):
		return

	shutil.copy(
		mod.config.path('class_files/com/thebluetropics/crabpack/Zoom.class'),
		mod.config.path('stage', side_name, 'com/thebluetropics/crabpack/Zoom.class')
	)
