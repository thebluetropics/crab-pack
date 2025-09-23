import mod

def apply():
	if mod.config.is_feature_enabled("food.raw_squid_and_calamari"):
		with open("stage/client/lang/en_US.lang", "a") as file:
			file.write("\n".join([
				"item.raw_squid.name=Raw Squid",
				"item.raw_squid.desc=",
				"item.calamari.name=Calamari",
				"item.calamari.desc=Calamari",
				"item.steel_ingot.name=Steel Ingot",
				"item.steel_ingot.desc="
			]))

	if mod.config.is_feature_enabled("block.fortress_bricks"):
		with open("stage/client/lang/en_US.lang", "a") as file:
			file.write("\n".join([
				"tile.fortress_bricks.name=Fortress Bricks",
				"tile.fortress_bricks.desc=",
				"tile.light_fortress_bricks.name=Light Fortress Bricks",
				"tile.light_fortress_bricks.desc=",
				"tile.mortar.name=Mortar",
				"tile.mortar.desc=",
				"tile.smelter.name=Smelter",
				"tile.smelter.desc="
			]))
