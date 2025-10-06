import urllib.request, os, shutil

project_dir = os.path.dirname(os.path.dirname(__file__))

if not os.path.exists(os.path.join(project_dir, 'deps')):
	os.mkdir(os.path.join(project_dir, 'deps'))

if not os.path.exists(os.path.join(project_dir, 'deps', 'kotlin-stdlib-2.2.0.jar')):
	urllib.request.urlretrieve('https://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.2.0/kotlin-stdlib-2.2.0.jar', os.path.join(project_dir, 'deps', 'kotlin-stdlib-2.2.0.jar'))

if not os.path.exists(os.path.join(project_dir, 'config')):
	os.mkdir(os.path.join(project_dir, 'config'))

if not os.path.exists(os.path.join(project_dir, 'config', 'features.json')):
	shutil.copy(os.path.join(project_dir, 'etc', 'config_template', 'features.json'), os.path.join(project_dir, 'config', 'features.json'))
