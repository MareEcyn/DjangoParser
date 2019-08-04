import subprocess
import sys

if __name__ == '__main__':
	subprocess.Popen(['python manage.py runserver'], shell=True)
	subprocess.Popen(['python Parser/server.py'], shell=False)
	subprocess.Popen(['python', 'Parser/scheduler.py'], shell=False)