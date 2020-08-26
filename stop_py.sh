ps aux | grep cloudbrain-importer-sensors_main.py |grep -v grep|cut -c 9-15|xargs kill -9
