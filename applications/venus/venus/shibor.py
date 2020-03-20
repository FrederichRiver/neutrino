#!/usr/bin/python3
import pandas as pd
from venus.stock_base import StockEventBase


class EventShibor(StockEventBase):
    def get_shibor_url(self, year):
        url = (
            f"http://www.shibor.org/shibor/web/html/"
            f"downLoad.html?nameNew=Historical_Shibor_Data_{year}.xls"
            f"&downLoadPath=data&nameOld=1{year}.xls"
            f"&shiborSrc=http://www.shibor.org/shibor/")
        return url

    def get_last_update(self):
        import datetime
        release_date = self.mysql.select_values('shibor', 'release_date')
        if not release_date.empty:
            d = release_date[0].tolist()
            result_date = d[-1]
        else:
            result_date = datetime.date(2004, 1, 1)
        return result_date

    def get_shibor_data(self, df):
        from dev_global.env import GLOBAL_HEADER, TIME_FMT
        from jupiter.utils import ERROR
        try:
            if not df.empty:
                df.columns = [
                    'release_date', 'overnight', '1W', '2W',
                    '1M', '3M', '6M', '9M', '1Y']
                df['release_date'] = pd.to_datetime(
                    df['release_date'], format=TIME_FMT)
                # get the last update date
                last_update = self.get_last_update()
                # filter the datetime already updated.
                df = df[df['release_date'] > last_update]
                print(df)
                for index, row in df.iterrows():
                    sql = (
                        f"INSERT IGNORE INTO shibor "
                        f"(release_date,overnight,1W,2W,1M,3M,6M,9M,1Y) "
                        f"VALUES ("
                        f"'{row['release_date']}',{row['overnight']},"
                        f"{row['1W']},{row['2W']},{row['1M']},{row['3M']},"
                        f"{row['6M']},{row['9M']},{row['1Y']})"
                    )
                    self.mysql.engine.execute(sql)
        except Exception as e:
            ERROR(e)


if __name__ == '__main__':
    from datetime import date
    from dev_global.env import GLOBAL_HEADER
    event = EventShibor(GLOBAL_HEADER)
    year_list = range(2006, date.today().year + 1)
    year = 2020
    url = event.get_shibor_url(year)
    df = event.get_excel_object(url)
    event.get_shibor_data(df)
