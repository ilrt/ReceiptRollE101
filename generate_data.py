""" A script that pulls together all the other scripts to parse the transcript and create an Excel file. """
from receipt_roll import create_data_csv, compare_sums_csv, extract_entities, create_excel_report
import settings
import nltk
import ssl

if __name__ == '__main__':

    # https://stackoverflow.com/questions/38916452/
    print('Installing NLTK modules')
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('popular')

    # parse the transcript and create the CSV
    print('Parsing transcript to create  ' + settings.ROLL_CSV + " and " + settings.DAILY_SUMS_CSV)
    create_data_csv.parse_roll()

    # compare sums and create report
    print('Compare computed daily sums with those of the Exchequer clerk and write to '
          + settings.DAILY_SUMS_COMPARE_CSV)
    compare_sums_csv.generate_report()

    # extract entities
    print('Extracting entities and creating ' + settings.ROLL_WITH_ENTITIES_CSV)
    extract_entities.add_entities_to_data_csv()

    # Bundle up the CSV as sheets in an Excel file
    print('Writing all data to ' + settings.RECEIPT_ROLL_EXCEL)
    create_excel_report.generate_report()
