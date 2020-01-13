from receipt_roll import common
from nltk import Tree, RegexpParser, word_tokenize, pos_tag
import pandas
import re
import settings

# label to identify a chunk that represents a name
PERSON_NAME = 'PERSON_NAME'

# regex for POS labels that might construct a name
PERSON_GRAMMAR_REGEX = PERSON_NAME + ': {<NNP><NNP|FW>*<NNP><NNP>?}'

# regex parser for names
person_parser = RegexpParser(PERSON_GRAMMAR_REGEX)

# regex to find text in square brackets (TODO: keep these in a custom tagger?)
square_brackets_regex = re.compile(r'\[.+\]')


def add_entities_to_data_csv():
    df = pandas.read_csv(settings.ROLL_CSV)
    df[common.PEOPLE_COL] = df.apply(extract_entities, axis=1)
    df.to_csv(settings.ROLL_WITH_ENTITIES_CSV)


def extract_entities(row):
    details = row[common.DETAILS_COL]
    people = extract_people(details)
    if len(people) > 0:
        return "; ".join(people)
    else:
        return None


def clean_details(details):
    # remove square brackets
    details = square_brackets_regex.sub('', details)
    return details


def tidy_tuples(tuple_array):
    results = []
    for item in tuple_array:
        if item[0] in ['fitz', 'le', 'de']:
            results.append((item[0], 'FW'))
        else:
            results.append(item)
    return results


def tokenize_tag_text(text):

    cleaned_text = clean_details(text)

    # tokenize the sentence
    tokens = word_tokenize(cleaned_text)

    # use the default tagger
    tagged = pos_tag(tokens)

    tagged = Tree(1, tidy_tuples(tagged))

    return tagged


def extract_people(text):
    """ Take an entry from the roll and try and extract any personal names  """

    # tokenize the sentence
    tokens_pos = tokenize_tag_text(text)

    # parse the tag into chunks ...
    chunked = person_parser.parse(tokens_pos)

    # hold any people we find
    people = []

    # traverse the chunks to find the names
    for child in chunked:
        if isinstance(child, Tree):
            # chunk tagged as name
            if child.label() == PERSON_NAME:
                # reconstruct the name
                name = []
                for num in range(len(child)):
                    name.append(child[num][0])
                # if we have the bits of name, reconstruct
                if len(name) > 0:
                    people.append(' '.join(name))

    return people


if __name__ == '__main__':
    add_entities_to_data_csv()
