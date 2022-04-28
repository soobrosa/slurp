paparazzi.sqlite:
	/usr/bin/sqlite3 paparazzi.sqlite < create_paparazzi.sql

paparazzo.json: paparazzi.sqlite
	curl https://api.github.com/repos/PrefectHQ/prefect > $@

paparazzo.csv: paparazzo.json
	cat paparazzo.json | jq '[.id, .name, .full_name, .html_url, .description, .created_at, .updated_at, .homepage, .size, .stargazers_count, .watchers_count, .language, .has_issues, .has_projects, .has_downloads, .has_wiki, .has_pages, .forks_count, .open_issues_count, .forks, .open_issues, .watchers, .network_count, .subscribers_count, (now | strftime("%Y-%m-%d") )]' -c | sed 's/[][]//g' > $@

load_paparazzo: paparazzo.csv
	sqlite3 paparazzi.sqlite -cmd ".mode csv" ".import paparazzo.csv paparazzi"
	
all: load_paparazzo

nuke:
	rm -f paparazzo.json
	rm -f paparazzo.csv
