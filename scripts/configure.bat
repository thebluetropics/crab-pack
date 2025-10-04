@echo off

if not exist deps mkdir deps
if not exist deps\kotlin-stdlib-2.2.0.jar curl -o deps\kotlin-stdlib-2.2.0.jar https://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.2.0/kotlin-stdlib-2.2.0.jar

if not exist config mkdir config
if not exist config\features.json copy etc\config_template\features.json config\features.json
