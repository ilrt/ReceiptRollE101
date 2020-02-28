import os
import settings
import sys

# CSV column headers
MEM_COL = 'Membrane'                # The membrane the entry is recorded
TERM_COL = 'Term'                   # The term of the entry (Michaelmas, Hilary, Easter and Trinity)
DAY_COL = 'Day'                     # The day. e.g. 'Saturday'
DATE_COL = 'Date'                   # The date of the entry, e.g. 1302-07-11
VAL_COL = 'Value'                   # Value extracted from the details. e.g. '½ mark'
PENCE_COL = 'Pence'                 # The pence equivalent of the value, easier for comparisons
SOURCE_COL = 'Source'               # The source (often geographical), e.g. 'Dublin'
DETAILS_COL = 'Details'             # The details, e.g. 'The same Nicholas, ½ mark for falsely raising hue and cry.'
PSD_COL = '£.s.d.'                  # £.s.d. (computed from the Pence)
YEAR_MONTH_COL = 'Monthly Period'   # Year/Month (computed from the string held in the 'Date' column)

# data extracted from the details column
PEOPLE_COL = 'People'       # people
KEYWORDS_COL = 'Keywords'   # keywords
PLACES_COL = 'Places'       # places

# Sheet names
DATA_SHEET = 'Data'
SUMS_SHEET = 'Daily Sums'
COMPARE_SUMS_SHEET = 'Daily Sums Compare'


def have_transcript():
    """ Do we have the transcript text file? """
    if not os.path.isfile(settings.ROLL_CSV):
        print("Missing " + settings.ROLL_TXT)
        sys.exit()


def have_roll_data():
    """ Have we generated the roll data? """
    if not os.path.isfile(settings.ROLL_CSV):
        print("Missing " + settings.ROLL_CSV + "; you need to generate it. See README.")
        sys.exit()


def have_sums_data():
    """ Have we generated the daily sums data? """
    if not os.path.isfile(settings.DAILY_SUMS_CSV):
        if not os.path.isfile(settings.DAILY_SUMS_CSV):
            print("Missing " + settings.DAILY_SUMS_CSV + "; you need to generate it. See README.")
            sys.exit()


def have_compare_data():
    """ Have we generated the comparisons data? """
    if not os.path.isfile(settings.DAILY_SUMS_COMPARE_CSV):
        if not os.path.isfile(settings.DAILY_SUMS_COMPARE_CSV):
            print("Missing " + settings.DAILY_SUMS_COMPARE_CSV + "; you need to generate it. See README.")
            sys.exit()


def have_entities_data():
    """ Have we extracted the entities """
    if not os.path.isfile(settings.ROLL_WITH_ENTITIES_CSV):
        if not os.path.isfile(settings.ROLL_WITH_ENTITIES_CSV):
            print("Missing " + settings.ROLL_WITH_ENTITIES_CSV + "; you need to generate it. See README.")
            sys.exit()


DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']