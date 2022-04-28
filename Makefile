paparazzi.sqlite:
	/usr/bin/sqlite3 paparazzi.sqlite < create_paparazzi.sql

paparazzo.json: paparazzi.sqlite
	curl https://api.github.com/repos/PrefectHQ/prefect > $@

all: paparazzo.json

nuke:
	rm paparazzo.json
	rm paparazzi.sqlite