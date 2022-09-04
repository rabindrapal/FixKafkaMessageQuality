from datetime import datetime
import pytz
from constant import EXPECTED_DATE_FORMAT
import logging
logger = logging.getLogger(__name__)

def convertToUTC(dateTimeValue):
    naive_datetime = datetime.strptime(dateTimeValue, EXPECTED_DATE_FORMAT)
    datetime_utc = naive_datetime.astimezone(pytz.utc)
    return datetime_utc

def isExpectedDateFormat(inDateTimeValue):
    IsFormatValid = False
    try:
        IsFormatValid = bool(datetime.strptime(inDateTimeValue, EXPECTED_DATE_FORMAT))
    except ValueError:
        ## skip and return false in case of non valid format of input datetime
        pass

    return IsFormatValid
