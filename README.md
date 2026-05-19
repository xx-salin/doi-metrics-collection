# doi-citation-metrics

A lightweight framework for collecting citation and download metrics from academic papers using their DOIs.

## Methods
- **API collection** via [Crossref](https://api.crossref.org/): retrieves citation counts and abstract metadata
- **Web scraping** via Selenium: retrieves download counts from publisher pages

## Data
The input dataset (`data/manscirep_meta_data.xlsx`) is not included in this repository.
Contact to request it.

## Requirements
- Python 3.12
- pandas, requests, selenium, webdriver-manager

Install dependencies:
pip install pandas requests selenium webdriver-manager

## Usage
Run the cells in `doi_apidatacollection_webscraping.ipynb` in order.
Place your input Excel file at `data/manscirep_meta_data.xlsx` before running.
