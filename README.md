# NSF Grant Award Data Scraper

Michael Nolan

## Description

A script to scrape and concatenate NSF research grant data from the NSF award search database: https://www.nsf.gov/awardsearch/download.jsp

Collects all listed awards from 1959 to present. Individual award information is collected and saved locally as a single CSV table and individual CSV tables from each year.

## Dependencies:

The script requires the following libraries: `pandas`, `requests`, `tqdm`

## Instructions:

To download xml files and the create the dataset (new award information is added regularly), run the python script `scrape_nsf_award_data.py`. The full dataset is ~1GB in size as of 2023-02-10.

After running, local copies of xml files are removed.

## Acknowledgements

Thank you to the NSF for publishing all of this data in one place. I built this to facilitate aggregate analysis of all award records and would not be able to without their dutiful book keeping.