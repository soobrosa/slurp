# slurp — vanity check for the Modern Data Stack

Collect GitHub stats on [prominent](https://github.com/soobrosa/slurp/blob/main/inputs/promis.txt)
Modern Data Stack tools with GitHub Actions. Inspired by
[Git scraping: track changes over time by scraping to a Git repository](https://simonwillison.net/2020/Oct/9/git-scraping/).

## How it works

- A scheduled [GitHub Action](https://github.com/soobrosa/slurp/blob/main/.github/workflows/scrape.yml)
  triggers the scrape.
- The logic lives in a [Makefile](https://github.com/soobrosa/slurp/blob/main/Makefile).
- Collected data is committed to [`outputs/`](https://github.com/soobrosa/slurp/tree/main/outputs).

## Usage

- **Hosted:** browse the data at
  [share.streamlit.io/soobrosa/slurp/main](https://share.streamlit.io/soobrosa/slurp/main).
- **Local:** clone the repo and run `make all` to scrape into `outputs/paparazzi.csv`.
- **Your own list:** edit `inputs/promis.txt` to track different tools.
