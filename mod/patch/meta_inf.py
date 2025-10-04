import shutil
import mod

def apply_client():
	shutil.rmtree(mod.config.path('stage', 'client', 'META-INF'))
	print('Removed client META-INF directory')

def apply_server():
	shutil.rmtree(mod.config.path('stage', 'server', 'META-INF'))
	print('Removed server META-INF directory')
