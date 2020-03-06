""" Parses the text document (transcript) and creates to CSV files. One has the individual
    entries of sums given in the roll and the other has the daily total of sums recorded by the Exchequer clerk. """

import fileinput
import re
import os
import pandas as pd

from receipt_roll import money, common
import settings

# so we can create the MM in a YYYY-MM-DD format
months_numerical = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

# regex for date matching
date_regex = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(.+)? (\d+) (January|February|'
                        r'March|April|May|June|July|August|September|October|November|December)')

# regex for finding days of the week
day_regex = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)')

# regex for finding 'Receipt' headings
receipt_regex = re.compile('^Receipt(s?)')

# regex for membrane numbers
membrane_regex = re.compile(r'^\[m\. \d*\]$')

# regex for a place declaration
place_regex = re.compile(r'^((\[)?[A-Z]{2,})(\])?(( .*)?( [A-Z]{2,}))?(\])?$')


def date_values(line_val):
    date_match = date_regex.match(line_val)
    day = date_match.group(1)
    day_val = date_match.group(3)
    month_val = date_match.group(4)
    if len(day_val) == 1:
        day_val = "0{}".format(day_val)
    month_val = months_numerical[month_val]
    if month_val == "09" or month_val == "10" or month_val == "11" or month_val == "12":
        year_val = "1301"
    else:
        year_val = "1302"
    return day, "{}-{}-{}".format(year_val, month_val, day_val)


def parse_roll():
    # heading for the main dataset
    data_columns = [common.MEM_COL, common.TERM_COL, common.DATE_COL, common.DAY_COL, common.SOURCE_COL,
                    common.DETAILS_COL, common.VAL_COL, common.PENCE_COL]

    # headings for the daily sums
    daily_sums_columns = [common.DATE_COL, common.VAL_COL, common.PENCE_COL]

    # to hold the data
    data = []
    daily_sums = []

    # keep track of values we use in rows (some span multiple rows)
    number = None
    place = None
    day_of_week = None
    date = None
    term = None

    # go through each line of the transcript
    for line in fileinput.input(settings.ROLL_TXT, openhook=fileinput.hook_encoded("utf-8")):
        # do we have a declaration of a membrane number
        if membrane_regex.match(line):
            number = re.search(r"\d+", line).group(0)
        # or are we declaring a place?
        elif place_regex.match(line):
            place = line.strip()
            if '[DUBLIN]' in place:
                place = 'DUBLIN'
        # or are we declaring with a date declaration?
        elif date_regex.match(line):
            date__ = date_values(line)
            day_of_week = date__[0]
            date = date__[1]
        # or are we declaring the financial term?
        elif 'Gross receipt' in line:
            if 'Michaelmas' in line:
                term = 'Michaelmas'
            elif 'Trinity' in line:
                term = 'Trinity'
            elif 'Hilary' in line:
                term = 'Hilary'
            elif 'Easter' in line:
                term = 'Easter'
        # or are we getting a daily sum?
        elif 'DAILY SUM RECEIVED' in line or re.match('^SUM:', line):
            tmp = line.split(':')
            val = tmp[1].strip()
            daily_sums.append([date, val, money.value_to_pence(val)])
        # ignore these sums
        elif re.match('^SUM OF', line) or re.match('^SUM FOR', line) or re.match('^SUM MEDII', line):
            pass
        # ignore these sums
        elif re.match('^WEEKLY SUM', line) or re.match('^WEEKLY RECEIPT', line):
            pass
        # ignore these sums
        elif 'MONTHLY SUM' in line or 'TOTAL' in line:
            pass
        elif re.match('^NOTHING', line):
            pass
        # ignore these sums
        elif day_regex.match(line):
            pass
        # ignore these sums
        elif receipt_regex.match(line):
            pass
        # this should be some details ...
        else:
            # only process if we have a membrane number, place and the line has content
            if number is not None and place is not None and len(line.strip()) > 0:
                # extract the value from the details
                val = money.extract_value(line)
                # if we extract details, get the value
                if val is not None:
                    # convert to pence
                    pennies = money.value_to_pence(val)
                else:
                    pennies = None
                # some entries don't have a value but refer to the line above
                if val is None and pennies is None and 'the same' in line.lower():
                    pennies = data[-1][-1]
                    val = data[-1][-2]
                # add the row to the data array
                data.append([number, term, date, day_of_week, place, line.strip(), val, pennies])

    # create the data directory if necessary
    if not os.path.exists(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR)

    # make a data frame
    df = pd.DataFrame(data, columns=data_columns)

    # cast the membrane to a number
    df[common.MEM_COL] = df[common.MEM_COL].apply(pd.to_numeric)

    # get the feast days ... days recorded, but no values given
    nothing_df = pd.read_csv(settings.NOTHING_CSV)

    # merge data with feast dates
    df = pd.merge(df, nothing_df, on=[common.MEM_COL, common.TERM_COL, common.DATE_COL, common.DAY_COL,
                                      common.SOURCE_COL, common.DETAILS_COL, common.VAL_COL, common.PENCE_COL],
                  how='outer', sort=True)

    df = df.sort_values(by=[common.DATE_COL, common.MEM_COL])

    # calculate week of the term
    week_values = []
    for term, term_g in df.groupby(common.TERM_COL, sort=False):
        idx = 0
        new_week_on_monday = False
        week = 1
        for index, row in term_g.iterrows():
            day = row[common.DAY_COL]
            if new_week_on_monday is True and day == 'Monday':
                new_week_on_monday = False
                week = week + 1
            if day != 'Monday':
                new_week_on_monday = True
            week_values.append(week)

    df.insert(4, common.WEEK_COL, week_values)

    # write to file
    df.to_csv(settings.ROLL_CSV, index=False)

    # use pandas to write the daily sums csv
    df2 = pd.DataFrame(daily_sums, columns=daily_sums_columns)
    df2.to_csv(settings.DAILY_SUMS_CSV, index=False)


if __name__ == '__main__':
    parse_roll()
