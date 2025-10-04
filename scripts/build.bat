@echo OFF

if not exist class_files (
	mkdir class_files
)

kotlinc -d class_files src\blackbox
