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

    def result_limit_get_today_status(self):
        result = self.limit - self.get_today_stats()
        return result

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
        result = self.result_limit_get_today_status()
        if result > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более "
                    f"{result} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00
    RUB_RATE: float = 1.00
    money_dict = {
        "usd": ["USD", USD_RATE],
        "eur": ["Euro", EURO_RATE],
        "rub": ["руб", RUB_RATE],
    }

    def get_today_cash_remained(self, currency) -> str:
        today_cash = round(self.result_limit_get_today_status(), 2)
        if today_cash == 0:
            return "Денег нет, держись"
        today_cash = round(today_cash / self.money_dict[currency][1], 2)
        if today_cash > 0:
            return (f"На сегодня осталось "
                    f"{today_cash} {self.money_dict[currency][0]}")
        else:
            return (f"Денег нет, держись: твой долг - "
                    f"{abs(today_cash)} {self.money_dict[currency][0]}")
