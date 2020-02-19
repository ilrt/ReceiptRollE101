import unittest

from receipt_roll import extract_entities


class TestExtractPlaces(unittest.TestCase):

    def test_1(self):
        places = extract_entities.extract_places('David Mazener, sheriff, £28.11s.11d. of the arrears of his account, '
                                                 'in victuals at Dublin.')
        self.assertEqual(places, ['Dublin'])

    # def test_2(self):
    #     places = extract_entities.extract_places('Walter de la Haye, £6 of the issues of the archbishopric of Dublin, '
    #                                              'by Henry de Waleton in corn of Colonie [Cullen].')
    #     print(places)
    #     self.assertEqual(places, ['Dublin', 'Colonie'])

    def test_3(self):
        places = extract_entities.extract_places('Of the rent of Thristeldermot and Gavernagh, £7, by Walter Ivethorn.')
        self.assertEqual(places, ['Thristeldermot', 'Gavernagh'])

    def test_4(self):
        places = extract_entities.extract_places('Of the farm of the manor of Chapelizod, £11.13s.4d., '
                                                 'by Brother W. de Ros, prior of Kilmainham.')
        self.assertEqual(places, ['Chapelizod', 'Kilmainham'])


if __name__ == '__main__':
    unittest.main()
