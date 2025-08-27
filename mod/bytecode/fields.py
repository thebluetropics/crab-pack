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

def push(cf, acc, name, desc, attrs):
	f = [None] * 5

	# field meta data
	f[0x00] = (acc).to_bytes(2)
	f[0x01] = (name).to_bytes(2)
	f[0x02] = (desc).to_bytes(2)

	# attributes
	f[0x03] = len(attrs).to_bytes(2)
	f[0x04] = attrs

	cf[0x0b].append(f)

def make_field(acc_flags, name, desc):
	acc = 0x0000

	for flag in acc_flags:
		acc = acc.__or__(field_access_flags[flag])

	f = [None] * 5

	f[0x00] = acc.to_bytes(2)
	f[0x01] = name.to_bytes(2)
	f[0x02] = desc.to_bytes(2)

	f[0x03] = bytes(2)
	f[0x04] = []

	return f
