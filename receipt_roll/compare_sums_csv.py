import settings
from receipt_roll import roll_data, common
import pandas as pd


def compare_pence(row):
    return row['Roll'] == row['Computed']


def generate_report():

    # get the roll data
    df_roll = roll_data.roll_as_df()

    # get the daily sums from the roll
    df_sums = roll_data.daily_sums_df()

    # compute daily sums ourselves
    df_sums_comp = roll_data.daily_sum_from_roll_df(df_roll)

    # just get the date, pence and merge into a new data frame
    df_sums_left = df_sums[[common.DATE_COL, common.PENCE_COL]]
    df_sums_right = df_sums_comp[[common.DATE_COL, common.PENCE_COL]]
    df_result = pd.merge(df_sums_left, df_sums_right, on=[common.DATE_COL])

    # rename columns
    df_result = df_result.rename(columns={'Pence_x': 'Roll', 'Pence_y': 'Computed'})

    # mark problematic rows
    df_result['Match'] = df_result.apply(compare_pence, axis=1)

    df_result.to_csv(settings.DAILY_SUMS_COMPARE_CSV, index=False)


if __name__ == '__main__':
    generate_report()
