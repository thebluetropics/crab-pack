from modmaker import *
import mod

def apply():
	cf = load_class_file(mod.config.path('stage/client/dc.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0d].append(_create_open_smelter_screen_method(cf, cp_cache))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open(mod.config.path('stage/client/dc.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:dc.class → net.minecraft.entity.player.ClientPlayerEntity')

def _create_open_smelter_screen_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'openSmelterScreen', '(Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', 'dc', 'b', 'Lnet/minecraft/client/Minecraft;'],
		['new', 'com/thebluetropics/crabpack/SmelterScreen'],
		'dup',
		'aload_0',
		['getfield', 'dc', 'c', 'Lix;'],
		'aload_1',
		['invokespecial', 'com/thebluetropics/crabpack/SmelterScreen', '<init>', '(Lix;Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V'],
		['invokevirtual', 'net/minecraft/client/Minecraft', 'a', '(Lda;)V'],
		'return'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
