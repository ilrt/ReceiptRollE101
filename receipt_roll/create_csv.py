import fileinput
import re
import os
import pandas as pd

from receipt_roll import money

import settings


date_regex = re.compile(r'^(\w*) (\d*) (January|February|March|April|May|June|July|August|September|October|November'
                        r'|December)')

day_regex = re.compile(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)')

receipt_regex = re.compile('^Receipt(s?)')

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

date_col = 'Date'
value_col = 'Value'
pence_col = 'Pence'
data_columns = ['Membrane', 'Term', date_col, 'Day', 'Source', 'Entry', value_col, pence_col]

daily_sums_columns = [date_col, value_col, pence_col]


def date_values(line_val):
    date_match = date_regex.match(line_val)
    day = date_match.group(1)
    day_val = date_match.group(2)
    month_val = date_match.group(3)
    if len(day_val) == 1:
        day_val = "0{}".format(day_val)
    month_val = months_numerical[month_val]
    if month_val == "09" or month_val == "10" or month_val == "11" or month_val == "12":
        year_val = "1301"
    else:
        year_val = "1302"
    return day, "{}-{}-{}".format(year_val, month_val, day_val)


number = None
place = None
day_of_week = None
date = None
term = None

data = []
daily_sums = []

for line in fileinput.input(settings.ROLL_TXT, openhook=fileinput.hook_encoded("utf-8")):
    if re.match(r"^\[m\. \d*\]$", line):
        number = re.search(r"\d+", line).group(0)
    elif re.match(r'^((\[)?[A-Z]{2,})(\])?(( .*)?( [A-Z]{2,}))?(\])?$', line):
        place = line.strip()
        if '[DUBLIN]' in place:
            place = 'DUBLIN'
    elif date_regex.match(line):
        date__ = date_values(line)
        day_of_week = date__[0]
        date = date__[1]
    elif 'Gross receipt' in line:
        if 'Michaelmas' in line:
            term = 'Michaelmas'
        elif 'Trinity' in line:
            term = 'Trinity'
        elif 'Hilary' in line:
            term = 'Hilary'
        elif 'Easter' in line:
            term = 'Easter'
    elif 'DAILY SUM RECEIVED' in line or re.match('^SUM:', line):
        tmp = line.split(':')
        val = tmp[1].strip()
        daily_sums.append([date, val, money.value_to_pence(val)])
        # roll_writer.writerow([number, term, date, '', '', '', val, ''])
        pass
    elif re.match('^SUM OF', line) or re.match('^SUM MEDII', line):
        pass
    elif re.match('^WEEKLY SUM', line) or re.match('^WEEKLY RECEIPT', line):
        pass
        # tmp = line.split(':')
        # if len(tmp) == 2:
        #     val = tmp[1].strip()
        #     roll_writer.writerow([number, term, date, '', '', '', '', val])
    elif 'MONTHLY SUM' in line or 'TOTAL' in line:
        pass
    elif day_regex.match(line):
        pass
    elif receipt_regex.match(line):
        pass
    else:
        if number is not None and place is not None and len(line.strip()) > 0:
            val = money.extract_value(line)
            if val is not None:
                pennies = money.value_to_pence(val)
            else:
                pennies = None
            data.append([number, term, date, day_of_week, place, line.strip(), val, pennies])


if not os.path.exists(settings.DATA_DIR):
    os.makedirs(settings.DATA_DIR)

df = pd.DataFrame(data, columns=data_columns)
df.to_csv(settings.ROLL_CSV, index=False)

df2 = pd.DataFrame(daily_sums, columns=daily_sums_columns)
df2.to_csv(settings.DAILY_SUMS_CSV, index=False)

