# slurp - vanity check for the Modern Data Stack

Collect GitHub stats on [prominent](https://github.com/soobrosa/slurp/blob/main/inputs/promis.txt) Modern Data Stack tools with GitHub Actions. Inspired by [Git scraping: track changes over time by scraping to a Git repository](https://simonwillison.net/2020/Oct/9/git-scraping/).

Gets trigerred by the [Action](https://github.com/soobrosa/slurp/blob/main/.github/workflows/scrape.yml).

Logic is a [Makefile](https://github.com/soobrosa/slurp/blob/main/Makefile).

Data sits on [GitHub](https://github.com/soobrosa/slurp/tree/main/outputs).

Inspect the data at [https://share.streamlit.io/soobrosa/slurp/main](https://share.streamlit.io/soobrosa/slurp/main).
