import mod

from mod.bytecode import (
	class_file,
	utf8
)

def apply():
	cf = class_file.create_template()
	cp = cf[0x04]

	cf[0x03] = (5).to_bytes(2)
	cp.append([1, b"\x01", len(utf8.encode("com/thebluetropics/crabpack/CommanderScreen")).to_bytes(2), utf8.encode("com/thebluetropics/crabpack/CommanderScreen")])
	cp.append([2, b"\x07", (1).to_bytes(2)])
	cp.append([3, b"\x01", len(utf8.encode("java/lang/Object")).to_bytes(2), utf8.encode("java/lang/Object")])
	cp.append([4, b"\x07", (3).to_bytes(2)])

	cf[0x05] = (0x0001).to_bytes(2)
	cf[0x06] = (2).to_bytes(2)
	cf[0x07] = (4).to_bytes(2)

	with open(mod.config.path("stage/client/CommanderScreen.class"), "wb") as file:
		file.write(class_file.make(cf))

	print("Created CommanderScreen.class")
