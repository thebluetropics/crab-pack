from .cp import get_utf8_at

def get_attribute(attributes, cp_cache, name):
	for a in attributes:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__(name):
			return a

	return None
