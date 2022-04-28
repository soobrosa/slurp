paparazzi.sqlite:
	/usr/bin/sqlite3 paparazzi.sqlite < create_paparazzi.sql > $@

all: paparazzi.sqlite
