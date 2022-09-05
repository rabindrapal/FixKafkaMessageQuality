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

    def test_convertToUTC(self):
        valid_non_utc_ber_timestamp_val = "2022-03-01T09:11:04+01:00"
        valid_non_utc_ind_timestamp_val = "2022-03-01T09:11:04+05:30"
        valid_utc_timestamp_val = "2022-03-01T09:11:04+00:00"
        converted_val_non_utc_ber =str(dt_util.convertToUTC(valid_non_utc_ber_timestamp_val))
        expected_val_non_utc_ber = "2022-03-01 08:11:04+00:00"

        converted_val_non_utc_ind =str(dt_util.convertToUTC(valid_non_utc_ind_timestamp_val))
        expected_val_non_utc_ind = "2022-03-01 03:41:04+00:00"
        converted_val_utc =str(dt_util.convertToUTC(valid_utc_timestamp_val))
        expected_val_utc = "2022-03-01 09:11:04+00:00"

        self.assertEqual(converted_val_non_utc_ber,expected_val_non_utc_ber)
        self.assertEqual(converted_val_non_utc_ind,expected_val_non_utc_ind)
        self.assertEqual(converted_val_utc,expected_val_utc)




if __name__ == "__main__":
    unittest.main()






