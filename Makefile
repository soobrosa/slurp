BASE_URL:='https://api.github.com/repos/'

paparazzi.sqlite:
	/usr/bin/sqlite3 paparazzi.sqlite < create_paparazzi.sql

json: paparazzi.sqlite
	@while read -r file; do \
	save_file=`echo "$${file##*/}"`; \
	curl ${BASE_URL}$${file} > $${save_file}.json; \
	done <promis.txt
	touch $@

csv: json
	@while read -r file; do \
	save_file=`echo "$${file##*/}"`; \
	cat $${save_file}.json | jq '[.id, .name, .full_name, .html_url, .description, .created_at, .updated_at, .homepage, .size, .stargazers_count, .watchers_count, .language, .has_issues, .has_projects, .has_downloads, .has_wiki, .has_pages, .forks_count, .open_issues_count, .forks, .open_issues, .watchers, .network_count, .subscribers_count, (now | strftime("%Y-%m-%d") )]' -c | sed 's/[][]//g' > $${save_file}.csv; \
	done <promis.txt
	touch $@

load_paparazzo: csv
	@while read -r file; do \
	save_file=`echo "$${file##*/}"`; \
	sqlite3 paparazzi.sqlite -cmd ".mode csv" ".import $${save_file}.csv paparazzi"; \
	done <promis.txt
	touch $@

all: load_paparazzo

nuke:
	rm -f *.json
	rm -f *.csv
	rm -f csv
	rm -f json
	rm -f load_paparazzo
