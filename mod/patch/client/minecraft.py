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

def apply():
	if not mod.config.is_one_of_features_enabled(['etc.log_version', 'blackbox']):
		return

	cf = load_class_file(mod.config.path('stage/client/net/minecraft/client/Minecraft.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('etc.log_version'):
		_modify_init_method(cf, cp_cache)

	if mod.config.is_feature_enabled('blackbox'):
		_modify_set_world_method(cf, cp_cache)
		_modify_start_game_method(cf, cp_cache)

	with open(mod.config.path('stage/client/net/minecraft/client/Minecraft.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched net.minecraft.client.Minecraft')

def _modify_init_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		['getstatic', 'java/lang/System', 'out', 'Ljava/io/PrintStream;'],
		['ldc_w.string', 'Crab Pack ' + mod.version],
		['invokevirtual', 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V']
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for entry in a_code[0x05]:
		entry[0x00] = (int.from_bytes(entry[0x00]) + 9).to_bytes(2)
		entry[0x01] = (int.from_bytes(entry[0x01]) + 9).to_bytes(2)
		entry[0x02] = (int.from_bytes(entry[0x02]) + 9).to_bytes(2)

	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_set_world_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(Lfd;Ljava/lang/String;Lgs;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + assemble_code(cf, cp_cache, 0, 0, [
		'aload_1', ['ifnonnull', 'skip'],
		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'stopClient', '()V'],
		['label', 'skip'],
		'return'
	])

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_start_game_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(Ljava/lang/String;Ljava/lang/String;J)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	code = assemble_code(cf, cp_cache, 0, 130, [
		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		['aload', 5], ['ldc_w.string', '_'], ['invokeinterface', 'wt', 'a', '(Ljava/lang/String;)Ljava/io/File;', 2],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'startClient', '(Ljava/io/File;)V']
	])

	a_code[0x03] = a_code[0x03][0:28] + (
		(int.from_bytes(a_code[0x03][28:30], signed=True) + len(code)).to_bytes(2, signed=True)
	) + a_code[0x03][30:98] + (
		(int.from_bytes(a_code[0x03][98:100], signed=True) + len(code)).to_bytes(2, signed=True)
	) + a_code[0x03][100:130] + code + a_code[0x03][130:131]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
