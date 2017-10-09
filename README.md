# Houzz Crawler

Python script that crawls Houzz.com architects directory and extracts emails from individual Websites and writes them to a .csv file

*Written for Python 2.7*

## How to run it

Go into the directory where the python files are installed and type:

```
python HouzzCrawler.py
```

you will be prompted with the following questions

```
At which page should I start crawling?
```

the script is zero indexed so page 0 is the first page

```
How many pages should I crawl?
```

Crawls from start page to specified number of pages

## Results

The results of the crawl will be displayed in the file *email_mine_clean.csv*

## Bugs

Please report any bugs, this code is pretty experimental
