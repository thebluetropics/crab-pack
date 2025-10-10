import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
)
from modmaker.m import(
	get_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	get_utf8_at
)
from modmaker.utf8 import utf8_encode

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
