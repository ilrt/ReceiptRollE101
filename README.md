# Introduction

This is the code and data for the 'Digital Humanities meets Medieval Financial Records: 
The Receipt Rolls of the Irish Exchequer' project. 

## Setup the environment

Create a virtual environment and activate it, e.g.

```
python -m venv .myenv
source .myenv/bin/activate
```

Install the dependencies:

```
pip install pip --upgrade
pip install -r requirements.txt
```

## Generate the data

On the first run this can take a while as NLTK downloads various corpora.
The script will process the text of a transcript, create various CSV files and, ultimately,
an Excel spreadsheet. These files are found in the `data` directory.

```
python generate_data.py
```

## Generating plots

This will generate the plots used in the blog posts and the paper published in 
_Irish Economic and Social History_.

## Project Structure

### data

Location of the source transcript (roll_1301.txt) and file that hold lists of stop words
for various aspects of data processing. CSV and Excel files are also written to here by
the Python scripts albeit the `.gitignore` omits them from the repository.

### receipt_roll

A module that contains all the Python files for processing the data. These files are 
found in the _plots_ directory.

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