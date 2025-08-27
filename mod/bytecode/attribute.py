from .constant_pool import vcp_utf8_get

def get_attribute(attr_list, cp, name):
	for a in attr_list:
		if vcp_utf8_get(cp, int.from_bytes(a[0x00])).__eq__(name):
			return a

	return None
