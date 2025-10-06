![hello world](./crabpack.png)

**Crab Pack** is a free and open-source mod pack for Minecraft Beta 1.7.3,
developed by [thebluetropics](https://github.com/thebluetropics).

```bat
@REM Configure
.\scripts\configure.bat
```

```sh
# Compile
kotlinc -d class_files src/blackbox
javac -d class_files src/zoom # → jdk8
javac -d class_files src/actions/com/thebluetropics/crabpack/Actions.java # → jdk8
```

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
py -m mod make

# Build portable user distribution (for Windows)
py ./scripts/make.py

# Project cleanup
git clean -Xdf
```
