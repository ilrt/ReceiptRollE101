import unittest

import receipt_roll.money as money


class TestPenceToPsd(unittest.TestCase):

    def test_1(self):
        self.assertEqual(money.pence_to_psd(160), '13s.4d.')

    def test_2(self):
        self.assertEqual(money.pence_to_psd(316), '£1.6s.4d.')

    def test_3(self):
        self.assertEqual(money.pence_to_psd(2716), '£11.6s.4d.')

    def test_4(self):
        self.assertEqual(money.pence_to_psd(316.25), '£1.6s.4¼d.')

    def test_5(self):
        self.assertEqual(money.pence_to_psd(316.5), "£1.6s.4½d.")

    def test_5(self):
        self.assertEqual(money.pence_to_psd(316.75), "£1.6s.4¾d.")

    def test_6(self):
        self.assertEqual(money.pence_to_psd(312), "£1.6s.")

    def test_7(self):
        self.assertEqual(money.pence_to_psd(2712), "£11.6s.")

    def test_8(self):
        self.assertEqual(money.pence_to_psd(76), "6s.4d.")

    def test_9(self):
        self.assertEqual(money.pence_to_psd(201), "16s.9d.")

    def test_10(self):
        self.assertEqual(money.pence_to_psd(76.25), "6s.4¼d.")

    def test_11(self):
        self.assertEqual(money.pence_to_psd(76.5), "6s.4½d.")

    def test_12(self):
        self.assertEqual(money.pence_to_psd(76.75), "6s.4¾d.")

    def test_13(self):
        self.assertEqual(money.pence_to_psd(4), "4d.")

    def test_14(self):
        self.assertEqual(money.pence_to_psd(4.25), "4¼d.")

    def test_15(self):
        self.assertEqual(money.pence_to_psd(4.5), "4½d.")

    def test_16(self):
        self.assertEqual(money.pence_to_psd(4.75), "4¾d.")

    def test_17(self):
        self.assertEqual(money.pence_to_psd(72), "6s.")

    def test_18(self):
        self.assertEqual(money.pence_to_psd(192), "16s.")

    def test_19(self):
        self.assertEqual(money.pence_to_psd(240), "£1.")

    def test_20(self):
        self.assertEqual(money.pence_to_psd(2880), "£12.")