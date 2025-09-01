import mod

from mod import (
	class_file,
	constant_pool
)
from mod.constant_pool import i2cpx_c

def apply():
	cf = class_file.create_new()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x05] = (0x0001).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/CommanderScreen')
	cf[0x07] = i2cpx_c(cf, cp_cache, 'java/lang/Object')

	with open(mod.config.path('stage/client/CommanderScreen.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Created CommanderScreen.class')
