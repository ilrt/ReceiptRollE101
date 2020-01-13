import os

# location of the data files
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + '/data'

# the transcript created by Paul Dryburgh and Brendan Smith of the 1301/2 Irish Exchequer receipt roll
ROLL_TXT = DATA_DIR + '/roll_1301.txt'

# roll data as csv
ROLL_CSV = DATA_DIR + '/roll_1301.csv'

# roll data with extracted entities
ROLL_WITH_ENTITIES_CSV = DATA_DIR + '/roll_entities_1301.csv'

# daily sums as csv
DAILY_SUMS_CSV = DATA_DIR + '/daily_sums_1301.csv'

# report comparing daily sums
DAILY_SUMS_COMPARE_CSV = DATA_DIR + '/daily_sums_compare.csv'

# receipt roll (number of sheets)
RECEIPT_ROLL_EXCEL = DATA_DIR + '/receipt_roll_1301.xlsx'
