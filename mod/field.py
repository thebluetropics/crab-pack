from .constant_pool import i2cpx_utf8

field_access_flags = {
	'public': 0x0001,
	'private': 0x0002,
	'protected': 0x0004,
	'static': 0x0008,
	'final': 0x0010,
	'volatile': 0x0040,
	'transient': 0x0080,
	'synthetic': 0x1000,
	'enum': 0x4000,
}

def create_field(cf, cp_cache, acc_flags, name, desc):
	acc = 0x0000

	for flag in acc_flags:
		acc = acc.__or__(field_access_flags[flag])

	f = [None] * 5

	f[0x00] = acc.to_bytes(2)
	f[0x01] = i2cpx_utf8(cf, cp_cache, name)
	f[0x02] = i2cpx_utf8(cf, cp_cache, desc)

	f[0x03] = bytes(2)
	f[0x04] = []

	return f
