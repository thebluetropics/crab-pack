from .constant_pool import vcp_utf8_get

def get_method(cf, cp, name, desc):
	for m in cf[0x0d]:
		name = vcp_utf8_get(cp, int.from_bytes(m[0x01]))
		desc = vcp_utf8_get(cp, int.from_bytes(m[0x02]))

		if not name.__eq__(name) or not desc.__eq__(desc):
			continue

		return m

	return None
