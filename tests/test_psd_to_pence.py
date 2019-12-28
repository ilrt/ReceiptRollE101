import unittest

import receipt_roll.money as money


class TestsMarksToPence(unittest.TestCase):
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


class TestPoundShillingPenceToPence(unittest.TestCase):
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


class TestPoundShillingToPence(unittest.TestCase):
    """ Test the conversion of £.s. to pence """

    def test_1(self):
        self.assertEqual(money.ps_to_pence("£1.6s."), 312)

    def test_2(self):
        self.assertEqual(money.ps_to_pence("£11.6s."), 2712)


class TestShillingPenceToPence(unittest.TestCase):
    """ Test the conversion of s.d. to pence """

    def test_1(self):
        self.assertEqual(money.sd_to_pence("6s.4d."), 76)

    def test_2(self):
        self.assertEqual(money.sd_to_pence("16s.9d."), 201)

    def test_3(self):
        self.assertEqual(money.sd_to_pence("6s.4¼d."), 76.25)

    def test_4(self):
        self.assertEqual(money.sd_to_pence("6s.4½d."), 76.5)

    def test_5(self):
        self.assertEqual(money.sd_to_pence("6s.4¾d."), 76.75)


class TestPenceToPence(unittest.TestCase):
    """ Test the conversion of d. to pence """

    def test_1(self):
        self.assertEqual(money.d_to_pence("4d."), 4)

    def test_3(self):
        self.assertEqual(money.d_to_pence("4¼d."), 4.25)

    def test_4(self):
        self.assertEqual(money.d_to_pence("4½d."), 4.5)

    def test_5(self):
        self.assertEqual(money.d_to_pence("4¾d."), 4.75)


class TestShillingToPence(unittest.TestCase):
    """ Test the conversion of s. to pence """

    def test_1(self):
        self.assertEqual(money.s_to_pence("6s."), 72)

    def test_2(self):
        self.assertEqual(money.s_to_pence("16s."), 192)


class TestPoundsToPence(unittest.TestCase):
    """ Test the conversion of £ to pence """

    def test_1(self):
        self.assertEqual(money.p_to_pence("£1."), 240)

    def test_2(self):
        self.assertEqual(money.p_to_pence("£12."), 2880)


class TestValueToPence(unittest.TestCase):

    def test_1(self):
        self.assertEqual(money.value_to_pence("1 mark"), 160)

    def test_2(self):
        self.assertEqual(money.value_to_pence("a mark"), 160)

    def test_3(self):
        self.assertEqual(money.value_to_pence("one mark"), 160)

    def test_4(self):
        self.assertEqual(money.value_to_pence("½ mark"), 80)

    def test_5(self):
        self.assertEqual(money.value_to_pence("2 marks"), 320)

    def test_6(self):
        self.assertEqual(money.value_to_pence("£1.6s.4d."), 316)

    def test_7(self):
        self.assertEqual(money.value_to_pence("£11.6s.4d."), 2716)

    def test_8(self):
        self.assertEqual(money.value_to_pence("£1.6s.4¼d."), 316.25)

    def test_9(self):
        self.assertEqual(money.value_to_pence("£1.6s.4½d."), 316.5)

    def test_10(self):
        self.assertEqual(money.value_to_pence("£1.6s.4¾d."), 316.75)

    def test_11(self):
        self.assertEqual(money.value_to_pence("£1.6s."), 312)

    def test_12(self):
        self.assertEqual(money.value_to_pence("£11.6s."), 2712)

    def test_13(self):
        self.assertEqual(money.value_to_pence("6s.4d."), 76)

    def test_14(self):
        self.assertEqual(money.value_to_pence("16s.9d."), 201)

    def test_15(self):
        self.assertEqual(money.value_to_pence("6s.4¼d."), 76.25)

    def test_16(self):
        self.assertEqual(money.value_to_pence("6s.4½d."), 76.5)

    def test_17(self):
        self.assertEqual(money.value_to_pence("6s.4¾d."), 76.75)

    def test_18(self):
        self.assertEqual(money.value_to_pence("4d."), 4)

    def test_19(self):
        self.assertEqual(money.value_to_pence("4¼d."), 4.25)

    def test_20(self):
        self.assertEqual(money.value_to_pence("4½d."), 4.5)

    def test_21(self):
        self.assertEqual(money.value_to_pence("4¾d."), 4.75)

    def test_22(self):
        self.assertEqual(money.value_to_pence("6s."), 72)

    def test_23(self):
        self.assertEqual(money.value_to_pence("16s."), 192)

    def test_24(self):
        self.assertEqual(money.value_to_pence("£1."), 240)

    def test_25(self):
        self.assertEqual(money.value_to_pence("£12."), 2880)


if __name__ == '__main__':
    unittest.main()
