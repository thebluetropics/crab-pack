from mod import class_file, utf8
import mod

def apply():
	if not mod.config.is_feature_enabled('log_version'):
		return

	cf = class_file.load(mod.config.path('stage/server/net/minecraft/server/MinecraftServer.class'))

	for e in cf[0x04]:
		if e[0].__eq__(452):
			e[2] = len(f'Crab Pack {mod.version}').to_bytes(2)
			e[3] = utf8.encode(f'Crab Pack {mod.version}')

	with open(mod.config.path('stage/server/net/minecraft/server/MinecraftServer.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched net.minecraft.server.MinecraftServer')
