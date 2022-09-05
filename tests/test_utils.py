import unittest
import utils.DateTimeUtils as dt_util



class Test_DateTimeUtils(unittest.TestCase):
    def test_isExpectedDateFormat(self):
        valid_expected_timestamp_val = "2022-03-01T09:11:04+01:00"
        valid_expected_utc_timestamp_val = "2022-03-01T09:11:04+00:00"
        invalid_timestamp_val = "2022/03/01T09:11:04+01:00"
        empty_string = ""
        invalid_nonempty_string ="Invalid data for timestamp"

        self.assertTrue(dt_util.isExpectedDateFormat(valid_expected_timestamp_val))
        self.assertTrue(dt_util.isExpectedDateFormat(valid_expected_utc_timestamp_val))
        self.assertFalse(dt_util.isExpectedDateFormat(invalid_timestamp_val))
        self.assertFalse(dt_util.isExpectedDateFormat(empty_string))
        self.assertFalse(dt_util.isExpectedDateFormat(invalid_nonempty_string))




if __name__ == "__main__":
    unittest.main()






