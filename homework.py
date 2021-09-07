import datetime as dt
from typing import Union


class Record:

    def __init__(
            self,
            amount: int,
            comment: str,
            date: Union[str, None] = None
    ) -> None:
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:

    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> int:
        now = dt.datetime.now().date()
        amount: int = 0
        for record in self.records:
            if record.date == now:
                amount += record.amount
        return amount

    def get_week_stats(self) -> int:
        day_week_ago = dt.date.today() - dt.timedelta(days=7)
        today = dt.datetime.now().date()
        amount = 0
        for record in self.records:
            if day_week_ago <= record.date <= today:
                amount += record.amount
        return amount


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        result = self.limit - self.get_today_stats()
        if self.limit > self.get_today_stats():
            return (f"Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более {result} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00

    def currency_is_usd(self):
        day_result = 0
        local_limit = self.limit
        currency = "USD"
        local_limit = round(local_limit / self.USD_RATE, 2)
        day_result = round(self.get_today_stats() / self.USD_RATE, 2)
        result = (currency, local_limit, day_result)
        return result

    def currency_is_euro(self):
        day_result = 0
        local_limit = self.limit
        currency = "Euro"
        local_limit = round(local_limit / self.EURO_RATE, 2)
        day_result = round(self.get_today_stats() / self.EURO_RATE, 2)
        result = (currency, local_limit, day_result)
        return result

    def currency_is_rub(self):
        day_result = 0
        local_limit = self.limit
        currency = "руб"
        day_result = round(self.get_today_stats(), 2)
        result = (currency, local_limit, day_result)
        return result

    def get_today_cash_remained(self, currency) -> str:
        if currency == "usd":
            result = self.currency_is_usd()
        if currency == "eur":
            result = self.currency_is_euro()
        if currency == "rub":
            result = self.currency_is_rub()
        if (result[1] - result[2]) == 0:
            return "Денег нет, держись"
        elif result[1] > result[2]:
            remains = round(result[1] - result[2], 2)
            return (f"На сегодня осталось "
                    f"{remains} {result[0]}")
        elif result[1] < result[2]:
            debt = round(result[2] - result[1], 2)
            return (f"Денег нет, держись: твой долг - "
                    f"{debt} {result[0]}")
