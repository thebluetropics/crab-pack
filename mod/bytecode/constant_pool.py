from sys import (exit, stderr)
from . import utf8

def bind_to_constant_pool():
	pass

def get_utf8(cp, i):
	for entry in cp:
		if entry[0].__eq__(i):
			if entry[1].__eq__(b"\x01"):
				return utf8.decode(entry[3])

	return None

def vcp_utf8_get(cp, i):
	if type(i) is bytes:
		pass

	for entry in cp:
		if entry[0].__eq__(i):
			if entry[1].__eq__(b"\x01"):
				return utf8.decode(entry[3])

	return None

def ecp_get(cp, i):
	for entry in cp:
		if entry[0].__eq__(i):
			return entry

	print("Err: can't find specified entry.")
	exit(1)

def icp_utf8_get(cp, s0):
	for entry in cp:
		if entry[1].__eq__(b"\x01"):
			s1 = utf8.decode(entry[3])

			if s0.__eq__(s1):
				return entry[0]

	print("Err: can't find specified utf-8 entry.")
	exit(1)

def i2cp_utf8_get(cp, s0):
	for entry in cp:
		if entry[1].__eq__(b"\x01"):
			s1 = utf8.decode(entry[3])

			if s0.__eq__(s1):
				return entry[0].to_bytes(2)

	print("Err: can't find specified utf-8 entry.")
	exit(1)

def icp_class_get(cp, class_name):
	for entry in cp:
		if entry[1].__eq__(b"\x07"):
			i, _, i2cp_to_utf8 = entry
			vcp_utf8 = vcp_utf8_get(cp, int.from_bytes(i2cp_to_utf8))

			if vcp_utf8.__eq__(class_name):
				return i

	print("Err: can't find specified class entry.")
	exit(1)

def i2cp_class_get(cp, class_name):
	return icp_class_get(cp, class_name).to_bytes(2)

def icp_f_get(cp, owner, name, desc):
	for entry in cp:
		if entry[1].__eq__(b"\x09"):
			i, *_ = entry
			icp_to_class = int.from_bytes(entry[2][0:2])
			icp_to_ntp = int.from_bytes(entry[2][2:4])

			ecp_class = ecp_get(cp, icp_to_class)
			icp_utf8_0 = int.from_bytes(ecp_class[2])
			vcp_utf8_0 = vcp_utf8_get(cp, icp_utf8_0)

			if not owner.__eq__(vcp_utf8_0):
				continue

			ecp_ntp = ecp_get(cp, icp_to_ntp)
			icp_utf8_1 = int.from_bytes(ecp_ntp[2][0:2])
			vcp_utf8_1 = vcp_utf8_get(cp, icp_utf8_1)

			if not name.__eq__(vcp_utf8_1):
				continue

			icp_utf8_2 = int.from_bytes(ecp_ntp[2][2:4])
			vcp_utf8_2 = vcp_utf8_get(cp, icp_utf8_2)

			if not desc.__eq__(vcp_utf8_2):
				continue

			return i

	print("Err: can't find specified field reference entry.")
	exit(1)

def i2cp_f_get(cp, owner, name, desc):
	return icp_f_get(cp, owner, name, desc).to_bytes(2)

def icp_m_get(cp, owner, name, desc):
	for entry in cp:
		if entry[1].__eq__(b"\x0a"):
			i, *_ = entry
			icp_to_class = int.from_bytes(entry[2][0:2])
			icp_to_ntp = int.from_bytes(entry[2][2:4])

			ecp_class = ecp_get(cp, icp_to_class)
			icp_utf8_0 = int.from_bytes(ecp_class[2])
			vcp_utf8_0 = vcp_utf8_get(cp, icp_utf8_0)

			if not owner.__eq__(vcp_utf8_0):
				continue

			ecp_ntp = ecp_get(cp, icp_to_ntp)
			icp_utf8_1 = int.from_bytes(ecp_ntp[2][0:2])
			vcp_utf8_1 = vcp_utf8_get(cp, icp_utf8_1)

			if not name.__eq__(vcp_utf8_1):
				continue

			icp_utf8_2 = int.from_bytes(ecp_ntp[2][2:4])
			vcp_utf8_2 = vcp_utf8_get(cp, icp_utf8_2)

			if not desc.__eq__(vcp_utf8_2):
				continue

			return i

	print("Err: can't find specified method reference entry.")
	exit(1)

def i2cp_m_get(cp, owner, name, desc):
	return icp_m_get(cp, owner, name, desc).to_bytes(2)
