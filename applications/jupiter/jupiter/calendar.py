#!/usr/bin/python3

import datetime
from datetime import date


class CalendarBase(object):
    def __init__(self, year=None):
        import datetime
        from datetime import date
        self.today = date.today()
        self.YEAR = year
        DAYS_IN_YEAR = 365 if self.YEAR%4 else 366
        self.days = [date(self.YEAR, 1, 1) + datetime.timedelta(days=i) for i in range(DAYS_IN_YEAR)]

    def _the_Nth_weekday_in_month(self):
        pass

    def __str__(self):
        return f"{self.today}"    

class Vocation(CalendarBase):
    def __init__(self, year, state='CHN'):
        import datetime
        super(Vocation,self).__init__(year=year)
        self.STATE = state
        
    def new_year(self):
        return date(self.YEAR, 1, 1)
    
    def chrismax(self):
        return date(self.YEAR, 12, 25)
 
    def national_day(self):
        if self.STATE == 'CHN':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'US':
            return date(self.YEAR, 7, 4)
        elif self.STATE == 'DU':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'JAP':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'UK':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'TW':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'HK':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'AU':
            return date(self.YEAR, 10, 1)
        elif self.STATE == 'CAN':
            return date(self.YEAR, 10, 1)
        
    def chinese_vocation(self):
        result = [
            date(self.YEAR, 1, 2),
            date(self.YEAR, 1, 3),
            date(self.YEAR, 4, 5),
            date(self.YEAR, 5, 1),
            date(self.YEAR, 5, 2),
            date(self.YEAR, 5, 3),
            date(self.YEAR, 10, 1),
            date(self.YEAR, 10, 2),
            date(self.YEAR, 10, 3),
            date(self.YEAR, 10, 4),
            date(self.YEAR, 10, 5),
            date(self.YEAR, 10, 6),
            date(self.YEAR, 10, 7),
        ]
        return result

class TradeDay(Vocation):
    def trade_day(self):
        trade_day = [d for d in self.days if d not in self.chinese_vocation()]
        return trade_day

    def quarter(self, dt:datetime.date):
        if dt.month <= 3:
            return 1
        elif dt.month <= 6:
            return 2
        elif dt.month <= 9:
            return 3
        else:
            return 4

    def period(self, base_period:datetime.date, delta=0):
        y, m = base_period.year, base_period.month
        # quarter > delta
        quarter = self.quarter(base_period)
        if quarter > delta:
            p = quarter -delta
        else:
            p = 4 - (delta - quarter)%4
            y -= int((delta - quarter)/4) + 1
        if p==1:
            period = datetime.date(y, 3, 31)
        elif p==2:
            period = datetime.date(y, 6, 30)
        elif p==3:
            period = datetime.date(y, 9, 30)
        elif p==4:
            period = datetime.date(y, 12, 31)
        return period

def event():
    cal = CalendarBase()
    print(cal)

if __name__ == "__main__":
    trade_period = TradeDay(2020)
    x = [trade_period.period(trade_period.today, i) for i in range(3)]
    print(x)
    