# doi-citation-metrics

A lightweight framework for collecting citation and download metrics from academic papers using their DOIs.

## Methods
- **API collection** via [Crossref](https://api.crossref.org/): retrieves citation counts and abstract metadata
- **Web scraping** via Selenium: retrieves download counts from publisher pages
- **Web scraping** via CloakBrowser: iterated scraping with bot-wall handling

## Data
The input dataset (`data/manscirep_meta_data.xlsx`) is not included in this repository.
Contact to request it.

## Requirements
- Python 3.12
- pandas, requests, selenium, webdriver-manager, openpyxl, cloakbrowser

Install dependencies:
pip install -r requirements.txt

## Usage
For API collection and single-observation scraping tests, run the cells in `doi_apidatacollection_webscraping.ipynb` in order.

For iterated web scraping, run `doi_webscraping_cloakbrowser.py`.

Place your input Excel file at `data/manscirep_meta_data.xlsx` before running.
