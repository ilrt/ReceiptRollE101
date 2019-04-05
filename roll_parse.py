import fileinput
import re

week = False
opener = False

header = open('header.inc', 'r')
header_data = header.read()

out = open('roll.xml', 'w')


out.write(header_data)

for line in fileinput.input('roll.txt'):

    if re.match(r"^(The receipt roll of the Irish Exchequer).*$", line):
        line = ""

    # ms header
    line = re.sub(r'^Gross.*\.$', r'<head>\g<0></head>', line)

    # membrane ?
    if re.match(r"^\[m\. \d*\]$", line):
        number = re.search(r"\d+", line).group(0)
        line = "<milestone unit=\"membrane\" n=\"{}\"/>".format(number)

    # place name
    if re.match(r'^([A-Z]{2,})(( .*)?( [A-Z]{2,}))?$', line):
        if not opener:
            line = re.sub(r'^([A-Z]{2,})(( .*)?( [A-Z]{2,}))?$',
                          r'<div><opener rend="margin"><placeName>\g<0></placeName></opener>', line)
            opener = True
        else:
            line = re.sub(r'^([A-Z]{2,})(( .*)?( [A-Z]{2,}))?$',
                          r'</div><div><opener rend="margin"><placeName>\g<0></placeName></opener>', line)

    if re.match('^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday).*$', line):
        if not week:
            line = re.sub(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday).*$',
                          '<div type="week"><div type="day"><head><date>\g<0></date></head>', line)
            week = True
        else:
            line = re.sub(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s\d{1,2}\s\w*',
                          '<div type="day"><head><date>\g<0></date></head>', line)

    if re.match(r'^DAILY SUM RECEIVED:.*\.$', line):
        line = re.sub(r'^DAILY SUM RECEIVED:.*\.$', r'</div><closer>\g<0></closer></div>', line)
        opener = False

    if re.match(r'^SUM:.*\.$', line):
        line = re.sub(r'^SUM:.*\.$', r'</div><closer>\g<0></closer></div>', line)
        opener = False

    if re.match(r'^(SUM OF (THE )?WEEKLY RECEIPTS:).*\.$', line):
        line = re.sub(r'^(SUM OF (THE )?WEEKLY RECEIPTS:).*\.$', r'<closer>\g<0></closer></div>', line)
        week = False

    if re.match(r'^WEEKLY SUM:.*\.$', line):
        line = re.sub(r'^WEEKLY SUM:.*\.$', r'<closer>\g<0></closer></div>', line)
        week = False

    if re.match(r'^WEEKLY RECEIPT:.*\.$', line):
        line = re.sub(r'^WEEKLY SUM:.*\.$', r'<closer>\g<0></closer>', line)
        week = False

    line = re.sub(r'^[A-Z].*\.$', r'<ab>\g<0></ab>', line)
    out.write(line)

out.write("</div></body></text></TEI>")
