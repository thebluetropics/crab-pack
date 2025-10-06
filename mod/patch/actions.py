import mod, shutil

def apply(side_name):
	if not mod.config.is_feature_enabled('actions'):
		return

	if side_name.__eq__('client'):
		shutil.copy(
			mod.config.path('class_files/com/thebluetropics/crabpack/Actions.class'),
			mod.config.path('stage', side_name, 'com/thebluetropics/crabpack/Actions.class')
		)
