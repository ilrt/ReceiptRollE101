import fileinput
import re

in_day = False
in_week = False
in_month = False

week = False
opener = False

header = open('header.inc', 'r')
header_data = header.read()

out = open('roll.xml', 'w')


out.write(header_data)

for line in fileinput.input('roll_1301.txt'):

    if in_month is False:
        out.write("<div type='month'>")
        in_month = True

    if in_week is False:
        out.write("<div type='week'>")
        in_week = True

    if re.match(r"^(The receipt roll of the Irish Exchequer).*$", line):
        line = ""

    # ms header
    elif re.match('^Gross.*\.$', line):
        line = re.sub(r'^Gross.*\.$', r'<head>\g<0></head>', line)

    # membrane ?
    elif re.match(r"^\[m\. \d*\]$", line):
        number = re.search(r"\d+", line).group(0)
        line = "<milestone unit=\"membrane\" n=\"{}\"/>".format(number)

    elif re.match(r'^NOTHING(\.)?$', line):
        line = '<div><opener rend="margin"><placeName>NOTHING</placeName></opener></div></div>'

    # place name
    elif re.match(r'^((\[)?[A-Z]{2,})(\])?(( .*)?( [A-Z]{2,}))?(\])?$', line):
        if not opener:
            line = re.sub(r'^((\[)?[A-Z]{2,})(\])?(( .*)?( [A-Z]{2,}))?(\])?$',
                          r'<div><opener rend="margin"><placeName>\g<0></placeName></opener>', line)
            opener = True
        else:
            line = re.sub(r'^((\[)?[A-Z]{2,})(\])?(( .*)?( [A-Z]{2,}))?(\])?$',
                          r'</div><div><opener rend="margin"><placeName>\g<0></placeName></opener>', line)

    # matching date
    elif re.match('^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday).*$', line):
        if not in_week:
            line = re.sub(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday).*$',
                          '<div type="week"><div type="day"><head><date>\g<0></date></head>', line)
            in_week = True
        else:
            line = re.sub(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday).*$',
                          '<div type="day"><head><date>\g<0></date></head>', line)

    elif re.match(r'^DAILY SUM RECEIVED:.*\.$', line):
        line = re.sub(r'^DAILY SUM RECEIVED:.*\.$', r'</div><closer>\g<0></closer></div>', line)
        opener = False

    elif re.match(r'^SUM:.*\.$', line):
        line = re.sub(r'^SUM:.*\.$', r'</div><closer>\g<0></closer></div>', line)
        opener = False

    elif re.match(r'^(SUM OF (THE )?WEEKLY RECEIPTS:).*\.$', line):
        line = re.sub(r'^(SUM OF (THE )?WEEKLY RECEIPTS:).*\.$', r'<closer>\g<0></closer></div>', line)
        in_week = False

    elif re.match(r'^WEEKLY SUM:.*\.$', line):
        line = re.sub(r'^WEEKLY SUM:.*\.$', r'<closer>\g<0></closer></div>', line)
        in_week = False

    elif re.match(r'^WEEKLY RECEIPT:.*\.$', line):
        line = re.sub(r'^WEEKLY RECEIPT:.*\.$', r'<closer>\g<0></closer></div>', line)
        in_week = False

    elif re.match(r'^SUM OF A DAY AND THREE WEEKS:.*\.$', line):
        line = re.sub(r'^SUM OF A DAY AND THREE WEEKS:.*\.$', r'<closer>\g<0></closer></div>', line)

    elif line.strip() != "":
        line = "<ab>" + line.strip() + "</ab>"

    out.write(line)


if in_month is True:
    out.write("</div>")

if in_week is True:
    out.write("</div>")

out.write("</text></TEI>")
