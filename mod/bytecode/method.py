from .constant_pool import vcp_utf8_get

def get_method(cf, cp, name, desc):
	for m in cf[0x0d]:
		if not vcp_utf8_get(cp, int.from_bytes(m[0x01])).__eq__(name) or not vcp_utf8_get(cp, int.from_bytes(m[0x02])).__eq__(desc):
			continue

		return m

	return None
