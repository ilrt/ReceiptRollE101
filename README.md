# Introduction

This is the code and data for the 'Digital Humanities meets Medieval Financial Records: 
The Receipt Rolls of the Irish Exchequer' project. 

## Generating data

The `create_data_csv.py` script parsing the transcript of the roll (`roll_1301.txt`) and
created a CSV file of the individual payments (`roll_1301.csv`) and a list of daily sums
calculated by the Exchequer clerks. It converts pound, shilling, pence and mark values
into pennies for easy comparison.

The `compare_sums_csv.py` script compares the daily sums calculated by the clerks with
those calculated programmatically. This is useful for spotting parsing errors by the 
scripts and, more rarely, issues in the transcript or clerical mistakes.

The `create_excel_report.py` creates three sheets in a single Excel file containing the 
CSV data created by the other scripts.

## Project funding

* Seed corn funding from the Jean Golding Institute, University of Bristol (2019–2020)