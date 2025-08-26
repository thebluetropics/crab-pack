![hello world](./crabpack.png)

**Crab Pack** is a free and open-source mod pack for Minecraft Beta 1.7.3,
developed by [thebluetropics](https://github.com/thebluetropics).

```sh
# Build the assets patcher (Linux)
cd c_libs/assets
make TARGET=linux all
```

```sh
# Build the assets patcher (Windows)
cd c_libs/assets
make TARGET=windows all
```

```sh
# Build the mod
py -m mod make_client

# Build portable user distribution (for Windows)
py make.py

# Project cleanup
git clean -Xdf
```
