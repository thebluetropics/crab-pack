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
