from . import code
from ..constant_pool import get_utf8_at

def get_attribute(attributes, xcp, name):
	for a in attributes:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__(name):
			return a

	return None
