CREATE TABLE IF NOT EXISTS raw.paparazzi (
id INTEGER NOT NULL
,name TEXT NOT NULL
,full_name TEXT NOT NULL
,html_url TEXT NOT NULL UNIQUE
,description TEXT NOT NULL
,created_at TEXT NOT NULL
,updated_at TEXT NOT NULL
,homepage TEXT NOT NULL
,size INTEGER NOT NULL
,stargazers_count INTEGER NOT NULL
,watchers_count INTEGER NOT NULL
,language TEXT NOT NULL
,has_issues INTEGER NOT NULL
,has_projects INTEGER NOT NULL
,has_downloads INTEGER NOT NULL
,has_wiki INTEGER NOT NULL
,has_pages INTEGER NOT NULL
,forks_count INTEGER NOT NULL
,open_issues_count INTEGER NOT NULL
,forks INTEGER NOT NULL
,open_issues INTEGER NOT NULL
,watchers INTEGER NOT NULL
,network_count INTEGER NOT NULL
,subscribers_count INTEGER NOT NULL
,date TEXT NOT NULL
);
