BASE_URL:='https://api.github.com/repos/'

outputs/paparazzi.sqlite:
	/usr/bin/sqlite3 outputs/paparazzi.sqlite < inputs/create_paparazzi.sql

json: outputs/paparazzi.sqlite
	@while read -r file; do \
	save_file=`echo "$${file##*/}"`; \
	curl ${BASE_URL}$${file} > temp/$${save_file}.json; \
	done <inputs/promis.txt
	touch $@

csv: json
	@while read -r file; do \
	save_file=`echo "$${file##*/}"`; \
	cat temp/$${save_file}.json | jq '[.id, .name, .full_name, .html_url, .description, .created_at, .updated_at, .homepage, .size, .stargazers_count, .watchers_count, .language, .has_issues, .has_projects, .has_downloads, .has_wiki, .has_pages, .forks_count, .open_issues_count, .forks, .open_issues, .watchers, .network_count, .subscribers_count, (now | strftime("%Y-%m-%d") )]' -c | sed 's/[][]//g' > temp/$${save_file}.csv; \
	done <inputs/promis.txt
	touch $@

load_paparazzo: csv
	@while read -r file; do \
	save_file=`echo "$${file##*/}"`; \
	sqlite3 outputs/paparazzi.sqlite -cmd ".mode csv" ".import temp/$${save_file}.csv paparazzi"; \
	done <inputs/promis.txt
	touch $@

outputs/paparazzi.csv: load_paparazzo
	sqlite3 -header -csv outputs/paparazzi.sqlite 'select * from paparazzi;' > $@

all: outputs/paparazzi.csv

nuke:
	rm -f temp/*
	rm -f json
	rm -f csv
	rm -f load_paparazzo

