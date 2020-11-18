"""
    Create an Excel file from the CSV data sets files created from the roll transcript.
    An Excel file with multiple sheets is useful for sharing with academics etc. 
"""

from receipt_roll.data import roll
import pandas as pd
import settings
from receipt_roll import common


def generate_report():
    """ Create Pandas data frames from CSV and create the Excel file. """

    # check we have the roll data we need
    common.have_entities_data()
    common.have_sums_data()
    common.have_compare_data()

    # get the data frames
    df_sums = roll.daily_sums_df()
    df_roll = roll.roll_with_entities_df()
    df_compare = roll.compare_daily_sums_df()

    # write to an Excel file
    with pd.ExcelWriter(settings.RECEIPT_ROLL_EXCEL) as writer:
        df_roll.to_excel(writer, common.DATA_SHEET, index=False)
        df_sums.to_excel(writer, common.SUMS_SHEET, index=False)
        df_compare.to_excel(writer, common.COMPARE_SUMS_SHEET, index=False)


if __name__ == '__main__':
    generate_report()
