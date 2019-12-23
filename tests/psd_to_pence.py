import unittest

import receipt_roll.money as money


class TestsMarks(unittest.TestCase):
    """ Test the conversion of marks to pence. """

    def test_1(self):
        self.assertEqual(money.marks_to_pence("1 mark"), 160)

    def test_2(self):
        self.assertEqual(money.marks_to_pence("a mark"), 160)

    def test_3(self):
        self.assertEqual(money.marks_to_pence("one mark"), 160)

    def test_4(self):
        self.assertEqual(money.marks_to_pence("½ mark"), 80)

    def test_5(self):
        self.assertEqual(money.marks_to_pence("2 marks"), 320)


class TestPoundShillingPence(unittest.TestCase):
    """ Test the conversion of £.s.d. to pence """

    def test_1(self):
        self.assertEqual(money.psd_to_pence("£1.6s.4d."), 316)

    def test_2(self):
        self.assertEqual(money.psd_to_pence("£11.6s.4d."), 2716)

    def test_3(self):
        self.assertEqual(money.psd_to_pence("£1.6s.4¼d."), 316.25)

    def test_4(self):
        self.assertEqual(money.psd_to_pence("£1.6s.4½d."), 316.5)

    def test_5(self):
        self.assertEqual(money.psd_to_pence("£1.6s.4¾d."), 316.75)


class TestPoundShilling(unittest.TestCase):
    """ Test the conversion of £.s. to pence """

    def test_1(self):
        self.assertEqual(money.ps_to_pence("£1.6s."), 312)

    def test_2(self):
        self.assertEqual(money.ps_to_pence("£11.6s."), 2712)


if __name__ == '__main__':
    unittest.main()
