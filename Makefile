paparazzi.sqlite:
	/usr/bin/sqlite3 paparazzi.sqlite < create_paparazzi.sql

paparazzo.json: paparazzi.sqlite
	curl https://api.github.com/repos/PrefectHQ/prefect > $@

paparazzo.csv: paparazzo.json
	cat paparazzo.json | jq '[.id, .name, .full_name, .html_url, .description, .created_at, .updated_at, .homepage, .size, .stargazers_count, .watchers_count, .language, .has_issues, .has_projects, .has_downloads, .has_wiki, .has_pages, .forks_count, .open_issues_count, .topics[], .forks, .open_issues, .watchers, .network_count, .subscribers_count]'" > $@

all: paparazzo.csv

nuke:
	rm paparazzo.json
	rm paparazzi.sqlite
	rm paparazzo.csv
