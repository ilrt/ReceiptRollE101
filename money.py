""" Helper module for extracting monetary values from the transcript, normalising to pennies and
    converting back to pound, shilling and pence."""

import re

# convert shillings, pounds and marks to pence
shilling_as_pence = 12
pound_as_pence = 20 * shilling_as_pence
mark_as_pence = (shilling_as_pence * 13) + 4

# regex for monetary values
# marks
marks_regex = re.compile(r'((\d+|½|one|a)\smark(s?))')
# pounds, shilling, pence
psd_regex = re.compile(r'(£(\d+)\.(\d+)s\.(\d+)d\.)')
# pounds and shillings
ps_regex = re.compile(r'(£(\d+)\.(\d)+s\.)')
# shillings and pence
sd_regex = re.compile(r'((\d+)s\.(\d+)d\.)')
# shillings
s_regex = re.compile(r'((\d+)s\.)')
# pence
d_regex = re.compile(r'((\d+)d\.)')
# pound
p_regex = re.compile(r'(£(\d+))')


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


def value_to_pennies(value):
    """ Convert the monetary value of pound, shilling and pence to just pence. For example, '£8.13s.4d.'
        will return the 2080 (int) """

    # marks
    if marks_regex.match(value):
        marks = marks_regex.match(value).group(2)
        if marks == "½":
            marks = 0.5
        elif marks == 'one' or marks == 'a':
            marks = 1
        else:
            marks = int(marks)
        return marks * mark_as_pence
    # £ s. d.
    elif psd_regex.match(value):
        psd = psd_regex.match(value)
        pound = psd.group(2)
        shilling = psd.group(3)
        pence = psd.group(4)
        return (int(pound) * pound_as_pence) + (int(shilling) * shilling_as_pence) + int(pence)
    # £ s.
    elif ps_regex.match(value):
        ps = ps_regex.match(value)
        pound = ps.group(2)
        shilling = ps.group(3)
        return (int(pound) * pound_as_pence) + (int(shilling) * shilling_as_pence)
    # s. d.
    elif sd_regex.match(value):
        sd = sd_regex.match(value)
        shilling = sd.group(2)
        pence = sd.group(3)
        return (int(shilling) * shilling_as_pence) + int(pence)
    # s.
    elif d_regex.match(value):
        d = d_regex.match(value)
        pence = d.group(2)
        return int(pence)
    # d.
    elif s_regex.match(value):
        s = s_regex.match(value)
        shilling = s.group(2)
        return int(shilling) * shilling_as_pence
    # £
    elif p_regex.match(value):
        p = p_regex.match(value)
        pound = p.group(2)
        return int(pound) * pound_as_pence
    elif value == 'NOTHING':
        return 0
    else:
        return None


def pennies_to_psd(pennies):
    """ Convert pence back to pound, shilling and pence ... this might not reflect contemporary conventions ..."""

    pounds = pennies // pound_as_pence
    pennies = pennies % pound_as_pence
    shillings = pennies // shilling_as_pence
    pennies = pennies % shilling_as_pence

    print("{} {} {}".format(pounds, shillings, pennies))

    if pounds > 0 and shillings > 0 and pennies > 0:
        return "£{}.{}s.{}d.".format(pounds, shillings, pennies)
    if pounds > 0 and shillings > 0 and pennies == 0:
        return "£{}.{}s.".format(pounds, shillings)
    if pounds > 0 and shillings == 0 and pennies == 0:
        return "£{}".format(pounds)
    if pounds == 0 and shillings > 0 and pennies > 0:
        return "{}s.{}d.".format(shillings, pennies)
    if pounds == 0 and shillings > 0 and pennies == 0:
        return "{}s.".format(shillings)
    if pounds == 0 and shillings == 0 and pennies > 0:
        return "{}d.".format(pennies)
    else:
        return "Unmatched"
