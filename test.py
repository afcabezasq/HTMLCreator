from datetime import datetime, timedelta
def test_date_format():
    date = datetime.strptime("06/24/2023 02:06:24 PM","%m/%d/%Y %I:%M:%S %p")
    assert date.hour == 14
    assert date.day == 24
    assert date.month == 6
    assert date.year == 2023
    assert date.minute == 6
    assert date.second == 24
    
if __name__ == "__main__":
    test_date_format()