import unittest

from utils import extract_rate, humanize, parse_delay


class ParseDelayTests(unittest.TestCase):
    def test_units(self):
        self.assertEqual(parse_delay("30s"), 30)
        self.assertEqual(parse_delay("10m"), 600)
        self.assertEqual(parse_delay("2h"), 7200)
        self.assertEqual(parse_delay("1d"), 86400)

    def test_case_and_spaces(self):
        self.assertEqual(parse_delay(" 5M "), 300)

    def test_bad_input(self):
        for bad in ("", "abc", "10", "m", "-5m", "1.5h", "10x"):
            with self.assertRaises(ValueError, msg=bad):
                parse_delay(bad)

    def test_zero_and_too_long(self):
        with self.assertRaises(ValueError):
            parse_delay("0m")
        with self.assertRaises(ValueError):
            parse_delay("8d")
        self.assertEqual(parse_delay("7d"), 7 * 86400)


class HumanizeTests(unittest.TestCase):
    def test_values(self):
        self.assertEqual(humanize(90), "1m 30s")
        self.assertEqual(humanize(3600), "1h")
        self.assertEqual(humanize(90061), "1d 1h 1m 1s")


class ExtractRateTests(unittest.TestCase):
    DATA = {"Valute": {
        "USD": {"Value": 90.5, "Nominal": 1},
        "JPY": {"Value": 60.0, "Nominal": 100},
    }}

    def test_simple(self):
        self.assertAlmostEqual(extract_rate(self.DATA, "usd"), 90.5)

    def test_nominal(self):
        self.assertAlmostEqual(extract_rate(self.DATA, "JPY"), 0.6)

    def test_unknown(self):
        with self.assertRaises(KeyError):
            extract_rate(self.DATA, "XXX")


if __name__ == "__main__":
    unittest.main()
