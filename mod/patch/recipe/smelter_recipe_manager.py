from modmaker import *
import os, mod

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/SmelterRecipeManager'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, 'java/lang/Object')

	cf[0x0b].append(create_field(cf, cp_cache, ['private', 'static'], 'recipes', 'Ljava/util/Map;'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_static_initializer(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_craft_method(cf, cp_cache, side, c_name))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:SmelterRecipeManager.class')

def _create_static_initializer(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<clinit>', '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		['new', 'java/util/HashMap'],
		'dup',
		['invokespecial', 'java/util/HashMap', '<init>', '()V'],
		['putstatic', c_name, 'recipes', 'Ljava/util/Map;'],

		['getstatic', c_name, 'recipes', 'Ljava/util/Map;'],
		'iconst_2',
		['anewarray', 'java/lang/Integer'],

		'dup',
		'iconst_0',
		['getstatic', ('gm', 'ej'), 'k', ('Lgm;', 'Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],
		['invokestatic', 'java/lang/Integer', 'valueOf', '(I)Ljava/lang/Integer;'],
		'aastore',

		'dup',
		'iconst_1',
		['getstatic', ('uu', 'na'), 'I', ('Luu;', 'Lna;')],
		['getfield', ('uu', 'na'), 'bn', 'I'],
		['invokestatic', 'java/lang/Integer', 'valueOf', '(I)Ljava/lang/Integer;'],
		'aastore',

		['invokestatic', 'java/util/Arrays', 'asList', '([Ljava/lang/Object;)Ljava/util/List;'],

		['new', ('iz', 'fy')],
		'dup',
		['getstatic', ('gm', 'ej'), 'STEEL_INGOT', ('Lgm;', 'Lej;')],
		['invokespecial', ('iz', 'fy'), '<init>', ('(Lgm;)V', '(Lej;)V')],

		['invokeinterface', 'java/util/Map', 'put', '(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;', 3],
		'pop',
		'return'
	])
	a_code = a_code_assemble([
		(7).to_bytes(2),
		(0).to_bytes(2),
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

def _create_craft_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public', 'static'], 'craft', ['(II)Liz;', '(II)Lfy;'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'iconst_2',
		['anewarray', 'java/lang/Integer'],

		'dup',
		'iconst_0',
		'iload_0',
		['invokestatic', 'java/lang/Integer', 'valueOf', '(I)Ljava/lang/Integer;'],
		'aastore',

		'dup',
		'iconst_1',
		'iload_1',
		['invokestatic', 'java/lang/Integer', 'valueOf', '(I)Ljava/lang/Integer;'],
		'aastore',

		['invokestatic', 'java/util/Arrays', 'asList', '([Ljava/lang/Object;)Ljava/util/List;'],
		['astore', 2],

		['getstatic', c_name, 'recipes', 'Ljava/util/Map;'],
		['aload', 2],
		['invokeinterface', 'java/util/Map', 'get', '(Ljava/lang/Object;)Ljava/lang/Object;', 2],
		['checkcast', ('iz', 'fy')],
		'areturn',
	])
	a_code = a_code_assemble([
		(4).to_bytes(2),
		(3).to_bytes(2),
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
