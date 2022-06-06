# Introduction

This is the code and data for the 'Digital Humanities meets Medieval Financial Records: 
The Receipt Rolls of the Irish Exchequer' project. 

## Project Structure

### data

Location of the source transcript (roll_1301.txt) and file that hold lists of stop words
for various aspects of data processing. CSV and Excel files are also written to here by
the Python scripts albeit the `.gitignore` omits them from the repository.

### receipt_roll

A module that contains all the Python files for processing the data.

### tests

A number of unit tests with particular emphasis on areas that extract monetary values
and entities like people and places.

```
python -m unittest tests/test_extract_person.py
python -m unittest tests/test_extract_place.py
python -m unittest tests/test_pence_to_psd.py
python -m unittest tests/test_psd_to_pence.py 
```

## Generating data

The `generate_data.py` is a wrapper that runs all the scripts below.

The `create_data_csv.py` script parsing the transcript of the roll (`roll_1301.txt`) and
created a CSV file of the individual payments (`roll_1301.csv`) and a list of daily sums
calculated by the Exchequer clerks. It converts pound, shilling, pence and mark values
into pennies for easy comparison.

The `compare_sums_csv.py` script compares the daily sums calculated by the clerks with
those calculated programmatically. This is useful for spotting parsing errors by the 
scripts and, more rarely, issues in the transcript or clerical mistakes.

The `extract_entities.py` scripts processes `roll_1301.csv` to extract people, places
and keywords and store the data in `roll_entities_1301.csv`.

The `create_excel_report.py` creates three sheets in a single Excel file containing the 
CSV data created by the other scripts.

## Project funding

* Seed corn funding from the Jean Golding Institute, University of Bristol (2019–2020)