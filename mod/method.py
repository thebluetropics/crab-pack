from .constant_pool import i2cpx_utf8, get_utf8_at
from sys import exit, stderr

method_access_flags = {
	'public': 0x0001,
	'private': 0x0002,
	'protected': 0x0004,
	'static': 0x0008,
	'final': 0x0010,
	'synchronized': 0x0020,
	'bridge': 0x0040,
	'varargs': 0x0080,
	'native': 0x0100,
	'abstract': 0x0400,
	'strict': 0x0800,
	'synthetic': 0x1000,
}

def create_method(xcp, acc_flags, name, desc):
	acc = 0x0000

	for flag in acc_flags:
			acc = acc.__or__(method_access_flags[flag])

	m = [None] * 5

	m[0x00] = acc.to_bytes(2)
	m[0x01] = i2cpx_utf8(xcp, name)
	m[0x02] = i2cpx_utf8(xcp, desc)

	m[0x03] = bytes(2)
	m[0x04] = []

	return m

def get_method(cf, xcp, name, desc):
	for m in cf[0x0d]:
		if not get_utf8_at(xcp, int.from_bytes(m[0x01])).__eq__(name) or not get_utf8_at(xcp, int.from_bytes(m[0x02])).__eq__(desc):
			continue

		return m

	print('Err: unknown.', file=stderr)
	exit(1)
