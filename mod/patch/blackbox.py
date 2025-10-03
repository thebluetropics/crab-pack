import mod, shutil, zipfile, os

def apply(side_name):
	if not mod.config.is_feature_enabled('blackbox'):
		return

	shutil.copy(
		mod.config.path('class_files/com/thebluetropics/crabpack/Blackbox.class'),
		mod.config.path('stage', side_name, 'com/thebluetropics/crabpack/Blackbox.class')
	)
	shutil.copy(
		mod.config.path('class_files/com/thebluetropics/crabpack/State.class'),
		mod.config.path('stage', side_name, 'com/thebluetropics/crabpack/State.class')
	)

	with zipfile.ZipFile(mod.config.path('deps/kotlin-stdlib-2.2.0.jar'), 'r') as zip_ref:
		for member in zip_ref.namelist():
			if member.lower().endswith('.class'):
				target_path = os.path.join(mod.config.path('stage', side_name), member)
				os.makedirs(os.path.dirname(target_path), exist_ok=True)
				zip_ref.extract(member, mod.config.path('stage', side_name))
