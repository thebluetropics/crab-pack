from . import utf8

def get_utf8(cp, i):
	for entry in cp:
		if entry[0].__eq__(i):
			if entry[1].__eq__(b"\x01"):
				return utf8.decode(entry[3])

	return None
