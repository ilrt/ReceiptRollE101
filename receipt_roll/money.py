""" Helper module for extracting monetary values from the transcript, normalising to pennies and
    converting back to pound, shilling and pence."""

import re

# convert shillings, pounds and marks to pence
shilling_as_pence = 12
pound_as_pence = 20 * shilling_as_pence
mark_as_pence = (shilling_as_pence * 13) + 4

# regex for monetary values
# marks
marks_regex = re.compile(r'((\d+|¼|½|¾|One|one|a)\smark(s?))')
# pounds, shilling, pence
psd_regex = re.compile(r'(£(\d+)\.(\d+)s\.((\d+)(¼|½|¾)?)d\.)')
# pounds and shillings
ps_regex = re.compile(r'(£(\d+)\.(\d+)+s\.)')
# pounds and pence
pd_regex = re.compile(r'(£(\d+)\.((\d+)(¼|½|¾)?)d\.)')
# shillings and pence
sd_regex = re.compile(r'((\d+)s\.((\d+)(¼|½|¾)?d\.))')
# shillings
s_regex = re.compile(r'((\d+)s\.)')
# pence
d_regex = re.compile(r'(((\d+)(¼|½|¾)?)d\.)')
# pound
p_regex = re.compile(r'(£(\d+))')


def is_vulgar_fraction(val):
    """ Is a character representing a fraction? """
    return val == '¼' or val == '½' or val == '¾'


def vulgar_fraction_to_decimal(val):
    """ Turn a decimal fraction into a vulgar fraction. """
    if val == '¼':
        return 0.25
    elif val == '½':
        return 0.5
    elif val == '¾':
        return 0.75
    else:
        return None


def decimal_to_vulgar_fraction(val):
    """ Turn a vulgar fraction into its decimal form. """
    if val == 0.25:
        return '¼'
    elif val == 0.5:
        return '½'
    elif val == 0.75:
        return '¾'
    else:
        return None


def marks_to_pence(val):
    """ Turn a mark (or fraction of a mark) to its pence value. """
    marks = marks_regex.match(val).group(2)
    if is_vulgar_fraction(marks):
        return vulgar_fraction_to_decimal(marks) * mark_as_pence
    elif marks.lower() == 'one' or marks == 'a':
        marks = 1
    else:
        marks = int(marks)
    return marks * mark_as_pence


def psd_to_pence(val):
    """ Turn pound, shilling and pence to its pence value. """

    psd = psd_regex.match(val)

    if psd.group(6):
        fraction = vulgar_fraction_to_decimal(psd.group(6))
    else:
        fraction = 0

    pence = psd.group(5)
    shilling = psd.group(3)
    pound = psd.group(2)

    return (int(pound) * pound_as_pence) + (int(shilling) * shilling_as_pence) + int(pence) + fraction


def ps_to_pence(val):
    """ Turn pound and shilling to its pence value. """

    ps = ps_regex.match(val)
    pound = ps.group(2)
    shilling = ps.group(3)

    return (int(pound) * pound_as_pence) + (int(shilling) * shilling_as_pence)


def pd_to_pence(val):
    """ Turn pounds and pence to its pence value """

    pd = pd_regex.match(val)

    if pd.group(5):
        fraction = vulgar_fraction_to_decimal(pd.group(5))
    else:
        fraction = 0

    pence = pd.group(4)
    pound = pd.group(2)

    return (int(pound) * pound_as_pence) + int(pence) + fraction


def sd_to_pence(val):
    """ Turn shilling and pence to its pence value. """

    sd = sd_regex.match(val)

    if sd.group(5):
        fraction = vulgar_fraction_to_decimal(sd.group(5))
    else:
        fraction = 0

    pence = sd.group(4)
    shilling = sd.group(2)

    return (int(shilling) * shilling_as_pence) + int(pence) + fraction


def d_to_pence(val):
    """ Turn pence to its pence value ... i.e. handle any vulgar fractions """

    d = d_regex.match(val)

    if d.group(4):
        fraction = vulgar_fraction_to_decimal(d.group(4))
    else:
        fraction = 0

    pence = d.group(3)

    return int(pence) + fraction


def s_to_pence(val):
    """ Turn shillings into pence """

    s = s_regex.match(val)

    return int(s.group(2)) * shilling_as_pence


def p_to_pence(val):
    """ Turn pounds into pence """

    p = p_regex.match(val)
    pound = p.group(2)
    return int(pound) * pound_as_pence


def extract_value(text):
    """ Extract the monetary value from a string. The value should be marks or pound, shilling and pence.
        For example, from 'Of aid promised to the king, £8.13s.4d., by the community of the town of Kilkenny.'
        it should return '£8.13s.4d.' """

    # marks
    if marks_regex.search(text):
        return marks_regex.search(text).group(1)
    # £ s. d.
    elif psd_regex.search(text):
        return psd_regex.search(text).group(1)
    # £ s.
    elif ps_regex.search(text):
        return ps_regex.search(text).group(1)
    # £ d.
    elif pd_regex.search(text):
        return pd_regex.search(text).group(1)
    # s. d.
    elif sd_regex.search(text):
        return sd_regex.search(text).group(1)
    # s.
    elif s_regex.search(text):
        return s_regex.search(text).group(1)
    # d.
    elif d_regex.search(text):
        return d_regex.search(text).group(1)
    # £
    elif p_regex.search(text):
        return p_regex.search(text).group(1)
    elif 'NOTHING' in text:
        return 'NOTHING'
    else:
        return None


def value_to_pence(value):
    """ Convert the monetary value of pound, shilling and pence to just pence. For example, '£8.13s.4d.'
        will return the 2080 (int) """

    # marks
    if marks_regex.match(value):
        return marks_to_pence(value)
    # £ s. d.
    elif psd_regex.match(value):
        return psd_to_pence(value)
    # £ s.
    elif ps_regex.match(value):
        return ps_to_pence(value)
    elif pd_regex.match(value):
        return pd_to_pence(value)
    # s. d.
    elif sd_regex.match(value):
        return sd_to_pence(value)
    # d.
    elif d_regex.match(value):
        return d_to_pence(value)
    # s.
    elif s_regex.match(value):
        return s_to_pence(value)
    # £
    elif p_regex.match(value):
        return p_to_pence(value)
    elif value == 'NOTHING':
        return 0
    else:
        return None


def pence_to_psd(pennies):
    """ Convert pence back to pound, shilling and pence ... this might not reflect contemporary conventions."""

    # use modulus and floor to convert back to pound, shillings and pence
    pounds = pennies // pound_as_pence
    pennies = pennies % pound_as_pence
    shillings = pennies // shilling_as_pence
    pennies = pennies % shilling_as_pence
    fraction = pennies % 1

    # format the various bits ... pound, shillings and pence are cast to integers to remove .0
    pound_fmt = "£{}.".format(int(pounds)) if pounds > 0 else ""
    shilling_fmt = "{}s.".format(int(shillings)) if shillings > 0 else ""
    # we need to check for quarter fractions
    fraction_fmt = decimal_to_vulgar_fraction(fraction) if fraction > 0 else ""
    if fraction_fmt is None:
        fraction_fmt = ""
    pennies_fmt = "{}{}d.".format(int(pennies), fraction_fmt) if pennies > 0 or fraction > 0 else ""

    return "{}{}{}".format(pound_fmt, shilling_fmt, pennies_fmt)
