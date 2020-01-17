from receipt_roll import common
from nltk import Tree, RegexpParser, word_tokenize, pos_tag, FreqDist
import pandas
import re
import settings


# --------- methods that load content into arrays

def load_words_into_array(file):
    """ Load list of words from a text file into an array. """
    with open(file, 'r') as file:
        words = file.readlines()
    return [word.strip() for word in words]


# --------- constants used in the module

# label to identify a chunk that possibly represents a name
POSSIBLE_PERSON_LABEL = 'PP'

# label to identify a chunk that possibly represents a place
POSSIBLE_PLACE_LABEL = 'PPL'

# regex for POS labels that might construct provide a person name
PERSON_GRAMMAR_REGEX = POSSIBLE_PERSON_LABEL + ': {<NNP><NNP|FW>*<NNP><NNP>?}'

# regex for POS labels that might construct provide a place
PLACE_GRAMMAR_REGEX = POSSIBLE_PLACE_LABEL + ': { (<NN>|<NNS>)<IN><NNP><NNP>?(<CC><NNP>)?}'

# regex parser for names
person_parser = RegexpParser(PERSON_GRAMMAR_REGEX)

# regex parser for places
places_parser = RegexpParser(PLACE_GRAMMAR_REGEX)

# regex to find text in square brackets (TODO: keep these in a custom tagger?)
square_brackets_regex = re.compile(r'\[.+\]')

# regex to find £.s.d. ... screws up the tokenizer if left in
psd_regex = re.compile(r'(£\d+\.?)(\d+s\.)?(\d+([¼|½|¾])?d\.)?|(\d+s\.)(\d+([¼|½|¾])?d\.)?|(\d+([¼|½|¾])?d\.)')

# regex for marks
marks_regex = re.compile(r'((\d+|¼|½|¾|One|one|a)\smark(s?))')

# Omitted value place-holder
OVP_LABEL = 'OVP'

# stop words not to be used in keywords
KEYWORD_STOP_WORDS = load_words_into_array(settings.KEYWORDS_STOP_WORDS_TXT)

# Load a list of words used in the 'Source' column that doesn't represent a geographical areas.
PLACES_NOUNS = load_words_into_array(settings.PLACES_NOUNS_TXT)

# Load a list of words used in the 'Source' column that doesn't represent a geographical areas
SOURCES_STOP_WORDS = load_words_into_array(settings.SOURCE_STOP_WORDS_TXT)


def add_entities_to_data_csv():
    """ Take the roll CSV and extract data, and add to additional columns. """

    # open the roll CSV
    df = pandas.read_csv(settings.ROLL_CSV)

    # extract people
    df[common.PEOPLE_COL] = df.apply(apply_extract_people, axis=1)

    # extract places
    df[common.PLACES_COL] = df.apply(apply_extract_places, axis=1)

    # extract keywords
    df[common.KEYWORDS_COL] = df.apply(extract_keywords, axis=1)

    # write to a CSV file
    df.to_csv(settings.ROLL_WITH_ENTITIES_CSV, index=False)


def apply_extract_people(row):
    """ Update the data frame to include a column of people mentioned in the details. """

    details = row[common.DETAILS_COL]
    return extract_people(details)


def apply_extract_places(row):
    """ Update the data frame to include a column of places mentioned in the details. """

    # get the details
    details = row[common.DETAILS_COL]

    # extract the details
    places = extract_places(details)

    # get the source since it night be place
    area_place = row[common.SOURCE_COL]

    # only process if not a stop word
    if area_place not in SOURCES_STOP_WORDS:

        # transform to title case
        area_place = area_place.title()

        # add to the array if its not already mentioned in the details
        if area_place not in places:
            places.append(area_place)

    # return the values as a string delimited by a semicolon
    return '; '.join(places)


def clean_details(details):
    """ We are using the standard NLTK POS tagger ... remove certain things from the details to make later
        parsing easier, such as monetary values. """

    # remove square brackets
    details = square_brackets_regex.sub('', details)

    # remove £.s.d.
    details = psd_regex.sub(OVP_LABEL, details)

    # remove marks
    details = marks_regex.sub(OVP_LABEL, details)

    return details


def tidy_tuples(tuple_array):
    """ The NLTK tagger makes a good attempt, but we want to correct some things that might be mis-tagged."""
    results = []
    for item in tuple_array:
        # declare French in toponyms as foreign
        if item[0] in ['fitz', 'le', 'de', 'del']:
            results.append((item[0], 'FW'))
        # we replaced monetary values with a place holder label, set the word type as the same
        elif item[0] == OVP_LABEL:
            results.append((OVP_LABEL, OVP_LABEL))
        elif item[1] == 'RB' and item[0] == 'prior':
            results.append(('prior', 'NN'))
        # accept the POS tagger category ...
        else:
            results.append(item)
    return results


def tokenize_tag_text(text):
    """ Create a POS tag so we can make an educated (ha!) guess about what it us referring to.
        Take the details text from the roll, clean it up, POS tag it, and then correct the tagging if necessary. """

    # clean the text for tagging
    cleaned_text = clean_details(text)

    # tokenize the sentence
    tokens = word_tokenize(cleaned_text)

    # use the default tagger
    tagged = pos_tag(tokens)

    # tidy up and return
    return Tree(1, tidy_tuples(tagged))


def extract_people(text):
    """ Take an entry from the roll and try and extract any personal names. We use the default NLTK POS tagger
      to identify nouns, prepositions etc. We then use a regex to find patterns that might be personal names,
      such as toponyms. """

    # turn into tokens
    tokens = tokenize_tag_text(text)

    # parse the tag into chunks ...
    chunked = person_parser.parse(tokens)

    # hold any people we find
    people = []

    # traverse the chunks to find the names
    for child in chunked:
        if isinstance(child, Tree):
            # chunk tagged as name
            if child.label() == POSSIBLE_PERSON_LABEL:
                # reconstruct the name
                name = []
                for num in range(len(child)):
                    name.append(child[num][0])
                # if we have the bits of name, reconstruct
                if len(name) > 0:
                    people.append(' '.join(name))

    if len(people) > 0:
        return "; ".join(people)
    else:
        return None


def extract_places(text):
    # turn into tokens
    tokens = tokenize_tag_text(text)

    # parse the tag into chunks ...
    chunked = places_parser.parse(tokens)

    # hold places
    places = []

    # traverse the chunks to find the places
    for child in chunked:
        if isinstance(child, Tree):
            # chunk tagged as name
            if child.label() == POSSIBLE_PLACE_LABEL:
                # print(text + " --> " + child[0][0])
                if child[0][0] in PLACES_NOUNS:
                    place = []
                    for num in range(len(child)):
                        if child[num][1] == 'NNP':
                            place.append(child[num][0])
                        elif child[num][1] == 'CC':
                            places.append(' '.join(place))
                            place.clear()

                    if len(place) > 0:
                        places.append(' '.join(place))

    return places


def extract_keywords(row):
    """ Extract nouns as keywords. """

    details = row[common.DETAILS_COL]

    tokens_pos = tokenize_tag_text(details)

    # get the type of words we are interested in
    keywords = [word for word, word_type in tokens_pos if word_type in ['NN', 'NNS']]

    # normalise to lower case
    keywords = [keyword.lower() for keyword in keywords]

    # remove single characters, i.e. punctuation
    keywords = [keyword for keyword in keywords if len(keyword) > 1]

    # remove stop words
    keywords = [keyword for keyword in keywords if keyword not in KEYWORD_STOP_WORDS]

    return '; '.join(keywords)


def create_details_corpus():
    df = pandas.read_csv(settings.ROLL_CSV)

    with open(settings.DETAILS_TEXT_CORPUS, 'w') as corpus_file:
        for index, row in df.iterrows():
            corpus_file.write(clean_details(row[common.DETAILS_COL]) + '\n')


def details_word_frequency():
    raw = open(settings.DETAILS_TEXT_CORPUS).read()
    tokens = word_tokenize(raw)

    # remove single letter tokens, usually punctuation
    tokens = [token for token in tokens if len(token) > 1]

    tokens = [token for token in tokens if token != OVP_LABEL]

    tokens = [token.lower() for token in tokens]

    tokens = [token for token in tokens if token not in KEYWORD_STOP_WORDS]

    freq = FreqDist(tokens)

    for word, frequency in freq.most_common(50):
        print(u'{};{}'.format(word, frequency))


if __name__ == '__main__':
    add_entities_to_data_csv()
