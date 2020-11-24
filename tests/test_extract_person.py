import unittest

from receipt_roll import extract_entities


class TestExtractPlaces(unittest.TestCase):

    def test_1(self):
        self.assertEqual(extract_entities.extract_people('From Henry de Curcy 5 marks of a fine for trespass.'),
                         'Henry de Curcy')

    def test_2(self):
        self.assertEqual(extract_entities.extract_people(
            'John Maungne, 10s. for him and his pledges, for he came not though mainperned.'),
            'John Maungne')

    def test_3(self):
        self.assertEqual(extract_entities.extract_people('William de Kent, 10s., for him and his pledges likewise.'),
                         'William de Kent')

    def test_4(self):
        self.assertEqual(extract_entities.extract_people('John Ringere, 1 mark for a false claim against J. de '
                                                         'Fresingfeld.'), 'John Ringere;J. de Fresingfeld')

    def test_5(self):
        self.assertEqual(extract_entities.extract_people('Richard fitz John, ½ mark to have a writ.'),
                         'Richard fitz John')

    def test_6(self):
        self.assertEqual(extract_entities.extract_people('William de Cauntone, sheriff, £20 for debts of divers '
                                                         'persons.'),
                         'William de Cauntone, sheriff')

    def test_7(self):
        self.assertEqual(extract_entities.extract_people('Of profit of the county, 46s.8d. by William de Cauntone, '
                                                         'sheriff.'),
                         'William de Cauntone, sheriff')

    def test_8(self):
        self.assertEqual(extract_entities.extract_people('Thomas de Salop, chaplain, ½ mark as he did not have a '
                                                         'warrant of the king’s service.'),
                         'Thomas de Salop, chaplain')

    def test_9(self):
        self.assertEqual(extract_entities.extract_people('Richard, vicar of the church of Moling, 20d. for unjust '
                                                         'detention.'),
                         'Richard, vicar of the church of Moling')

    def test_10(self):
        self.assertEqual(extract_entities.extract_people('Farm of the lands of Thomas de Arundel, 20s. by Richard '
                                                         'Botild.'),
                         'Thomas de Arundel;Richard Botild')

    def test_11(self):
        self.assertEqual(extract_entities.extract_people('Farm of the mills of Taghyanewy, 10s. by Edusam Inmaulouz.'),
                         'Edusam Inmaulouz')

    def test_12(self):
        self.assertEqual(extract_entities.extract_people('Roger Roth, sheriff, £20 of debts of divers persons.'),
                         'Roger Roth, sheriff')

    def test_13(self):
        self.assertEqual(extract_entities.extract_people('Ralph de Monthermer, earl, and J. his wife, £6 of the '
                                                         'arrears of their account by F., seneschal.'),
                         'Ralph de Monthermer, earl;F., seneschal')

    def test_14(self):
        self.assertEqual(extract_entities.extract_people('The villata of Loughsewdy, 30s. for the escape of Reginald '
                                                         'le Tanner.'),
                         'Reginald le Tanner')

    def test_15(self):
        self.assertEqual(extract_entities.extract_people('William le Blund de Otimi, 53s.4d. of a fine for trespass.'),
                         'William le Blund de Otimi')

    def test_16(self):
        self.assertEqual(extract_entities.extract_people('Nicholas, archbishop of Armagh, £10 of a fine for trespass.'),
                         'Nicholas, archbishop of Armagh')

    def test_17(self):
        self.assertEqual(extract_entities.extract_people('Master Nicholas de Exeter, archdeacon of Ossory, one mark '
                                                         'for himself and his pledges, as he did not prosecute.'),
                         'Master Nicholas de Exeter, archdeacon of Ossory')

    def test_18(self):
        self.assertEqual(extract_entities.extract_people('Roger de Novo Castro, an Irishman, 20s. for having entry on '
                                                         'his tenements at Swords.', ),
                         'Roger de Novo Castro')

    def test_19(self):
        self.assertEqual(extract_entities.extract_people('Of the issues of the lands late of Cristiana de Mariscis at '
                                                         'Killimen [?], 40s., by William Molroni.'),
                         'Cristiana de Mariscis at Killimen;William Molroni')

    def test_20(self):
        self.assertEqual(extract_entities.extract_people('Richard de Peveneseie, seneschal, 10 marks of the arrears '
                                                         'of his account for John fitz H., by John fitz John de la '
                                                         'Hide.'),
                         'Richard de Peveneseie, seneschal;John fitz H.;John fitz John de la Hide')

    # def test_21(self):
    #     self.assertEqual(extract_entities.extract_people('Adam de Cromelin, sheriff, £17.6s.8d. of the arrears of his '
    #                                                      'account, by N. bishop of Leighlin of a fine for trespass.'),
    #                      'Adam de Cromelin, sheriff; N. bishop of Leighlin')

    def test_22(self):
        self.assertEqual(extract_entities.extract_people('Ralph the baker [pistor] of Drogheda, 20d. of a fine for '
                                                         'trespass.'),
                         'Ralph the baker')

    def test_23(self):
        self.assertEqual(extract_entities.extract_people(
            'Robert de Maundeville and Roger de Burford, 26s.8d. of a fine for trespass.'),
                         'Robert de Maundeville;Roger de Burford')


if __name__ == '__main__':
    unittest.main()
