from modmaker import *
import mod

def apply():
	if not mod.config.is_one_of_features_enabled(['etc.log_version']):
		return

	cf = load_class_file(mod.config.path('stage/server/net/minecraft/server/MinecraftServer.class'))

	if mod.config.is_feature_enabled('etc.log_version'):
		for entry in cf[0x04]:
			if entry[0].__eq__(452):
				entry[2] = len(f'Crab Pack {mod.version}').to_bytes(2)
				entry[3] = utf8_encode(f'Crab Pack {mod.version}')

	with open(mod.config.path('stage/server/net/minecraft/server/MinecraftServer.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched net.minecraft.server.MinecraftServer')
